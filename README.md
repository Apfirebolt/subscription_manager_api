# Subscription Manager App

## Steps to scaffold the project

# Create and enter your new project directory
mkdir subscription_manager && cd subscription_manager

# Initialize a uv project (pins python, creates pyproject.toml and uv.lock)
uv init --python 3.13

# Add core Django
uv add django

# Add development-only tools (like a linter/formatter) using the dev group
uv add --dev ruff pytest-django

# Generate the Django project structure in the current directory
uv run django-admin startproject config .

# Run default migrations
uv run python manage.py migrate

# Start the development server
uv run python manage.py runserver

The real magic of a modern uv workflow shines when syncing states—whether pulling down changes on a coworker's machine, or deploying via a pipeline.
On a fresh checkout / developer setup:
Instead of running individual install commands, simply run:

uv sync

This looks at uv.lock, automatically checks if your local .venv matches the lockfile precisely, drops unlisted packages, and installs the exact versions specified.
For Production deployments (e.g., Docker):
In production, you don't want testing frameworks bloating your runtime environment. You can pass the --no-dev flag to ensure a lean, secure image:

uv sync --no-dev --locked

### Added Postgres related dependencies

```uv add "psycopg[binary]"```

- uv run python manage.py migrate

To add a new Django app simply run

- uv run python manage.py startapp users