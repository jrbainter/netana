#!/usr/bin/env python3

from setuptools import setup, find_packages
""" This file is used to build the 'NetAna' distrubtion.
    All files in 'examples' directory and all files defined in the MANFEST.in
    template file. """
setup(name='netana',
      version = '3.1.2',
      zip_safe=True,
      include_package_data = True,
      install_requires = ['python3','python3-matplotlib>=1.3.1','python3-numpy>=1.8.2'],
      scripts = ["cp-examples.sh"],
      packages=['netana'],
      package_data={'netana': ['examples/*', 'doc/*'],
        "" : ['netana-3.1.0-md5sums', 'netana.desktop', 'license', 'change.log']},
      author= 'James Bainter',
      maintainer= 'James Bainter',
      author_email= 'bainter8326@gmail.com',
      description= 'Electronic Network Analyzer',
      long_description= 'This program solves electronic AC & DC Mash and Node network equations using matrix algebra.',
      platforms= [ 'Linux', 'MSWindows' ],
      keywords="network circuit node mash analysis",
      license = "GPL-3 - GNU General Public License",
      url = "https://github.com/jrbainter/netana"
      )

