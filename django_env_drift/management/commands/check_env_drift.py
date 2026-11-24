import fnmatch
from typing import Any

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from django_env_drift import PLATFORM_VARIABLES, Env


class Command(BaseCommand):
    help = 'List the environment variables that are set but that settings never read, one name per line.'

    def handle(self, *args: Any, **options: Any) -> None:
        environ = Env.ENVIRON
        if not environ.asked:
            # Every variable would be listed, which says only that settings use another Env.
            raise CommandError('Nothing was read through django_env_drift.Env. Do settings create their env with it?')
        ignore = getattr(settings, 'ENV_DRIFT_IGNORE', PLATFORM_VARIABLES)
        names = sorted(
            name for name in environ
            if name not in environ.asked
            and not any(fnmatch.fnmatchcase(name, pattern) for pattern in ignore)
        )
        for name in names:
            self.stdout.write(name)
        if names:
            raise CommandError(f'{len(names)} set but unread.')
