# import inspect
# import subprocess
# import sys
# from distutils.command.build import build
# from setuptools.command.install import install

try:
    from setuptools import setup, find_packages
except ImportError:
    import ez_setup

    ez_setup.use_setuptools()
    from setuptools import setup, find_packages

setup(
    name="step",
    version="0.0.1",
    url='https://github.com/mattpaletta/step',
    packages=find_packages(),
    include_package_data=True,
    install_requires=["cuckoostash", "configparser", "pqdict"],
    setup_requires=["Cython"],
    author="Matthew Paletta",
    author_email="mattpaletta@gmail.com",
    description="Step cache",
    license="BSD",
    dependency_links=[
        'git+git://github.com/mattpaletta/configparser.git@master#egg=configparser-0'
        'git+git://github.com/mattpaletta/cuckoostash.git@master#egg=cuckoostash-0'
        'git+git://github.com/mattpaletta/pqdict.git@master#egg=pqdict-0'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Communications',
    ],
    # cmdclass={
    #     'build': BuildCommand,
    #     'install': InstallCommand,
    # },
)