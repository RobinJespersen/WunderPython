#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name='WunderPython',
      version='0.1a1',
      
      description='API wrapper for the Wunderground API',
      long_description='API wrapper for the Wunderground API',
      
      author='Robin Jespersen',
      author_email='robin.jespersen@tum.de',
      url='https://github.com/RobinJespersen/WunderPython',
      
      license = "MIT",
      classifiers = [
        'Development Status :: 3 - Alpha',        
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',        
        'License :: OSI Approved :: MIT License',        
        'Programming Language :: Python :: 2', 
        'Programming Language :: Python :: 2.7'
      ],
      
      keywords="weather data wunderground",
      packages = find_packages(),
        
      test_suite="tests")
