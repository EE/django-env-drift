import os

import pytest

from django_env_drift import Env


@pytest.fixture
def asked(monkeypatch):
    asked = set()
    monkeypatch.setattr(Env.ENVIRON, 'asked', asked)
    return asked


def test_notes_every_name_asked_for_set_or_not(asked, monkeypatch):
    monkeypatch.setenv('DATABASE_URL', 'postgres:///db')
    env = Env()

    env.db()
    env.bool('UNSET_FLAG', default=False)
    'PROBED' in env

    assert asked == {'DATABASE_URL', 'UNSET_FLAG', 'PROBED'}


def test_loading_a_dotenv_file_asks_nothing(asked, tmp_path):
    (tmp_path / '.env').write_text('STALE_LINE=1\n')

    Env.read_env(tmp_path / '.env')

    assert os.environ['STALE_LINE'] == '1'
    assert asked == set()
