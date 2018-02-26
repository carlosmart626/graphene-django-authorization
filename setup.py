from setuptools import find_packages, setup
from graphene_django_authorization import __version__

tests_require = [
    'pytest>=2.7.2',
    'pytest-cov',
    'coveralls',
    'coverage==4.4.2',
    'mock',
    'pytz',
    'django-filter',
    'pytest-django==3.1.2',
    'graphene-django<2.0',
    'django<2.0'
]

setup(
    name='graphene-django-authorization',
    version=__version__,

    description='Graphene Django Authorization Integration',
    long_description=open('README.rst').read(),

    url='https://github.com/CarlosMart626/graphene-django-authorization',

    author='Carlos Martinez',
    author_email='carlosmart626@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],

    keywords='api graphql protocol rest relay graphene django autotization',

    packages=find_packages(exclude=['tests']),

    install_requires=[
        'graphene-django<2.0'
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=tests_require,
    extras_require={
        'test': tests_require,
    },
    include_package_data=True,
    zip_safe=False,
    platforms='any',
)
