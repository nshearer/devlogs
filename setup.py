from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name = 'devlogs',
    version = '0.0.0.9', # version string
    description = 'Development VM Log Watcher',
    long_description = readme(),
    url = 'https://github.com/shearern/devlogs',
    author = 'Nathan Shearer',
    author_email = 'shearern@gmail.com',
    license = 'MIT',
    packages = ['devlogs', 'devlogs.monitors', 'devlogs.views'],
    #package_dir = {'': 'src'},
    entry_points = {
        'console_scripts': ['devlogs=devlogs.command_line:main'],
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Topic :: System :: Logging',
    ],
    install_requires=[
        'devhttp',
    ],
    include_package_data=True,
    zip_safe=False,  # True?
    )
