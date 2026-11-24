import os
from io import StringIO

import pytest
from django.core.management import CommandError, call_command

from django_env_drift import Env


def check_env_drift():
    # pytest sets it for the duration of each test.
    os.environ.pop('PYTEST_CURRENT_TEST', None)
    stdout = StringIO()
    with pytest.raises(CommandError) as error:
        call_command('check_env_drift', stdout=stdout)
    return stdout.getvalue(), str(error.value)


def test_lists_what_is_set_and_never_read(monkeypatch):
    for name in ['SECRET_KEY', 'PATH', 'HEROKU_APP_NAME', 'OLD_NAME', 'REMOVED']:
        monkeypatch.setenv(name, 'value')

    stdout, error = check_env_drift()

    assert stdout == 'OLD_NAME\nREMOVED\n'
    assert error == '2 set but unread.'


def test_skips_what_ENV_DRIFT_IGNORE_lists_instead_of_the_platform(monkeypatch, settings):
    settings.ENV_DRIFT_IGNORE = ['BUILD_*']
    for name in ['BUILD_ID', 'PATH']:
        monkeypatch.setenv(name, 'value')

    stdout, _ = check_env_drift()

    assert stdout == 'PATH\n'


def test_refuses_when_settings_read_nothing_through_env(monkeypatch):
    monkeypatch.setattr(Env.ENVIRON, 'asked', set())
    monkeypatch.setenv('SECRET_KEY', 'value')

    stdout, error = check_env_drift()

    assert stdout == ''
    assert 'django_env_drift.Env' in error
