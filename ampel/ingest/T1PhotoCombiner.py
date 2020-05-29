#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-photometry/ampel/ingest/T1PhotoCombiner.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 01.01.2018
# Last Modified Date: 18.03.2020
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

import hashlib
from typing import List, Union, ClassVar, Type
from ampel.type import ChannelId, DataPointId
from ampel.content.Compound import CompoundElement
from ampel.ingest.PhotoCompoundBluePrint import PhotoCompoundBluePrint
from ampel.ingest.T1DefaultCombiner import T1DefaultCombiner


class T1PhotoCombiner(T1DefaultCombiner[PhotoCompoundBluePrint]):
	"""
	Please see super class docstring for more info.
	Used abbreviations: "eid": effective id, "sid": strict id,
	"chan": channel name, "comp": compound
	"""

	BluePrintClass: ClassVar[Type] = PhotoCompoundBluePrint

	def combine_extra(self,
		blue_print: PhotoCompoundBluePrint, chan_name: ChannelId, eff_id: bytes,
		eff_comp: List[Union[DataPointId, CompoundElement]], eff_hash_payload: List[str]
	):
		""" Override of superclass """

		# first element of eff_hash_payload is str(Stock id)
		pp_hash_payload = eff_hash_payload[0]
		for i, el in enumerate(eff_comp, 1):
			if isinstance(el, dict):
				if el['id'] > 0:
					pp_hash_payload += eff_hash_payload[i]
			else:
				if el > 0:
					pp_hash_payload += eff_hash_payload[i]

		# pps_id = photopoints compound id = md5 hash of photopoins payload (without upper limits)
		pps_id: bytes = hashlib \
			.md5(bytes(pp_hash_payload, "utf-8")) \
			.digest()

		# Save channel name <-> pp comp id association
		if pps_id in blue_print.d_ppsid_chnames:
			blue_print.d_ppsid_chnames[pps_id].add(chan_name)
		else:
			blue_print.d_ppsid_chnames[pps_id] = {chan_name}

		# Save eid <-> ppid association
		blue_print.d_eid_ppsid[eff_id] = pps_id
