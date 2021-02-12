#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-photometry/ampel/ingest/PhotoCompoundIngester.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 14.12.2017
# Last Modified Date: 02.06.2020
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from time import time
from pymongo import UpdateOne
from typing import Sequence, List, Tuple, Union, Set, Optional
from ampel.type import StockId, ChannelId
from ampel.log.AmpelLogger import AmpelLogger, INFO
from ampel.log.handlers.RecordBufferingHandler import RecordBufferingHandler
from ampel.content.PhotoCompound import PhotoCompound
from ampel.content.DataPoint import DataPoint
from ampel.abstract.ingest.AbsCompoundIngester import AbsCompoundIngester
from ampel.abstract.AbsT1Unit import AbsT1Unit
from ampel.model.UnitModel import UnitModel
from ampel.ingest.PhotoCompoundBluePrint import PhotoCompoundBluePrint


class PhotoCompoundIngester(AbsCompoundIngester[PhotoCompoundBluePrint]):

	combiner: Union[UnitModel, str]
	channels: Set[ChannelId] = set()


	def __init__(self, **kwargs) -> None:

		super().__init__(**kwargs)

		# This ingester uses a T1 unit underneath, which requires a logger
		# like every other base units. We create a logger associated a
		# buffering handlers whose logs are later transfered to the
		# LogsBufferDict instance (self.logd) used and shared among ingesters
		logger = AmpelLogger.get_logger(console=False)
		self.rbh = RecordBufferingHandler(level=INFO)
		self.rec_buffer = self.rbh.buffer
		logger.addHandler(self.rbh)

		self.engine = self.context.loader.new_base_unit(
			unit_model = self.combiner if isinstance(self.combiner, UnitModel)
				else UnitModel(unit=self.combiner),
			logger = logger, sub_type = AbsT1Unit[PhotoCompoundBluePrint]
		)


	def add_channel(self, channel: ChannelId):
		self.channels.add(channel)


	def ingest(self,
		stock_id: StockId,
		datapoints: Sequence[DataPoint],
		chan_selection: List[Tuple[ChannelId, Union[bool, int]]]
	) -> Optional[PhotoCompoundBluePrint]:
		"""
		This method is called by the AlertProcessor for alerts
		passing at least one T0 channel filter
		"""

		# Keep only channels requiring the creation of 'states'
		chans = [k for k, v in chan_selection if k in self.channels]

		# Compute 'compound blueprint' (used for creating compounds and t2 docs)
		blue_print = self.engine.combine(stock_id, datapoints, chans)

		if self.rec_buffer:
			self.log_records_to_logd(self.rbh)

		if blue_print is None:
			return None

		# See how many different eff_comp_id were generated (possibly a single one)
		# and generate corresponding ampel document to be inserted later
		for eff_comp_id in blue_print.get_effids_for_chans(chans):

			d_addtoset = {
				'channel': {
					'$each': list(
						blue_print.get_chans_with_effid(eff_comp_id)
					)
				},
				'run': self.run_id
			}

			if blue_print.has_flavors(eff_comp_id):
				d_addtoset['flavor'] = {
					'$each': blue_print.get_compound_flavors(eff_comp_id)
				}

			comp_dict = blue_print.get_eff_compound(eff_comp_id)
			pp_comp_id = blue_print.get_ppsid_of_effid(eff_comp_id)

			comp_set_on_ins: PhotoCompound = {
				'_id': eff_comp_id,
				'stock': stock_id,
				'tag': list(blue_print.get_comp_tags(eff_comp_id)),
				'tier': 0,
				'added': time(),
				'lastjd': datapoints[0]['body']['jd'],
				'len': len(comp_dict),
				'body': comp_dict
			}

			if pp_comp_id != eff_comp_id:
				comp_set_on_ins['ppsid'] = pp_comp_id

			self.updates_buffer.add_t1_update(
				UpdateOne(
					{'_id': eff_comp_id},
					{
						'$setOnInsert': comp_set_on_ins,
						'$addToSet': d_addtoset
					},
					upsert=True
				)
			)

		return blue_print
