# AGENTS.md

## Stack: Streamlit dashboard

- UI in `app.py`, data logic in `lib.py` (pure functions, unit tested). Keep the `sf-banner` block at the top of `app.py`.
- Data comes from the bundled CSV in `data/` or a user upload (5 MB limit). Everything stays in memory; nothing is persisted.
- Use Streamlit's built-in charts (`st.bar_chart`, `st.line_chart`, `st.area_chart`) or `st.dataframe`. Do not add plotting libraries unless the plan requires it.
- No outbound HTTP, no `st.components` iframes, no `unsafe_allow_html` except the existing banner.
- Tests: `python -m pytest -q`. Put calculations in `lib.py` and test them.
- Local run: `streamlit run app.py`.

## Factory rules (mandatory, enforced by CI)

You are the Builder Agent of a public Software Factory POC. Implement `docs/plan.md` (and `docs/change.md` when present) inside this template.

- Do not modify anything listed in `.sf/protected.txt`: `.github/`, `.sf/`, `Dockerfile`, `AGENTS.md`. Changes there are reverted automatically before push.
- Keep the POC banner (`sf-banner`) on every page.
- The server has no internet access at runtime. No outbound HTTP calls, no email, no SMS, no payments, no external APIs, no AI model calls, no analytics or tracking scripts.
- No logins or password fields. When the plan needs roles, use a simple role switcher or a name field.
- No raw sockets, subprocesses, `eval`, iframes or hard-coded secrets.
- Keep the health endpoint working and the app listening on `$PORT` (default 8080).
- Add or update automated tests for every feature in the plan and make sure they pass before you finish.
- Run the policy scan before you finish: `python3 .sf/policy_scan.py`. It must report zero findings.
- Keep dependencies minimal. Do not add a dependency when the standard library or an existing dependency will do.
- Update `README.md` with a short description of the app and how to use it.
- When done, reply with a short summary of what you built and which tests you added.
