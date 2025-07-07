from setuptools import setup, find_packages

setup(
    name="cursor",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'flask>=2.0.0',
        'flask-cors>=3.0.0',
        'aiohttp>=3.8.0',
        'mcp-server>=0.1.4',
        'python-dotenv>=0.19.0',
        'websockets>=10.0',
        'requests>=2.26.0',
        'typing-extensions>=4.0.0',
        'asyncio>=3.4.3',
        'pathlib>=1.0.1',
        'werkzeug>=2.0.0',
        'jinja2>=3.0.0',
        'markupsafe>=2.0.0',
        'itsdangerous>=2.0.0',
        'click>=8.0.0'
    ],
    python_requires='>=3.8',
) 