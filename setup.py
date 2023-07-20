from setuptools import setup, find_packages

setup(
    name="Makita-UI",
    version="0.3.1",
    author="Jelle Teijema",
    author_email="j.j.teijema@uu.nl",
    description="Experimental UI for the asreview-makita package",
    packages=find_packages(),
    install_requires=[
        "asreview-makita",
        "PySimpleGUI>=4.0.0"
    ],
    entry_points={
    "console_scripts": [
        "makita-ui=makita_ui:run_makita_ui"
    ]
    }
)