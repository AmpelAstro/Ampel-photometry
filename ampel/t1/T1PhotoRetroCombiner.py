#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-photometry/ampel/t1/T1PhotoRetroCombiner.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 25.05.2021
# Last Modified Date: 25.05.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Optional, List
from ampel.types import DataPointId
from ampel.t1.T1SimpleRetroCombiner import T1SimpleRetroCombiner


class T1PhotoRetroCombiner(T1SimpleRetroCombiner):
	"""
	combine(
		[
			{'_id': 12}, {'_id': -11}, {'_id': 10}, {'_id': -8},
			{'_id': -7}, {'_id': 6}, {'_id': -4}
		]
	)
	will yield [
		[12, -11, 10, -8, -7, 6, -4],
		[10, -8, -7, 6, -4],
	  	[6, -4]
	]
	"""

	def _prev_det_seq(self, datapoints: List[DataPointId]) -> Optional[List[DataPointId]]:

		for i in range(1, len(datapoints)):
			if datapoints[-(i+1)] > 0:
				return datapoints[:-i]

		return None
