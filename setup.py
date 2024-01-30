#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-photometry/setup.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                11.12.2019
# Last Modified Date:  06.04.2023
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from setuptools import find_namespace_packages, setup

setup(
	name='ampel-photometry',
	version='0.9.0',
	packages=find_namespace_packages(),
	package_data = {
		'': ['py.typed'],
		'conf': [
			'*.json', '**/*.json', '**/**/*.json',
			'*.yaml', '**/*.yaml', '**/**/*.yaml',
			'*.yml', '**/*.yml', '**/**/*.yml'
		]
	},
	zip_safe = False,
	install_requires = [
		"ampel-interface",
		"ampel-core",
	],
)
