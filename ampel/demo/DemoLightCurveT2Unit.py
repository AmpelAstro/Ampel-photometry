#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-photometry/ampel/demo/DemoLightCurveT2Unit.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                07.08.2020
# Last Modified Date:  30.05.2021
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from time import time

from ampel.abstract.AbsLightCurveT2Unit import AbsLightCurveT2Unit
from ampel.struct.UnitResult import UnitResult
from ampel.types import UBson
from ampel.view.LightCurve import LightCurve


class DemoLightCurveT2Unit(AbsLightCurveT2Unit):

	test_parameter: int = 0

	def process(self, lightcurve: LightCurve) -> UBson | UnitResult:
		return {
			"id": lightcurve.get_values("jd"),
			"time": time(),
			"test_parameter": self.test_parameter
		}
