#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-photometry/ampel/ingest/PhotoCompoundBluePrint.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 01.01.2018
# Last Modified Date: 04.03.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Set, Dict
from ampel.type import ChannelId, StrictIterable
from ampel.ingest.CompoundBluePrint import CompoundBluePrint


class PhotoCompoundBluePrint(CompoundBluePrint):
	"""
	Instance members of this class are typically set/updated by PhotoCompoundBluePrintGenerator
	Abbreviations used in this class:
	"eid": effective id, "chan": channel name, "comp": compound
	"""

	# save channels names using pp id as key
	d_ppsid_chnames: Dict[bytes, Set[ChannelId]]

	# save eid <-> ppsid association
	d_eid_ppsid: Dict[bytes, bytes]


	def __init__(self):
		super().__init__()
		self.d_ppsid_chnames = {}
		self.d_eid_ppsid = {}


	def get_ppsids_of_chans(self, chan_names: StrictIterable[ChannelId]) -> Set[bytes]:

		pps_ids = set()
		for chan_name in chan_names:
			for eid in self.d_ppsid_chnames.keys():
				if chan_name in self.d_ppsid_chnames[eid]:
					pps_ids.add(eid)
					break
		return pps_ids


	def get_ppsid_of_effid(self, eff_comp_id: bytes) -> bytes:
		return self.d_eid_ppsid[eff_comp_id]


	def get_chans_with_ppsid(self, pps_id: bytes) -> Set[ChannelId]:
		return self.d_ppsid_chnames[pps_id]
