from setuptools import setup, find_packages

setup(
    name="ssot-rule-engine",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "flask==3.0.2",
        "flask-cors==4.0.0",
        "werkzeug==3.0.1",
        "pathlib==1.0.1",
    ],
) 