from setuptools import setup, find_packages

setup(name='probutil',
      version='0.0.1',
      packages=find_packages(),

      author='Jong-Chan Kim',
      author_email='jongchank@gmail.com',
      description='Utils for handling probability distributions',
      long_description=open('README.md').read(),
      keywords='probability',
      url='https://github.com/jongchank/probutil',

      license='MIT',
      classifiers = [
	  'Development Status :: 3 - Alpha',
          'Environment :: Console'
      ]
)
