#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-photometry/ampel/abstract/AbsTiedLightCurveT2Unit.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 11.03.2020
# Last Modified Date: 11.02.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Iterable, ClassVar, Dict, Any, Sequence, Union, Optional, Literal
from ampel.base import abstractmethod
from ampel.type import T2UnitResult
from ampel.view.LightCurve import LightCurve
from ampel.content.Compound import Compound
from ampel.content.DataPoint import DataPoint
from ampel.view.T2DocView import T2DocView
from ampel.abstract.AbsTiedCustomStateT2Unit import AbsTiedCustomStateT2Unit


class AbsTiedLightCurveT2Unit(AbsTiedCustomStateT2Unit[LightCurve], abstract=True):

	#: Default class ingest option for upper_limits:
	#:   - True: compound id computed using photopoint & upperlimit ids
	#:   - False: compound id computed using photopoint ids only
	ingest: ClassVar[Dict[str, Any]] = {'upper_limits': True}


	@abstractmethod
	def run(self, light_curve: LightCurve, t2_views: Sequence[T2DocView]) -> T2UnitResult:
		"""
		Returned object should contain computed science results to be saved into the DB.
		Notes: dict must have only string keys and values must be bson encodable
		"""


	@staticmethod
	def get_link(
		link_override: Dict[Literal['pps', 'uls'], Literal['first', 'middle', 'last']],
		light_curve: LightCurve
	) -> Optional[Union[int, bytes]]:
		"""
		Method used by T2Processor.
		:param link_override: value associated with key 'link_override' of `T2Dependency <ampel.struct.T2Dependency.T2Dependency>`
		:returns: the value of 'link' (tied t2 documents) to be matched
		"""

		if 'pps' in link_override:
			dps = light_curve.photopoints
			v = link_override['pps']
		elif 'uls' in link_override:
			dps = light_curve.upperlimits
			v = link_override['uls']
		else:
			raise ValueError("Invalid key in link_override")

		if v == 'first':
			return dps[0]['_id'] if dps else None
		elif v == 'middle':
			return dps[len(dps) // 2]['_id'] if dps else None
		elif v == 'last':
			return dps[-1]['_id'] if dps else None
		else:
			raise ValueError("Invalid value in link_override specs")


	@staticmethod
	def build(compound: Compound, datapoints: Iterable[DataPoint]) -> LightCurve:
		return LightCurve.build(compound, datapoints)
