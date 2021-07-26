from setuptools import setup

setup(
    name='riskit',
    version='0.0.0',
    description='Identify options strikes with the best risk/reward ratio for your stock plays',
    url='https://github.com/Slamwise/risk-reward-calculator.git',
    author='Slamwise',
    author_email='',
    license='MIT',
    packages=['riskit'],
    classifiers=[
        # How mature is this project? Common values are
        # 3 - Alpha
        # 4 - Beta
        # 5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Traders',
        'Intended Audience :: Financial and Insurance Industry',
        'Topic :: Office/Business :: Financial :: Investment',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Operating System :: OS Independent',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='stocks options finance market shares greeks implied volatility risk reward yolo',
    install_requires=['requests', 'beautifulsoup4', 'scipy', 'dateutil', 'warnings'],
)
