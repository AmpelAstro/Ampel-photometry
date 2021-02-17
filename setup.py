#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-photometry/setup.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 11.12.2019
# Last Modified Date: 28.01.2020
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from setuptools import setup, find_namespace_packages

import version_query

setup(
	name='ampel-photometry',
	version=version_query.predict_version_str(),
	packages=find_namespace_packages(),
	package_data = {
		'': ['py.typed'],
		'conf': [
			'*.json', '**/*.json', '**/**/*.json',
			'*.yaml', '**/*.yaml', '**/**/*.yaml',
			'*.yml', '**/*.yml', '**/**/*.yml'
		]
	},
	zip_safe=False,
	install_requires = [
		"ampel-interface",
		"ampel-core",
	],
	extras_require = {
		"testing": [
			"pytest"
		],
	},
)
