#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-photometry/ampel/demo/DemoTiedLightCurveT2Unit.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 07.08.2020
# Last Modified Date: 04.04.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from time import time
from typing import Sequence, List, Union

from ampel.type import UBson
from ampel.struct.UnitResult import UnitResult
from ampel.enum.T2RecordCode import T2RecordCode
from ampel.view.T2DocView import T2DocView
from ampel.abstract.AbsTiedLightCurveT2Unit import AbsTiedLightCurveT2Unit
from ampel.view.LightCurve import LightCurve


class DemoTiedLightCurveT2Unit(AbsTiedLightCurveT2Unit):

	test_parameter: int = 0

	@classmethod
	def get_tied_unit_names(cls) -> List[str]:
		return ["DemoPointT2Unit"]

	def run(self, lightcurve: LightCurve, t2_views: Sequence[T2DocView]) -> Union[UBson, T2RecordCode, UnitResult[UBson]]:
		return {
			"jds": lightcurve.get_values("jd"),
			"time": time(),
			"linked_views": [el.serialize() for el in t2_views],
			"linked_results": [el.get_content() for el in t2_views],
			"test_parameter": self.test_parameter
		}
