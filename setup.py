from distutils.core import setup

setup(
    name='daily-crunch',
    version='0.0.1',
    description='A basic framework for crunching MLB data at least for trying to Beat The Streak',
    packages=['daily-crunch'],
    install_requires=[
        'mlbgame',
        'datetime',
        'csv',
        'pandas',
        'tempfile',
        'requests',
    ],
)
