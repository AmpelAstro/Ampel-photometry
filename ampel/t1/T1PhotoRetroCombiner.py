#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-photometry/ampel/t1/T1PhotoRetroCombiner.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                25.05.2021
# Last Modified Date:  25.05.2021
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from typing import Generator
from ampel.content.DataPoint import DataPoint
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

	def generate_retro_sequences(self, datapoints: list[DataPoint]) -> Generator[list[DataPointId], None, None]:
		while datapoints:
			yield [dp["id"] for dp in datapoints]
			# trim the list at the next most recent detection (positive id)
			for i in range(len(datapoints)-2, -1, -1):
				if datapoints[i]["id"] > 0:
					datapoints = datapoints[:i+1]
					break
			else:
				break
