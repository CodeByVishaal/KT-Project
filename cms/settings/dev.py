from .base import *
from decouple import config

DEBUG=config('DEBUG')
print("Running in Dev Environment")
ALLOWED_HOSTS=config('ALLOWED_HOSTS').split(',')
