#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-photometry/ampel/view/TransientView.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 13.01.2018
# Last Modified Date: 09.06.2020
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Optional, List
from ampel.content.DataPoint import DataPoint
from ampel.view.LightCurve import LightCurve
from ampel.view.SnapView import SnapView

class TransientView(SnapView):

	def get_photopoints(self) -> Optional[List[DataPoint]]:

		if not self.t0:
			return None

		# By convention photopoints have positive int ids
		return [dp for dp in self.t0 if dp['_id'] > 0]


	def get_upperlimits(self) -> Optional[List[DataPoint]]:

		if not self.t0:
			return None

		# By convention photopoints have negative int ids
		return [dp for dp in self.t0 if dp['_id'] < 0]


	def get_lightcurves(self) -> Optional[List[LightCurve]]:

		if not self.extra:
			return None

		return self.extra.get('lighcurve')
