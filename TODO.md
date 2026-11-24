# TODO

## `FileAwareEnv`

django-environ's `FileAwareEnv` reads `NAME` from the file `NAME_FILE` points at,
through a `FileAwareMapping` in place of `os.environ`.
Settings using it read nothing through `Env`.
A `FileAwareEnv` here would be that class with `ENVIRON = FileAwareMapping(env=Env.ENVIRON)`,
noting `NAME_FILE` and `NAME` in the one `asked` set the command consults.

## Other platforms

`PLATFORM_VARIABLES` covers Heroku and Scalingo, whose variables were seen on running containers.
Kubernetes adds `<SERVICE>_SERVICE_HOST`, `<SERVICE>_PORT_<N>_TCP` and the like for every service in the namespace,
too many and too varied for `ENV_DRIFT_IGNORE` by hand;
Fly.io, Render and Railway each add a prefix of their own.
Add each from a real container's environment, not from memory.

## PyPI

The package is installed from a commit.
Publishing needs a workflow and a trusted publisher on PyPI.
