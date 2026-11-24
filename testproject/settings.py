from django_env_drift import Env


env = Env()

SECRET_KEY = env.str('SECRET_KEY', default='test')
USE_TZ = True
INSTALLED_APPS = ['django_env_drift']
