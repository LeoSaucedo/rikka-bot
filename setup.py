from setuptools import setup
setup(name = 'rikka-bot',
    version='0.1',
    description='A discord bot that performs various functions.',
    url='https://github.com/LeoSaucedo/rikka-bot',
    author='LeoSaucedo',
    author_email='carlos@cgsphoto.com',
    license='GPL-3.0',
    packages=['rikka-bot'],
    install_requires=[
        'discord',
        'asyncio',
        'googletrans',
        'bs4'
        'dblpy',]
    )