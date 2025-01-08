#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-photometry/ampel/demo/DemoTiedLightCurveT2Unit.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                07.08.2020
# Last Modified Date:  28.09.2021
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from collections.abc import Sequence
from time import time

from pydantic import TypeAdapter

from ampel.abstract.AbsTiedLightCurveT2Unit import AbsTiedLightCurveT2Unit
from ampel.struct.UnitResult import UnitResult
from ampel.types import UBson
from ampel.view.LightCurve import LightCurve
from ampel.view.T2DocView import T2DocView


class DemoTiedLightCurveT2Unit(AbsTiedLightCurveT2Unit):

	test_parameter: int = 0

	def process(self, lightcurve: LightCurve, t2_views: Sequence[T2DocView]) -> UBson | UnitResult:
		return {
			"jds": lightcurve.get_values("jd"),
			"time": time(),
			"linked_views": [serialize(el, mode="json") for el in t2_views],
			"linked_results": [el.get_payload() for el in t2_views],
			"test_parameter": self.test_parameter
		}

serialize = TypeAdapter(T2DocView).dump_python