#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-photometry/ampel/demo/unit/base/DemoLightCurveT2Unit.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 07.08.2020
# Last Modified Date: 07.08.2020
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from time import time
from typing import Dict, Any, ClassVar
from ampel.type import T2UnitResult
from ampel.abstract.AbsLightCurveT2Unit import AbsLightCurveT2Unit
from ampel.view.LightCurve import LightCurve


class DemoLightCurveCustomIngestT2Unit(AbsLightCurveT2Unit):

	test_parameter: int = 0
	ingest: ClassVar[Dict[str, Any]] = {'upper_limit': False}

	def run(self, lightcurve: LightCurve) -> T2UnitResult:
		return {
			"id": lightcurve.get_values("jd"),
			"time": time(),
			"test_parameter": self.test_parameter
		}
