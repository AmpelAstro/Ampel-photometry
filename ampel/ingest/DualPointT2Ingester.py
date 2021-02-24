#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-photometry/ampel/ingest/DualPointT2Ingester.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 23.03.2020
# Last Modified Date: 11.02.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from time import time
from pymongo import UpdateOne
from typing import Sequence, Dict, Optional, Union, Literal, Tuple, List

from ampel.type import StockId, ChannelId
from ampel.util.collections import try_reduce
from ampel.content.DataPoint import DataPoint
from ampel.enum.T2SysRunState import T2SysRunState
from ampel.abstract.ingest.AbsPointT2Ingester import AbsPointT2Ingester
from ampel.ingest.compile.PointT2Compiler import PointT2Compiler
from ampel.ingest.compile.DualPointT2Compiler import DualPointT2Compiler


class DualPointT2Ingester(AbsPointT2Ingester):

	compiler: PointT2Compiler = DualPointT2Compiler()
	default_ingest_config: Dict[ # type: ignore[misc]
		Literal['eligible'],
		Dict[
			Literal['all', 'pps', 'uls'],
			Optional[Union[Literal['first', 'last', 'all', Tuple[int, int, int]]]]
		]
	] = {} # Empty dict or None key means all eligible


	def ingest(self,
		stock_id: StockId,
		datapoints: Sequence[DataPoint],
		chan_selection: List[Tuple[ChannelId, Union[bool, int]]]
	) -> None:

		optimized_t2s = self.compiler.compile(chan_selection, datapoints)
		now = int(time())

		# Loop over t2 units to be created
		for (t2_id, run_config, link_id), chan_names in optimized_t2s.items():

			# Set of channel names
			eff_chan_names = list(chan_names) # pymongo requires list

			# Append update operation to bulk list
			self.updates_buffer.add_t2_update(
				UpdateOne(
					# Matching search criteria
					{
						'stock': stock_id,
						'unit': t2_id,
						'config': run_config,
						'link': link_id,
						'col': 't0'
					},
					{
						# Attributes set if no previous doc exists
						'$setOnInsert': {
							'stock': stock_id,
							'tag': self.tags,
							'unit': t2_id,
							'link': link_id,
							'config': run_config,
							'status': T2SysRunState.NEW.value,
							'col': 't0'
						},
						# Journal and channel update
						'$addToSet': {
							'channel': {'$each': eff_chan_names},
							'journal': {
								'tier': self.tier,
								'dt': now,
								'channel': try_reduce(eff_chan_names)
							}
						}
					},
					upsert=True
				)
			)
