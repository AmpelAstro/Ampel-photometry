#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-photometry/ampel/abstract/AbsLightCurveT2Unit.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 13.12.2017
# Last Modified Date: 01.03.2020
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Iterable, ClassVar, Dict, Any
from ampel.view.LightCurve import LightCurve
from ampel.content.Compound import Compound
from ampel.content.DataPoint import DataPoint
from ampel.abstract.AbsCustomStateT2Unit import AbsCustomStateT2Unit


class AbsLightCurveT2Unit(AbsCustomStateT2Unit[LightCurve], abstract=True):
	"""
	upper_limits:
	-> True: compound id computed using PPs & ULs IDs
	-> False: compound id computed using PPs IDs only
	"""

	ingest: ClassVar[Dict[str, Any]] = {'upper_limits': True}


	@staticmethod
	def build(compound: Compound, datapoints: Iterable[DataPoint]) -> LightCurve:
		return LightCurve(
			compound_id = compound['_id'],
			tier = compound['tier'],
			added = compound['added'],
			photopoints = [el for el in datapoints if el['_id'] > 0],
			upperlimits = [el for el in datapoints if el['_id'] < 0]
		)
