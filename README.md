# django-env-drift

A setting is removed or renamed, the code ships,
and the old variable stays on every server that ever had it.
Nothing reads it and nothing complains,
so a deployment's config fills with names nobody can explain and nobody dares to unset,
some of them credentials still valid somewhere.

This app tells which they are.
Settings read the environment through an `Env` that notes every name it is asked for,
and `check_env_drift`, run on the deployment, lists what is set and was never asked for:

```
$ heroku run python manage.py check_env_drift
MAILGUN_API_KEY
SENTRY_URL
CommandError: 2 set but unread.
```

## The idea

- **Asked, not grepped.**
  A grep finds `AWS_*` in settings and calls them used,
  even on a deployment where settings read them only when `STORAGE=s3` and it isn't.
  This app records what settings asked for in the process that runs them,
  so the answer is per deployment.
- **The deployment's environment, not a file.**
  The leftovers live in the platform's config, which no `.env` in the repository shows.
- **Asked counts, set or not.**
  A setting that fell back to its default still asked, so the name is in use.
- **Names only.**
  Values are secrets, and nothing here prints or compares them.
- **What it cannot answer, it refuses.**
  If settings read nothing through `Env`, every variable would be listed,
  so the command fails instead.

## Install

It is not on PyPI yet; depend on a commit of this repository:

```
django-env-drift @ git+https://github.com/EE/django-env-drift.git@<sha>
```

Add `'django_env_drift'` to `INSTALLED_APPS`,
and create the settings' `Env` from this package instead of `environ`:

```python
from django_env_drift import Env

env = Env()
```

It is django-environ's `Env`, every getter as before.

## Cleaning up a deployment

Run the command where the variables are:
`heroku run`, `scalingo run`, `kubectl exec`, or a shell on the server.
It prints one name per line and exits non-zero if it printed any.

Before unsetting a name, find what stopped reading it: `git log -S NAME` shows the commit.
If the setting was renamed, make sure the new name carries the value,
or the deployment has been running on the new name's default since that commit.
Then unset it:

```bash
heroku config:unset MAILGUN_API_KEY SENTRY_URL
```

Unset after the deploy that stops reading a variable, never before,
since the release still running needs it until then.
For the same reason the check does not belong in a release phase:
it would fail every deploy that removes a setting.
Run it by hand or on a schedule.

Run locally, it lists stale lines in `.env` too,
since `read_env()` loads them into the environment.

## What it cannot see

The command sees only what settings ask `Env` for,
so it also lists what something else reads:
the shell, the platform, a library reading `os.environ` itself, a frontend build.
It skips the globs in `ENV_DRIFT_IGNORE`,
which defaults to `PLATFORM_VARIABLES` in `django_env_drift/__init__.py`:
those of the shell, the Python and Node buildpacks, gunicorn, Heroku and Scalingo.
Extend it with your own:

```python
from django_env_drift import PLATFORM_VARIABLES, Env

ENV_DRIFT_IGNORE = [
    *PLATFORM_VARIABLES,
    'SENTRY_ENVIRONMENT',  # sentry_sdk.init() reads it itself
    'VITE_*',  # the frontend build
]
```

Keep the reason next to each:
an entry whose reason has gone hides the leftover this app exists to find.

`env` called outside settings, in a view or a task, asks only when that code runs,
which the command does not do.
Read the environment in settings.

## Deliberately not here

- **Unsetting.**
  The command prints names; a person decides.
- **Settings nobody uses.**
  A variable settings read into a setting that no code uses is set, read and still dead.
  That is a question about the code, not the deployment.
- **Watching `os.environ`.**
  Replacing it would catch libraries that read it directly,
  but not `getenv` from C, shell scripts or a frontend build,
  so the ignore list would stay, and a library would be patching a process-wide object.

## Development

```bash
poetry install
poetry run pytest
poetry run flake8
```
