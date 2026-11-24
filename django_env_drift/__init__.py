"""
django-environ asks ``Env.ENVIRON`` for every name,
the mapping ``FileAwareEnv`` swaps out to read secrets from files.
Here it is ``os.environ`` noting each name asked for,
so a name set and never asked for is one nothing read.
"""
import os
from collections.abc import Iterator, MutableMapping

import environ


#: Variables that the shell, the platform, its buildpacks and the process manager set or read,
#: which no settings module asks for.
#: The default of ``settings.ENV_DRIFT_IGNORE``.
PLATFORM_VARIABLES = (
    # process and shell, including what a one-off container (`heroku run`, `scalingo run`) adds
    'PATH', 'HOME', 'PWD', 'OLDPWD', 'SHLVL', '_', 'LANG', 'LC_*', 'TZ', 'TERM', 'COLUMNS', 'LINES', 'PS1',
    'HOSTNAME', 'CLIENT_OS',
    'LD_LIBRARY_PATH', 'LIBRARY_PATH', 'CPATH', 'CPPPATH', 'INCLUDE_PATH', 'PKG_CONFIG_PATH',
    # read by manage.py and wsgi.py before settings exist
    'DJANGO_SETTINGS_MODULE',
    # Python and Node buildpacks, and gunicorn
    'PYTHON*', 'NODE_*', 'WEB_CONCURRENCY*', 'FORWARDED_ALLOW_IPS', 'GUNICORN_CMD_ARGS',
    # Heroku, including dyno metadata and add-ons' extra copies of their URLs
    'DYNO', 'DYNO_RAM', 'PORT', 'STACK', 'HEROKU_*',
    # Scalingo
    'APP', 'CONTAINER', 'CONTAINER_*', 'REGION_NAME', 'SCALINGO_*',
)


class RecordingEnviron(MutableMapping[str, str]):
    """``os.environ``, noting in ``asked`` every name asked for, set or not."""

    def __init__(self) -> None:
        self.asked: set[str] = set()

    def __getitem__(self, name: str) -> str:
        self.asked.add(name)
        return os.environ[name]

    def setdefault(self, name: str, default: str) -> str:
        # How read_env() loads .env: a write, which asks nothing.
        return os.environ.setdefault(name, default)

    def __setitem__(self, name: str, value: str) -> None:
        os.environ[name] = value

    def __delitem__(self, name: str) -> None:
        del os.environ[name]

    def __iter__(self) -> Iterator[str]:
        return iter(os.environ)

    def __len__(self) -> int:
        return len(os.environ)


class Env(environ.Env):
    ENVIRON = RecordingEnviron()
