from setuptools import setup, find_packages

setup(
    name='web2md',
    version='0.1.0',
    description='Convert web pages to clean, readable Markdown',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Saad Khalid',
    author_email='saadkhalid913+dev@gmail.com',
    url='https://github.com/Saadkhalid913/web2md',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'beautifulsoup4>=4.12.3',
        'requests>=2.32.3',
        'html2text @ git+https://github.com/Saadkhalid913/html2text.git'
    ],
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
) 