from setuptools import setup

version = '0.0.0b1'

setup(
    name='djsn_scrapper',
    install_requires=[
        'pyshp',
        'requests',
        'ujson',
        'uncurl',
    ],
    entry_points={
        'console_scripts': [
            'extract_data = scrapper.extract_data:main',
            'retrieve_kabupaten_id = scrapper.retrieve_kabupaten_id:main',
        ],
    },
    tests_require=["pytest"],
    author='Sari Setianingsih',
    author_email='sari.thok@gmail.com',
)