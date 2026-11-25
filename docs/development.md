# Development

## Local setup

Install the package in editable mode along with the test dependencies:

```bash
python -m pip install -e .
python -m pip install pytest pytest-asyncio
```

Django and discord.py are provided by the BallsDex host installation.

## Running tests

```bash
python -m pytest -q
```

The test suite configures an in-memory SQLite database and stubs the
BallsDex-only `bd_models` import, so it can run without a full bot deployment.

## Database migrations

After changing `role_reward/models.py`, generate and verify migrations:

```bash
python manage.py makemigrations role_reward
python manage.py migrate
```

Run `makemigrations --check --dry-run` in CI to catch missing migrations.

## Building these docs locally

```bash
python -m pip install -r docs/requirements.txt
sphinx-build -b html docs docs/_build/html
```

Open `docs/_build/html/index.html` in a browser. On Linux and macOS you can
also run `make -C docs html`.

## Read the Docs

The site is configured through `.readthedocs.yaml` at the repository root.
Connect the GitHub repository to [Read the Docs](https://readthedocs.io/) and
the default branch will be built and published automatically on every push.
The version number in `docs/conf.py` is read from `pyproject.toml`, so released
documentation stays in sync with the package version.
