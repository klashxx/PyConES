"""setup conf"""

from setuptools import setup, find_packages

setup(name='rspace',
      version=0.1,
      author='Juan Diego Godoy Robles',
      url='https://klashxx.github.io/',
      author_email='klashxx@gmail.com',
      description='PyConEs 2016 Demo',
      license='GPL',
      platforms=['Linux x86_64', 'Darwin'],
      packages=find_packages(),
      entry_points={
          'console_scripts': [
              'rspace = rspace.main:main',
          ]
      },
      classifiers=['Environment :: Console',P
                   'Intended Audience :: System Administrators',
                   'License :: GPL',
                   'Natural Language :: Englih',
                   'Operating System :: POSIX :: Linux',
                   'Programming Language :: Python',
                   'Topic :: Utilities'],
      include_package_data=True,
      package_data={'rspace': ['secret/*']})
