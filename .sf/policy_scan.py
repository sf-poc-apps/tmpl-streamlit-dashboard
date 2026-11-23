#!/usr/bin/env python3
"""Software Factory policy scan. Runs in CI and in the builder before every push.

Blocks code patterns that this public POC does not allow: outbound network calls
from the server, email, raw sockets, miners, credential-collecting forms, iframes
and removal of the POC banner. Exit code 1 means at least one blocking finding.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
POLICY = json.loads((ROOT / ".sf" / "policy.json").read_text())
SKIP_DIRS = {".git", "node_modules", ".next", ".sf", ".venv", "venv", "__pycache__", ".pytest_cache", "dist", "build"}
TEXT_EXT = {".py", ".js", ".mjs", ".cjs", ".ts", ".tsx", ".jsx", ".html", ".htm", ".css", ".json", ".toml",
            ".yml", ".yaml", ".sh", ".conf", ".template", ".cfg", ".ini"}
ALLOWED_HOSTS = ("localhost", "127.0.0.1", "0.0.0.0", "fonts.googleapis.com", "fonts.gstatic.com",
                 "cdn.jsdelivr.net", "unpkg.com", "cdnjs.cloudflare.com", "github.com", "www.w3.org",
                 "schemas.", "json-schema.org", "nextjs.org", "react.dev", "fastapi.tiangolo.com", "streamlit.io",
                 "docs.", "example.com", "registry.npmjs.org", "pypi.org", "opencode.ai")

RULES = [
    ("email", r"\bsmtplib\b|\bnodemailer\b|\bsendgrid\b|\bmailgun\b|\bsmtp\.", "Sending email is not allowed."),
    ("socket", r"\bsocket\.socket\(|\bnet\.createConnection\(|\bdgram\b", "Raw sockets are not allowed."),
    ("miner", r"stratum\+tcp|xmrig|coinhive|cryptonight|minero", "Crypto mining is not allowed."),
    ("subprocess", r"\bchild_process\b|\bsubprocess\.(Popen|run|call|check_output)\b|\bos\.system\(",
     "Spawning processes from app code is not allowed."),
    ("server_http", r"\brequests\.(get|post|put|delete|request)\(|\bhttpx\.|\burllib\.request\b|\baiohttp\b",
     "Outbound HTTP from the server is not allowed."),
    ("password_field", r"type\s*=\s*[\"']password[\"']", "Password fields are not allowed (no logins in this POC)."),
    ("iframe", r"<iframe\b", "Embedding other sites with iframes is not allowed."),
    ("eval", r"\beval\(|new Function\(", "Dynamic code evaluation is not allowed."),
    ("secrets", r"(api[_-]?key|secret|token)\s*[:=]\s*[\"'][A-Za-z0-9_\-]{16,}[\"']", "Hard-coded secrets are not allowed."),
]
URL_RE = re.compile(r"https?://([A-Za-z0-9.\-]+)")


def files():
    for p in ROOT.rglob("*"):
        if p.is_file() and not (set(p.relative_to(ROOT).parts) & SKIP_DIRS) and p.suffix in TEXT_EXT:
            if p.stat().st_size < 400_000 and p.name not in ("package-lock.json",):
                yield p


def main() -> int:
    findings = []
    allow = POLICY.get("allow", {})
    for path in files():
        rel = str(path.relative_to(ROOT))
        text = path.read_text(errors="ignore")
        for rule_id, pattern, message in RULES:
            if any(rel.startswith(a) for a in allow.get(rule_id, [])):
                continue
            for m in re.finditer(pattern, text, flags=re.IGNORECASE):
                line = text.count("\n", 0, m.start()) + 1
                findings.append({"rule": rule_id, "file": rel, "line": line, "message": message})
        if path.suffix in {".py", ".ts", ".tsx", ".js", ".mjs"} and not rel.startswith(("public/", "tests/", "test")):
            for m in URL_RE.finditer(text):
                host = m.group(1).lower()
                if not any(host == h or host.startswith(h) or host.endswith("." + h) for h in ALLOWED_HOSTS):
                    line = text.count("\n", 0, m.start()) + 1
                    findings.append({"rule": "external_url", "file": rel, "line": line,
                                     "message": f"External host {host} referenced in app code."})
    for ref in POLICY.get("banner_refs", []):
        p = ROOT / ref
        if not p.exists() or "sf-banner" not in p.read_text(errors="ignore"):
            findings.append({"rule": "banner", "file": ref, "line": 0, "message": "POC banner reference missing."})
    print(json.dumps({"findings": findings, "count": len(findings)}, indent=2))
    for f in findings:
        print(f"::error file={f['file']},line={f['line']}::[{f['rule']}] {f['message']}", file=sys.stderr)
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
