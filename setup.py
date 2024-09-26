from setuptools import setup, find_packages

setup(
    name='pyji',
    version='1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        req.strip() for req in open('requirements.txt').readlines()
    ],
    entry_points={
        'console_scripts': [
            'pyji = main:main'
        ],
    },
    package_data={
        '': ['icons/*.png'],
    },
)
