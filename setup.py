from setuptools import setup


def get_requirements():
    # intentionally naive, does not support include files etc
    with open("./requirements.txt") as fp:
        return fp.read().split()


setup(
    name="gitsane",
    packages=["gitsane", "gitsane.utils", "gitsane.commands"],
    version="0.1.0",
    description="sane(r) cli for common git operations",
    author="Jesper Wendel Devantier",
    url="https://github.com/jwdevantier/gitsane",
    license="MIT",
    install_requires=get_requirements(),
    options={"bdist_wheel": {"universal": True}},
    entry_points = {
        "console_scripts": [
            "gitsane=gitsane.__main__:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python",
    ]
)
