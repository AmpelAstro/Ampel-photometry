#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-photometry/ampel/ingest/compile/DualPointT2Compiler.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 14.12.2017
# Last Modified Date: 24.02.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import List, Dict, Set, Union, Sequence, Any, Literal, Tuple, Optional
from ampel.content.DataPoint import DataPoint
from ampel.type import ChannelId, DataPointId
from ampel.model.ingest.T2IngestModel import T2IngestModel
from ampel.ingest.compile.PointT2Compiler import PointT2Compiler


class DualPointT2Compiler(PointT2Compiler):
	"""
	Helper class capabable of generating a nested dict that is used as basis to create T2 documents.
	The generated structure is optimized: multiple T2 documents associated with the same datapoint
	accross different channels are merged into one single T2 document
	that references all corrsponding channels.
	"""

	def __init__(self) -> None:
		super().__init__()
		self.dual_slices: Dict[Tuple[ChannelId, str, Optional[int]], Dict[bool, List[slice]]] = {}


	def set_ingest_options(self,
		channel: ChannelId, model: T2IngestModel, options: Optional[Dict[str, Any]]
	) -> None:

		try:

			if not options:
				super().set_ingest_options(channel, model, {})
				return

			if 'all' in options['eligible']:
				super().set_ingest_options(
					channel, model, {'eligible': options['eligible']['all']}
				)

			for k in ('pps', 'uls'):
				if k in options['eligible']:
					self.set_special_options(
						channel, model, options['eligible'][k], k == 'uls'
					)
		except Exception as e:
			print("Error adding ingest config")
			print(f"model: {model}")
			print(f"options: {options}")
			raise e


	def set_special_options(self,
		chan: ChannelId,
		model: T2IngestModel,
		slice_arg: Union[Literal['first', 'last'], Tuple[int, int, int]],
		upper_limit: bool
	):

		s = self.get_slice(slice_arg)
		k = (chan, model.unit_id, model.config)

		if k not in self.dual_slices:
			self.dual_slices[k] = {}

		if upper_limit in self.dual_slices[k]:
			# Avoid duplicated slices from bad config
			for el in self.dual_slices[k][upper_limit]:
				if s.__reduce__()[1] == el.__reduce__()[1]:
					return
			self.dual_slices[k][upper_limit].append(s)
		else:
			self.dual_slices[k][upper_limit] = [s]


	def compile(self,
		chan_selection: List[Tuple[ChannelId, Union[bool, int]]],
		datapoints: Sequence[DataPoint]
	) -> Dict[Tuple[str, Optional[int], DataPointId], Set[ChannelId]]:
		"""
		TLDR: This function computes and returns a dict structure helpful for creating T2 docs.
		This computation is required since:
		* A given alert can be accepted by one filter and be rejected by the other
		* T0 filters can return a customized set of T2 units to be run (group id)
		----------------------------------------------------------------------------------

		:param chan_selection: example: {"CHAN_SN": True, "CHAN_GRB": 1, "CHAN_BH": None}
		CHANNEL_SN accepted the alert and requests all associated T2s to be created
		CHANNEL_GRB accepted the alert and requests only T2s with group ID 1 to be created
		CHANNEL_BH rejected the alert

		This method will create the following dict:
		{
			(SNCOSMO, 123, 456): {"CHANNEL_SN"},
			(PHOTO_Z, 487, 2336): {"CHANNEL_SN", "CHANNEL_GRB"}
		}

		Dict key element 1: unit id
		Dict key element 2: hashed dict value of the T2's init config dict (123)
		Dict key element 3: datapoint id
		Dict values: set of channel ids
		"""

		t2s_eff: Dict[Tuple[str, Optional[int], DataPointId], Set[ChannelId]] = {}
		datapoints = list(datapoints)

		for chan, ingest_model in self.get_ingest_models(chan_selection):

			t2_id = ingest_model.unit_id
			config = ingest_model.config
			sk = (chan, t2_id, config)

			if sk in self.slices:
				for s in self.slices[sk]:
					for dp in datapoints[s]:
						k = (t2_id, config, dp['_id'])
						if k not in t2s_eff:
							t2s_eff[k] = {chan}
						else:
							t2s_eff[k].add(chan)

			if sk in self.dual_slices:

				ds = self.dual_slices[sk]

				# Upper limit
				if True in ds:

					if "uls" not in locals():
						uls = [dp for dp in datapoints if dp['_id'] < 0]

					for s in ds[True]:
						for dp in uls[s]:
							k = (t2_id, config, dp['_id'])
							if k not in t2s_eff:
								t2s_eff[k] = {chan}
							else:
								t2s_eff[k].add(chan)

				# Photo point
				if False in ds:

					if "pps" not in locals():
						pps = [dp for dp in datapoints if dp['_id'] > 0]

					for s in ds[False]:
						for dp in pps[s]:
							k = (t2_id, config, dp['_id'])
							if k not in t2s_eff:
								t2s_eff[k] = {chan}
							else:
								t2s_eff[k].add(chan)

		return t2s_eff
