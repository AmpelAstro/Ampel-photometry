#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-photometry/ampel/abstract/AbsLightCurveT2Unit.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                13.12.2017
# Last Modified Date:  01.03.2020
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from collections.abc import Iterable

from ampel.abstract.AbsCustomStateT2Unit import AbsCustomStateT2Unit
from ampel.content.DataPoint import DataPoint
from ampel.content.T1Document import T1Document
from ampel.view.LightCurve import LightCurve


class AbsLightCurveT2Unit(AbsCustomStateT2Unit[LightCurve], abstract=True):
	"""
	Base class for T2s that operate on light curves.
	"""

	@staticmethod
	def build(compound: T1Document, datapoints: Iterable[DataPoint]) -> LightCurve:
		return LightCurve.build(compound, datapoints)
