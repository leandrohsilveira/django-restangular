from setuptools import setup, find_packages

setup(
    name = "django-restangular",
    version = "1.0.0",
    url = 'http://github.com/leandrohsilveira/django-restangular',
    license = 'BSD',
    description = "A short URL handler for Django apps.",
    author = 'Leandro Hinckel Silveira',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    install_requires = ['setuptools'],
)