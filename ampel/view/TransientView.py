#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-photometry/ampel/view/TransientView.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 13.01.2018
# Last Modified Date: 15.08.2020
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Optional, Sequence
from ampel.util.t1 import get_datapoint_ids
from ampel.content.DataPoint import DataPoint
from ampel.view.LightCurve import LightCurve
from ampel.view.SnapView import SnapView


class TransientView(SnapView):

	__slots__ = "lightcurve",

	lightcurve: Optional[Sequence[LightCurve]]

	def __init__(self, *args, **kwargs) -> None:
		super().__init__(*args, **kwargs)

		if self.t0 and self.t1:
			lightcurve: Optional[Sequence[LightCurve]] = tuple(
				LightCurve.build(
					comp, tuple(el for el in self.t0 if el['_id'] in get_datapoint_ids(comp)),
				)
				for comp in self.t1
			)
		else:
			lightcurve = None
		object.__setattr__(self, "lightcurve", lightcurve)


	def get_photopoints(self) -> Optional[Sequence[DataPoint]]:

		if not self.t0:
			return None

		# By convention photopoints have positive int ids
		return [dp for dp in self.t0 if dp['_id'] > 0]


	def get_upperlimits(self) -> Optional[Sequence[DataPoint]]:

		if not self.t0:
			return None

		# By convention photopoints have negative int ids
		return [dp for dp in self.t0 if dp['_id'] < 0]


	def get_lightcurves(self) -> Optional[Sequence[LightCurve]]:
		return self.lightcurve
