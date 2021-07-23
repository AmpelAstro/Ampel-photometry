#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-photometry/ampel/abstract/AbsLightCurveT2Unit.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 13.12.2017
# Last Modified Date: 01.03.2020
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Iterable
from ampel.view.LightCurve import LightCurve
from ampel.content.T1Document import T1Document
from ampel.content.DataPoint import DataPoint
from ampel.abstract.AbsCustomStateT2Unit import AbsCustomStateT2Unit


class AbsLightCurveT2Unit(AbsCustomStateT2Unit[LightCurve], abstract=True):
	"""
	Base class for T2s that operate on light curves.
	"""

	@staticmethod
	def build(compound: T1Document, datapoints: Iterable[DataPoint]) -> LightCurve:
		return LightCurve.build(compound, datapoints)
