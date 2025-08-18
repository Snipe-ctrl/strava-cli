# st — Typer CLI Boilerplate

Minimal, sane Typer setup using a `src/` layout, editable install, and a console script named `st`.

## Quick start

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate

pip install -e ".[dev]"
mc --help
python -m st --help
```

## Adding commands

- Put simple commands in `src/st/cli.py` using `@app.command()`.
- For larger features, add modules in `src/st/commands/` and register them in `src/st/cli.py` with `app.command("name")(func)` or by mounting a sub-app via `app.add_typer(...)`.

## Tests

```bash
pytest -q
```

## Common pitfalls

- If `st --help` only shows a `--help` option, you didn't register any commands or there is an import loop. Keep business logic out of the command modules and avoid importing the top-level `app` inside command modules.
- If `python -m st` fails, check that `src/st/__main__.py` exists and that your editable install succeeded.
- If the console script `st` isn't found, your venv might be deactivated or the editable install failed.
