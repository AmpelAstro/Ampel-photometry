#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-photometry/ampel/ingest/compile/PhotoT2Compiler.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 14.12.2017
# Last Modified Date: 19.11.2020
# Last Modified By  : Jakob van Santen <jakob.van.santen@desy.de>

from typing import Dict, Set, Any, Union, Tuple, List, Optional
from ampel.type import ChannelId
from ampel.model.ingest.T2IngestModel import T2IngestModel
from ampel.abstract.ingest.AbsStateT2Compiler import AbsStateT2Compiler
from ampel.ingest.PhotoCompoundBluePrint import PhotoCompoundBluePrint


class PhotoT2Compiler(AbsStateT2Compiler):
	"""
	Helper class capable of generating a nested dict that is used as basis to create T2 documents.
	The generated structure is optimized: multiple T2 documents associated with the same compound
	accross different channels are merged into one single T2 document
	that references all corrsponding channels.
	"""

	def __init__(self) -> None:
		super().__init__()
		self.upper_limits: Dict[Tuple[ChannelId, str, Optional[int]], bool] = {}


	def set_ingest_options(self,
		channel: ChannelId,
		model: T2IngestModel,
		options: Dict[str, Any]
	) -> None:
		k = (channel, model.unit_id, model.config)

		if k in self.upper_limits and self.upper_limits[k] != options["upper_limits"]:
			raise ValueError("Invalid config")

		self.upper_limits[k] = options["upper_limits"]


	def compile(self,
		chan_selection: List[Tuple[ChannelId, Union[bool, int]]],
		compound_blueprint: PhotoCompoundBluePrint
	) -> Dict[Tuple[str, Optional[int], Union[bytes, Tuple[bytes, ...]]], Set[ChannelId]]:
		"""
		TLDR: This function computes and returns a dict structure helpful for creating T2 docs.

		This computation is required since:
		  * A given alert can be accepted by one filter and be rejected by the other
		  * T0 filters can return a customized set of T2 units to be run (group id)
		  * An alert loaded by different channels can result in different compounds

		:param chan_selection:
		  example: ``{"CHANNEL_SN": True, "CHANNEL_GRB": 1, "CHANNEL_BH": None}``
		    * CHANNEL_SN accepted the alert and requests all associated T2s to be created
		    * CHANNEL_GRB accepted the alert and requests only T2s with group ID 1 to be created
		    * CHANNEL_BH rejected the alert

		Loop 1

		Say following T2s are requested by CHAN_SN and CHAN_GRB::
		  
		  {
		      "CHANNEL_SN": {"T2SNCosmo", "T2PhotoZ"},
		      "CHANNEL_GRB": {"T2GRBFit", "T2PhotoZ"}
		  }

		Loop 1 will create the following dict::
		  
		  {
		      ("T2SNCosmo", 123, True): {"CHANNEL_SN"}
		      ("T2PhotoZ", 123, False): {"CHANNEL_SN", "CHANNEL_GRB"}
		      ("T2GRBFit", 123, True): {"CHANNEL_GRB"}
		  }

		* Dict key 1st element: unit id
		* Dict key 2nd element: hashed dict value of the T2's init config dict (123)
		* Dict key 3rd element: whether upperlimits should be used to compute compound ids
		* Dict value: set of channel ids

		Loop 2

		Computes and returns a dict structure used for creating T2 docs.
		This loop replaces the value at depth 2 (bool) of the previously created dict
		by the computed compound ids (bytes) and thereby takes into account that an alert
		loaded by different channels can result in different compounds.

		Let's consider the example from the Loop 1 again (limited to PHOTO_Z with param 123 only)
		Loop 2 makes sure that CHANNEL_SN & CHANNEL_GRB are associated with the same compound
		(by checking compoundId equality), otherwise different t2 *docs* should be created. For example:
		
		* If compound ids differ between CHANNEL_SN & CHANNEL_GRB, *two* t2 docs will be created::
		    
		    {
		        ("T2PhotoZ", 123, a1b2c3d4): {"CHANNEL_SN"},
		        ("T2PhotoZ", 123, d4c3b2a1): {"CHANNEL_GRB"}
		    }
		* If compound ids are equal, *one* t2 doc will be created::
		    
		    {
		        ("T2PhotoZ", 123, a1b2c3d4): {"CHANNEL_SN", "CHANNEL_GRB"}
		    }
		"""

		fd: Dict[Tuple[str, Optional[int], bool], Set[ChannelId]] = {}

		# Loop 1
		########

		for chan, ingest_model in self.get_ingest_models(chan_selection):

			t2_id = ingest_model.unit_id
			config = ingest_model.config
			k = (
				t2_id,
				config,
				self.upper_limits[(chan, t2_id, config)]
			)

			if k in fd:
				fd[k].add(chan)
			else:
				fd[k] = {chan}



		t2s_eff: Dict[Tuple[str, Optional[int], Union[bytes, Tuple[bytes, ...]]], Set[ChannelId]] = {}

		# Loop 2
		########

		# Loop through loop 1 structure
		for (t2_id, config, ul), chans in fd.items():

			# Using PPS only (no upper limits).
			# The first element of doc_link will always be the PPS id
			if ul is False:

				links = compound_blueprint.get_ppsids_of_chans(chans)

				# Simple case: there is only one compound id for the current association of channels
				if len(links) == 1:
					# Link the T2 doc both the pps id and to the effective id
					t2s_eff[(t2_id, config, (*links, *compound_blueprint.get_effids_for_chans(chans)))] = chans

				else:
					# different channels have different compound id. The intersection (&) between
					# chan_names from loop 1 and the set of channels returned by CompoundGenerator
					# for a given compound_id must be computed
					for pp_id in links:
						sub_chans = compound_blueprint.get_chans_with_ppsid(pp_id) & chans
						t2s_eff[(t2_id, config, (pp_id, *compound_blueprint.get_effids_for_chans(sub_chans)))] = sub_chans

			# Using Upper limits
			else:

				links = compound_blueprint.get_effids_for_chans(chans)

				# Simple case: there is only one compound id for the current association of channels
				if len(links) == 1:
					t2s_eff[(t2_id, config, next(iter(links)))] = chans
				else:
					# different channels have different compound id. The intersection (&) between
					# chan_names from loop 1 and the set of channels returned by CompoundGenerator
					# for a given compound_id must be computed
					for link in links:
						t2s_eff[(t2_id, config, link)] = \
							compound_blueprint.get_chans_with_effid(link) & chans


		return t2s_eff

		# Output example:
		# {
		#	(PHOTO_Z, 123, a1b2c3d4): {CHANNEL_SN | CHANNEL_LEN | CHANNEL_5}
		#	(PHOTO_Z, 456, (a1b2c3d4, d4c3b2a1)): {CHANNEL_GRB}
		# }
