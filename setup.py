#!/usr/bin/env python3

from setuptools import setup, find_packages
""" This file is used to build the 'NetAna' distrubtion.
    All files in 'examples' directory and all files defined in the MANFEST.in
    template file. """
setup(name='netana',
      version = '3.1.18',
      zip_safe=True,
      packages=find_packages(),
      include_package_data = True,
      install_requires = ['python3-matplotlib','python3-numpy'],
      entry_points = { 'gui_scripts' : [ 'netana = startnetana.__main__: main' ] },
      scripts = ["cp-examples.sh"],
      package_data={'netana': ['examples/*', 'doc/*'],
        "" : ['netana-3.1.18-md5sums', 'netana.desktop', 'license', 'change.log']},
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

