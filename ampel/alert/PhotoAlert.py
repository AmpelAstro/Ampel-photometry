#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-photometry/ampel/alert/PhotoAlert.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 14.12.2017
# Last Modified Date: 25.05.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Dict, Tuple, List, Sequence, Optional, Any, Literal, Union
from ampel.types import StockId
from ampel.alert.AmpelAlert import AmpelAlert, osa
from ampel.view.ReadOnlyDict import ReadOnlyDict


class PhotoAlert(AmpelAlert):
	"""
	Class with two collections (photopoints and upperlimits) of read-only dicts.
	The ampel AlertConsumer (repository Ampel-alerts) typically instantiates this class and feed T0 filters with it.

	.. note:: an alert must contain at least one photopoint
	"""

	__slots__ = 'pps', 'uls', 'name', 'data'

	pps: Sequence[ReadOnlyDict] #: photopoints (positive detections)
	uls: Optional[Sequence[ReadOnlyDict]] #: upper limits
	name: Optional[str] #: transient name
	data: Dict[str, Sequence[ReadOnlyDict]]

	def __init__(self,
		id: Union[int, str], stock_id: StockId,
		dps: Sequence[Dict],
		pps: Sequence[ReadOnlyDict],
		uls: Optional[Sequence[ReadOnlyDict]],
		name: Optional[str] = None
	) -> None:

		osa(self, 'id', id)
		osa(self, 'stock_id', stock_id)
		osa(self, 'dps', dps)
		osa(self, 'pps', pps)
		osa(self, 'uls', uls)
		osa(self, 'name', name)
		osa(self, 'data', {'pps': self.pps, 'uls': self.uls, 'all': self.dps})


	def __reduce__(self):
		return (type(self), (self.id, self.stock_id, self.dps, self.pps, self.uls, self.name))


	def get_values(self, # type: ignore[override]
		param_name: str,
		filters: Optional[Sequence[Dict[str, Any]]] = None,
		data: Literal['pps', 'uls', 'all'] = 'pps'
	) -> List[Any]:
		""" ex: get_values("magpsf") """
		if seq := self.data[data]:
			return AmpelAlert.get_values(self, param_name, filters, seq)
		return []


	def get_tuples(self, # type: ignore[override]
		param1: str, param2: str,
		filters: Optional[Sequence[Dict[str, Any]]] = None,
		data: Literal['pps', 'uls', 'all'] = "pps"
	) -> List[Tuple[Any, Any]]:
		""" ex: get_tuples("jd", "magpsf") """
		if seq := self.data[data]:
			return AmpelAlert.get_tuples(self, param1, param2, filters, seq)
		return []


	def get_ntuples(self, # type: ignore[override]
		params: List[str],
		filters: Optional[Sequence[Dict[str, Any]]] = None,
		data: Literal['pps', 'uls', 'all'] = "pps"
	) -> List[Tuple]:
		""" ex: get_ntuples(["fid", "jd", "magpsf"]) """
		if seq := self.data[data]:
			return AmpelAlert.get_ntuples(self, params, filters, seq)
		return []


	def get_photopoints(self) -> Sequence[ReadOnlyDict]:
		return self.pps


	def get_upperlimits(self) -> Optional[Sequence[ReadOnlyDict]]:
		return self.uls


	def is_new(self) -> bool:
		return len(self.pps) == 1


	def dict(self) -> Dict:
		return {
			'id': self.id, 'stock_id': self.stock_id,
			'pps': self.pps, 'uls': self.uls, 'name': self.name
		}
