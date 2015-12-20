from setuptools import setup

setup(
    name='ldsconf',
    version='1.0.1',
    description='LDS General Conference Study Plan Generator',
    url='https://github.com/burnhamup/ldsconf',
    author='Chris Burnham',
    author_email="chris@burnhamup.com",
    license='MIT',
    packages=['ldsconf'],
    install_requires=['lxml', 'requests'],
    data_files=[('data', ['data/conferences.json'])],
    entry_points={
        'console_scripts': [
            'ldsconf=ldsconf.main:main'
        ]
    }
)
