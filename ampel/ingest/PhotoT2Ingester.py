#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-photometry/ampel/ingest/PhotoT2Ingester.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 14.12.2017
# Last Modified Date: 11.02.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from time import time
from pymongo import UpdateOne
from typing import Dict, Any, Union, Tuple, List

from ampel.type import StockId, ChannelId
from ampel.util.collections import try_reduce
from ampel.enum.T2SysRunState import T2SysRunState
from ampel.content.PhotoT2Document import PhotoT2Document
from ampel.abstract.ingest.AbsT2Ingester import AbsT2Ingester
from ampel.abstract.ingest.AbsStateT2Ingester import AbsStateT2Ingester
from ampel.abstract.ingest.AbsStateT2Compiler import AbsStateT2Compiler
from ampel.ingest.PhotoCompoundBluePrint import PhotoCompoundBluePrint
from ampel.ingest.compile.PhotoT2Compiler import PhotoT2Compiler


class PhotoT2Ingester(AbsStateT2Ingester):

	# Defaults override
	compiler: AbsStateT2Compiler[PhotoCompoundBluePrint] = PhotoT2Compiler()

	# AbsT2Ingester override. Value (possibly overriden by sublcass attrs or config)
	# is provied for each channel to the compiler via the method <compiler instance>.set_ingest_options(...)
	default_ingest_config: Dict[str, Any] = {"upper_limits": False}


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
				# 'link' is added below
			}

			# Attributes set if no previous doc exists
			set_on_insert: PhotoT2Document = {
				'unit': t2_id,
				'config': run_config,
				'stock': stock_id,
				'status': T2SysRunState.NEW.value
			}

			if self.tags:
				set_on_insert['tag'] = self.tags

			jchan, chan_add_to_set = AbsT2Ingester.build_query_parts(chans)
			add_to_set: Dict[str, Any] = {'channel': chan_add_to_set}

			# A T2 ignoring upper limits is T2s that can be linked with multiple compounds
			# (link_id contains the 'photopoint compound id' and the effective id)
			if isinstance(link_id, tuple):

				# Note: link_id[0] is always is the pp id
				match_dict['ppsid'] = link_id[0]
				set_on_insert['ppsid'] = link_id[0]
				add_to_set['link'] = {'$each': list(link_id[1:])}

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
					for eff_id in link_id[1:]
				]

				# Update journal: register pp id common to all channels
				journal_entries.insert(
					0, {
						'tier': self.tier,
						'dt': now,
						'run': self.run_id,
						'channel': jchan,
						'pp': link_id[0]
					}
				)

				# Update journal
				add_to_set['journal'] = {'$each': journal_entries}

			# T2 doc referencing a single compound id (link_id is then an 'effective compound id')
			else:

				# $elemMatch is needed -> See https://jira.mongodb.org/browse/SERVER-3946
				match_dict['link'] = {"$elemMatch": {"$eq": link_id}}
				add_to_set['link'] = link_id

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
