#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-photometry/ampel/aux/ULSFilter.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 05.05.2021
# Last Modified Date: 05.05.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import List
from ampel.abstract.AbsApplicable import AbsApplicable
from ampel.content.DataPoint import DataPoint

class ULSFilter(AbsApplicable):
	def apply(self, arg: List[DataPoint]) -> List[DataPoint]:
		return [el for el in arg if el['id'] < 0]
