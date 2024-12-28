from setuptools import setup, find_packages

setup(
    name='web2md',
    version='0.1.0',
    description='A FastAPI-based web service that converts HTML web pages to Markdown format.',
    author='Your Name',
    author_email='your.email@example.com',
    packages=find_packages(),
    install_requires=[
        'aiohttp==3.11.7',
        'beautifulsoup4==4.12.3',
        'fastapi==0.115.5',
        'html2text',
        'requests==2.32.3',
        'uvicorn==0.32.1',
        'pydantic==2.10.2',
    ],
    entry_points={
        'console_scripts': [
            'web2md=app:main',  # Assuming you have a main function in app.py
        ],
    },
) 