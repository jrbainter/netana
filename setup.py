#!/usr/bin/env python3

from  setuptools import setup, find_packages
""" This file is used to build the 'NetAna' distrubtion.
    All files in 'examples' directory and all files defined in the MANFEST.in
    template file. """

setup(
      name='netana',
      version = '3.3.2',
      packages=find_packages(),
      zip_safe=True,
      include_package_data = True,
      install_requires = ['python3-tk','python3-matplotlib','python3-pil','python3-pil.imagetk'],
      entry_points = { "gui_scripts" : ["netana=main:main"]},
      scripts = ["cp-examples.sh"],
      package_data={'netana': ['examples/*', 'doc/*',
        'netana-3.2.0-md5sums', 'netana.desktop', 'license', 'change.log', 'copyright' ]},
      author= 'James Bainter',
      maintainer= 'James Bainter',
      author_email= 'bainter8326@gmail.com',
      description= 'Electronic Network Analyzer',
      long_description= 'This program solves electronic AC & DC Mash and Node network equations using matrix algebra.',
      platforms= [ 'Linux', 'MSWindows', 'OSX' ],
      keywords="network circuit node mash analysis",
      license = "GPL 3.0 or later",
      python_requires='>=3.6',
      url = "https://github.com/jrbainter/netana.git",
      )

