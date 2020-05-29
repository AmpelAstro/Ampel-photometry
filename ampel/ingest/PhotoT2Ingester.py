#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-photometry/ampel/ingest/PhotoT2Ingester.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 14.12.2017
# Last Modified Date: 30.04.2020
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from time import time
from pymongo import UpdateOne
from typing import Dict, Any, Union, Tuple, List

from ampel.type import StockId, ChannelId
from ampel.util.collections import try_reduce
from ampel.t2.T2RunState import T2RunState
from ampel.content.T2Record import T2Record
from ampel.abstract.ingest.AbsT2Ingester import AbsT2Ingester
from ampel.abstract.ingest.AbsStateT2Ingester import AbsStateT2Ingester
from ampel.abstract.ingest.AbsStateT2Compiler import AbsStateT2Compiler
from ampel.ingest.PhotoCompoundBluePrint import PhotoCompoundBluePrint
from ampel.ingest.compile.PhotoT2Compiler import PhotoT2Compiler


class PhotoT2Ingester(AbsStateT2Ingester):

	# Defaults override
	compiler: AbsStateT2Compiler[PhotoCompoundBluePrint] = PhotoT2Compiler()
	default_options: Dict[str, Any] = {"upper_limits": False}


	def ingest(self, # type: ignore[override]
		stock_id: StockId,
		comp_bp: PhotoCompoundBluePrint,
		chan_selection: List[Tuple[ChannelId, Union[bool, int]]]
	) -> None:

		optimized_t2s = self.compiler.compile(chan_selection, comp_bp)
		now = int(time())

		# Loop over t2 units to be created
		for (t2_id, run_config, link_id), chans in optimized_t2s.items():

			# Matching search criteria
			match_dict: Dict[str, Any] = {
				'stock': stock_id,
				'unit': t2_id,
				'config': run_config
			}

			# Attributes set if no previous doc exists
			set_on_insert: T2Record = {
				'stock': stock_id,
				'tag': self.tags,
				'unit': t2_id,
				'config': run_config,
				'status': T2RunState.TO_RUN.value
			}

			jchan, chan_add_to_set = AbsT2Ingester.build_query_parts(chans)
			add_to_set: Dict[str, Any] = {'channel': chan_add_to_set}

			# A T2 not using upper limits is T2s that can be linked with multiple compounds
			# (link_id contains the 'photopoint compound id' and the effective id)
			if isinstance(link_id, tuple):

				llink_id = list(link_id)

				# match_dict['link'] = bifold_comp_id or
				# match_dict['link'] = {'$in': [bifold_comp_id]}
				# triggers the error: 'Cannot apply $addToSet to non-array field. \
				# Field named 'link' has non-array type string'
				# -> See https://jira.mongodb.org/browse/SERVER-3946

				# First llink_id is always is the pp id
				match_dict['link'] = llink_id[0]
				add_to_set['link'] = {'$each': llink_id}

				# Update journal: register eff id for each channel
				journal_entries = [
					{
						'tier': self.tier,
						'dt': now,
						'run': self.run_id,
						'channel': try_reduce(
							list(comp_bp.get_chans_with_effid(eff_id))
						),
						'eff': eff_id
					}
					for eff_id in llink_id[1:]
				]

				# Update journal: register pp id common to all channels
				journal_entries.insert(
					0, {
						'tier': self.tier,
						'dt': now,
						'run': self.run_id,
						'channel': jchan,
						'pp': llink_id[0]
					}
				)

				# Update journal
				add_to_set['journal'] = {'$each': journal_entries}

			# T2 doc referencing a single compound id
			# bifold_comp_id is then an 'effective compound id'
			else:

				match_dict['link'] = link_id

				# list is required for later $addToSet operations to succeed
				set_on_insert['link'] = [link_id]

				# Update journal
				add_to_set['journal'] = {
					'tier': self.tier,
					'dt': now,
					'channel': jchan
				}

			# Append update operation to bulk list
			self.updates_buffer.add_t2_update(
				UpdateOne(
					match_dict,
					{
						'$setOnInsert': set_on_insert,
						'$addToSet': add_to_set
					},
					upsert=True
				)
			)
