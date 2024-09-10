from setuptools import setup, find_packages

setup(
    name='dev_tracker',
    version='1.0.0',
    description='A tool to track developer activity and time spent on files',
    author='Uzma Mansoori',
    author_email='uzmamansoori220@gmail.com',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'dev_tracker=dev_tracker.main:main',
        ],
    },
    install_requires=[
        'watchdog',
        'pandas',
    ],
)
