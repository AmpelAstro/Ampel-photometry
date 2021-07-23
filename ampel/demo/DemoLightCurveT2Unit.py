#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-photometry/ampel/demo/DemoLightCurveT2Unit.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 07.08.2020
# Last Modified Date: 30.05.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from time import time
from typing import Union
from ampel.types import UBson
from ampel.struct.UnitResult import UnitResult
from ampel.abstract.AbsLightCurveT2Unit import AbsLightCurveT2Unit
from ampel.view.LightCurve import LightCurve


class DemoLightCurveT2Unit(AbsLightCurveT2Unit):

	test_parameter: int = 0

	def process(self, lightcurve: LightCurve) -> Union[UBson, UnitResult]:
		return {
			"id": lightcurve.get_values("jd"),
			"time": time(),
			"test_parameter": self.test_parameter
		}
