#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-photometry/ampel/demo/unit/base/DemoLightCurveT2Unit.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 07.08.2020
# Last Modified Date: 07.08.2020
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from time import time
from typing import Sequence, List
from ampel.type import T2UnitResult
from ampel.content.T2Record import T2Record
from ampel.abstract.AbsTiedLightCurveT2Unit import AbsTiedLightCurveT2Unit
from ampel.view.LightCurve import LightCurve


class DemoTiedLightCurveT2Unit(AbsTiedLightCurveT2Unit):

	test_parameter: int = 0

	def get_tied_unit_names(self) -> List[str]:
		return ["DemoPointT2Unit"]

	def run(self, lightcurve: LightCurve, t2_records: Sequence[T2Record]) -> T2UnitResult:
		return {
			"id": lightcurve.get_values("jd"),
			"time": time(),
			"linked_records": t2_records,
			"test_parameter": self.test_parameter
		}
