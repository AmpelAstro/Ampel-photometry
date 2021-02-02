#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-photometry/ampel/abstract/AbsTiedLightCurveT2Unit.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 11.03.2020
# Last Modified Date: 08.06.2020
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Sequence, ClassVar, Dict, Any
from ampel.base import abstractmethod
from ampel.type import T2UnitResult
from ampel.view.LightCurve import LightCurve
from ampel.content.T2Record import T2Record
from ampel.abstract.AbsTiedCustomStateT2Unit import AbsTiedCustomStateT2Unit

from ampel.content.Compound import Compound
from ampel.content.DataPoint import DataPoint

class AbsTiedLightCurveT2Unit(AbsTiedCustomStateT2Unit[LightCurve], abstract=True):


	# Just as for AbsLightCurveT2Unit we set the default class behaviour
	# Deactivating upper limits cause each T2 doc to have multiple links
	# and possibly uintended 
	#: 
	#: upper_limits:
	#:   - True: compound id computed using photopoint & upperlimit ids
	#:   - False: compound id computed using photopoint ids only
	ingest: ClassVar[Dict[str, Any]] = {'upper_limits': True}



	@abstractmethod
	def run(self, # type: ignore
		light_curve: LightCurve, t2_records: Sequence[T2Record]
	) -> T2UnitResult:
		"""
		Returned object should contain computed science results to be saved into the DB.
		Notes: dict must have only string keys and values must be bson encodable
		"""

	@staticmethod
	def build(compound: Compound, datapoints: Sequence[DataPoint]) -> LightCurve:
		return LightCurve.build(compound, datapoints)
