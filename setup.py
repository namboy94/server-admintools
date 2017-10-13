# imports
import os
from server_admin import version
from server_admin.sudo import quit_if_not_sudo
from setuptools import setup, find_packages


def readme() -> str:
    """
    Reads the readme file.
    :return: the readme file as a string, 
             if possible converted from markdown to RST
    """

    with open('README.md') as f:
        content = f.read()

    try:
        # noinspection PyPackageRequirements
        import pypandoc
        content = pypandoc.convert(content, 'rst', format='md')
    except ModuleNotFoundError:
        print("pypandoc not installed, will use raw markdown")
        pass

    return content


def find_scripts():
    """
    Returns a list of scripts in the scripts directory
    :return: the list of scripts
    """
    scripts = []
    for file_name in os.listdir("scripts"):
        if not file_name == "__init__.py" and os.path.isfile(
                os.path.join("scripts", file_name)):
            scripts.append(os.path.join("scripts", file_name))
    return scripts

if __name__ == "__main__":

    quit_if_not_sudo()

    setup(
        name="server-admin",
        version=version,
        description="A collection of server administration scripts",
        long_description=readme(),
        classifiers=[
            "Environment :: Console",
            "Natural Language :: English",
            "Intended Audience :: System Administrators",
            "Development Status :: 1 - Planning",
            "Operating System :: POSIX :: Linux",
            "Programming Language :: Python :: 3",
            "Topic :: System :: Systems Administration",
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
        ],
        url="https://gitlab.namibsun.net/namboy94/server-admin",
        download_url="https://gitlab.namibsun.net/namboy94/"
                     "server-admin/repository/archive.zip?ref=master",
        author="Hermann Krumrey",
        author_email="hermann@krumreyh.com",
        license="GNU GPL3",
        packages=find_packages(),
        install_requires=['typing'],
        test_suite='nose.collector',
        tests_require=['nose'],
        scripts=find_scripts(),
        zip_safe=False
    )
