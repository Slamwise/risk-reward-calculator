from setuptools import setup

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='riskit',
    url='https://github.com/Slamwise/risk-reward-calculator.git',
    author='Slamwise',
    author_email='',
    # Needed to actually package something
    packages=['riskit'],
    # Needed for dependencies
    install_requires=['numpy', 'requests', 'json', 'datetime', 'dateutil', 'warnings'],
    # *strongly* suggested for sharing
    version='0.1',
    # The license can be anything you like
    license='MIT',
    description=''
    # long_description=open('README.txt').read(),
)
