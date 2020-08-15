#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-photometry/ampel/view/TransientView.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 13.01.2018
# Last Modified Date: 15.08.2020
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Optional, Sequence, Dict, Any

from ampel.type import StockId
from ampel.util.t1 import get_datapoint_ids
from ampel.content.DataPoint import DataPoint
from ampel.content.Compound import Compound
from ampel.content.T2Record import T2Record
from ampel.content.StockRecord import StockRecord
from ampel.content.LogRecord import LogRecord
from ampel.view.LightCurve import LightCurve
from ampel.view.SnapView import SnapView


class TransientView(SnapView):

	__slots__ = "lightcurve",

	def __init__(self,
		id: StockId,
		stock: Optional[StockRecord] = None,
		t0: Optional[Sequence[DataPoint]] = None,
		t1: Optional[Sequence[Compound]] = None,
		t2: Optional[Sequence[T2Record]] = None,
		log: Optional[Sequence[LogRecord]] = None,
		extra: Optional[Dict[str, Any]] = None,
		freeze: bool = True
	):
		if t0 and t1:
			self.lightcurve: Optional[Sequence[LightCurve]] = tuple(
				LightCurve.build(
					comp, tuple(el for el in t0 if el['_id'] in get_datapoint_ids(comp)),
				)
				for comp in t1
			)
		else:
			self.lightcurve = None

		self.stock = stock
		self.t0 = t0
		self.t1 = t1
		self.t2 = t2
		self.log = log
		self.extra = extra
		self.id = id
		self._frozen = freeze


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
