#!/usr/bin/env python3

import setuptools
""" This file is used to build the 'NetAna' distrubtion.
    All files in 'examples' directory and all files defined in the MANFEST.in
    template file. """
setuptools.setup(
      name='netana',
      version = '3.1.18',
      zip_safe=True,
      include_package_data = True,
      install_requires = ['matplotlib','numpy'],
      entry_points = { "gui_scripts" : ["netana = src.netana:main"] },
      scripts = ["cp-examples.sh"],
      package_data={'netana': ['examples/*', 'doc/*'],
        "" : ['netana-3.1.18-md5sums', 'netana.desktop', 'license', 'change.log']},
      author= 'James Bainter',
      maintainer= 'James Bainter',
      author_email= 'bainter8326@gmail.com',
      description= 'Electronic Network Analyzer',
      long_description= 'This program solves electronic AC & DC Mash and Node network equations using matrix algebra.',
      packages=setuptools.find_packages(),
      platforms= [ 'Linux', 'MSWindows' ],
      keywords="network circuit node mash analysis",
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent" ],
      url = "https://github.com/jrbainter/netana.git"
      )

