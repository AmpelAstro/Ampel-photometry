#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-photometry/ampel/view/TransientView.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                13.01.2018
# Last Modified Date:  17.06.2021
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from typing import TYPE_CHECKING, Any

from ampel.view.LightCurve import LightCurve
from ampel.view.SnapView import SnapView

if TYPE_CHECKING:
	from collections.abc import Sequence

	from ampel.content.DataPoint import DataPoint
	from ampel.content.LogDocument import LogDocument
	from ampel.content.StockDocument import StockDocument
	from ampel.content.T1Document import T1Document
	from ampel.types import OneOrMany, StockId
	from ampel.view.T2DocView import T2DocView


class TransientView(SnapView):

	__slots__ = "lightcurve",

	lightcurve: "None | Sequence[LightCurve]"

	def __init__(
		self,
		id: "StockId",
		stock: "None | StockDocument" = None,
		origin: "None | OneOrMany[int]" = None,
		t0: "None | Sequence[DataPoint]" = None,
		t1: "None | Sequence[T1Document]" = None,
		t2: "None | Sequence[T2DocView]" = None,
		logs: "None | Sequence[LogDocument]" = None,
		extra: "None | dict[str, Any]" = None
	):
		super().__init__(id, stock=stock, origin=origin, t0=t0, t1=t1, t2=t2, logs=logs, extra=extra)

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
