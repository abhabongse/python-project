#!/usr/bin/env python3
from myhelpers.primitives import EnvVariable


# def non_negative(value):
#     return value >= 0


seconds_amount = EnvVariable(default=0, parse=int, validate=lambda x: x >= 0)
print(seconds_amount)


class ApplicationConfig:
    SECRET_KEY = EnvVariable(required=True, validate=lambda x: len(x) > 0)
    DELAY_SECONDS = seconds_amount
    # POLLING_SECONDS = seconds_amount
    FAUX_NAME = EnvVariable(env_name='REAL_NAME')

    def preload_all(self):
        """
        Optionally call this method at the program start-up
        if you wish to pre-load all environment variables.
        Use this method is useful if you wish for your program to fail
        as earliest as possible when configuration is not complete.
        """
        for key in self._envvar_fields_.keys():
            getattr(self, key)


conf = ApplicationConfig()
conf.preload_all()
print(conf.__dict__)
print(ApplicationConfig.DELAY_SECONDS)
