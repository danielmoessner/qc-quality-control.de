from .base import *

DEBUG = False

ALLOWED_HOSTS = get_secret("ALLOWED_HOSTS")

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'handlers': {
        'debug': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'tmp/logs/debug.log',
        },
        'info': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'tmp/logs/info.log',
        },
        'warning': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'tmp/logs/warning.log',
        },
        'error': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'tmp/logs/error.log',
        },
        'critical': {
            'level': 'CRITICAL',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'tmp/logs/critical.log',
        },
        'mail_admins': {
            'level': 'INFO',
            'class': 'django.utils.log.AdminEmailHandler',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['debug', 'info', 'warning', 'error', 'critical', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': True,
        }
    }
}
