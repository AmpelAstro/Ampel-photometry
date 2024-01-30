#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-photometry/ampel/aux/ULSFilter.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                05.05.2021
# Last Modified Date:  05.05.2021
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from ampel.abstract.AbsApplicable import AbsApplicable
from ampel.content.DataPoint import DataPoint


class ULSFilter(AbsApplicable):
	def apply(self, arg: list[DataPoint]) -> list[DataPoint]:
		return [el for el in arg if el['id'] < 0]
