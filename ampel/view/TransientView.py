#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-photometry/ampel/view/TransientView.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                13.01.2018
# Last Modified Date:  17.06.2021
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from ampel.view.LightCurve import LightCurve
from ampel.view.SnapView import SnapView

if TYPE_CHECKING:
	from collections.abc import Sequence

	from ampel.content.DataPoint import DataPoint


@dataclass(frozen=True)
class TransientView(SnapView):

	lightcurve: "None | Sequence[LightCurve]" = field(init=False)

	def __post_init__(self) -> None:

		if self.t0 and self.t1:
			lightcurve: None | Sequence[LightCurve] = tuple(
				LightCurve.build(comp, tuple(el for el in self.t0 if el['id'] in comp['dps']))
				for comp in self.t1
			)
		else:
			lightcurve = None
		object.__setattr__(self, "lightcurve", lightcurve)


	def get_photopoints(self) -> "None | Sequence[DataPoint]":

		if not self.t0:
			return None

		# By convention photopoints have positive int ids
		return [dp for dp in self.t0 if dp['id'] > 0]


	def get_upperlimits(self) -> "None | Sequence[DataPoint]":

		if not self.t0:
			return None

		# By convention photopoints have negative int ids
		return [dp for dp in self.t0 if dp['id'] < 0]


	def get_lightcurves(self) -> "None | Sequence[LightCurve]":
		return self.lightcurve
