# CLAUDE.md

This repository is public.
Work on it often starts from a private project that uses it,
so nothing from such a project goes in here: no names, settings, variables, incidents or links to its docs —
not in code, tests, docs or commit messages.
Examples use made-up names (`MAILGUN_API_KEY`).

## Running tests

The README's Development section says how.
CI also runs the oldest versions `pyproject.toml` allows;
`.github/workflows/pytest.yml` lists them.

## What `Env` relies on

django-environ asks `Env.ENVIRON` for every name,
and `read_env()` writes `.env` into it with `setdefault`;
this package replaces only that mapping.
`env_tests.py` holds both: names asked for are noted, and loading `.env` asks for nothing.
If django-environ starts reaching the environment some other way, those tests are where it shows.

## Writing

The README owns why and how to use it; docstrings own how the code works; neither repeats the other.
Prose — README, `TODO.md`, docstrings, comments — breaks at clause boundaries, one sentence per line, not at a column.

`TODO.md` holds deferred work, a paragraph each, concrete enough to pick up cold.
A finished item is deleted in the change that finishes it.
