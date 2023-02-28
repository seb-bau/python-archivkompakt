from setuptools import setup

setup(
    name='archivkompakt',
    version='0.1.1',
    description='Aareon Archiv Kompakt connector',
    long_description='Basic implementation for communication with the Aareon Archiv Kompakt REST API',
    url='https://github.com/seb-bau/python-archivkompakt',
    author='Sebastian Bauhaus',
    author_email='sebastian@bytewish.de',
    license='MIT',
    packages=['archivkompakt'],
    install_requires=['requests>=2.0'],
    keywords=['AAK', 'archiv kompakt', 'archivkompakt', 'aareon'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires=">=3.0"
)
