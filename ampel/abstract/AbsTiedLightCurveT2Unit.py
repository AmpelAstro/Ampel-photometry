#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-photometry/ampel/abstract/AbsTiedLightCurveT2Unit.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 11.03.2020
# Last Modified Date: 08.06.2020
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Sequence
from ampel.base import abstractmethod
from ampel.type import T2UnitResult
from ampel.view.LightCurve import LightCurve
from ampel.content.T2Record import T2Record
from ampel.abstract.AbsTiedCustomStateT2Unit import AbsTiedCustomStateT2Unit


class AbsTiedLightCurveT2Unit(AbsTiedCustomStateT2Unit[LightCurve], abstract=True):

	@abstractmethod
	def run(self, # type: ignore
		light_curve: LightCurve, t2_records: Sequence[T2Record]
	) -> T2UnitResult:
		"""
		Returned object should contain computed science results to be saved into the DB.
		Notes: dict must have only string keys and values must be bson encodable
		"""
