# Development

## Local setup

Install the package in editable mode along with the test dependencies:

```bash
python -m pip install -e .
python -m pip install pytest pytest-asyncio
```

Django and discord.py are provided by the BallsDex host installation. The test suite
configures an in-memory SQLite database and stubs the BallsDex-only `bd_models` import, so
it can run without a full bot deployment.

## Running tests

```bash
python -m pytest -q
```

The suite covers settings validation, the progression threshold calculation, and the
cog's role assignment workflow.

## Database migrations

After changing `role_reward/models.py`, generate and verify migrations:

```bash
python manage.py makemigrations role_reward
python manage.py migrate
```

Run `makemigrations --check --dry-run` in CI to catch missing migrations.

## Building these docs locally

Install the documentation dependencies and build the MkDocs site:

```bash
python -m pip install -r docs/requirements.txt
mkdocs build --strict
```

Serve it locally with live reload while editing:

```bash
mkdocs serve
```

Open <http://127.0.0.1:8000/> in a browser. The generated `site/` directory is ignored by
Git.

## Read the Docs

The site is configured through `.readthedocs.yaml` at the repository root. It builds the
default branch with MkDocs Material on Read the Docs and publishes to
<https://ballsdex-role-reward.readthedocs.io/> on every push.
