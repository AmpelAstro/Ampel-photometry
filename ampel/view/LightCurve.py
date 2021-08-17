#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-photometry/ampel/view/LightCurve.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 13.01.2018
# Last Modified Date: 13.06.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

import operator
from dataclasses import dataclass
from typing import Sequence, Dict, Optional, List, Any, Tuple, Union, Callable, Iterable
from ampel.types import StockId
from ampel.content.T1Document import T1Document
from ampel.content.DataPoint import DataPoint

# Do not enable operator customizations by sub-classes for now
ops: Dict[str, Callable[[str, Any], bool]] = {
	'>': operator.gt,
	'<': operator.lt,
	'>=': operator.ge,
	'<=': operator.le,
	'==': operator.eq,
	'!=': operator.ne,
	'is': operator.is_,
	'is not': operator.is_not
}

@dataclass(frozen=True)
class LightCurve:
	"""
	Contains a collection of :class:`~ampel.content.DataPoint.DataPoint` (photo
	points and upper limits), and a few convenience methods to return values
	from internal collections.
	"""

	compound_id: int
	stock_id: Union[StockId, Sequence[StockId]]
	photopoints: Optional[Sequence[DataPoint]] = None
	upperlimits: Optional[Sequence[DataPoint]] = None


	@classmethod
	def build(cls, compound: T1Document, datapoints: Iterable[DataPoint]) -> 'LightCurve':
		return cls(
			compound_id = compound['link'],
			stock_id = compound['stock'],
			photopoints = [el for el in datapoints if el['id'] > 0],
			upperlimits = [el for el in datapoints if el['id'] < 0]
		)


	def __len__(self):
		return (len(self.photopoints) if self.photopoints else 0) + \
			(len(self.upperlimits) if self.upperlimits else 0)


	def get_values(self,
		key: str,
		filters: Optional[Union[Dict[str, Any], Sequence[Dict[str, Any]]]] = None,
		of_upper_limits: bool = False
	) -> Optional[List[Any]]:
		"""
		:param filters: filter criteria for data points, e.g. ``{'attribute': 'magpsf', 'operator': '<', 'value': 18}``
		:param of_upper_limits: return upper limits instead of photo points
		
		usage example::

			lightcurve.get_values('jd')
		
		.. seealso:: :func:`get_tuples`, :func:`get_ntuples`
		"""
		if datapoints := self._get_datapoints(filters, of_upper_limits):
			return [dp['body'][key] for dp in datapoints if key in dp['body']]
		return None


	def get_tuples(self,
		key1: str, key2: str,
		filters: Optional[Union[Dict[str, Any], Sequence[Dict[str, Any]]]] = None,
		of_upper_limits: bool = False
	) -> Optional[List[Tuple[Any, Any]]]:
		"""
		:param filters: filter criteria for datapoints
		:param of_upper_limits: return upper limits instead of photo points
		
		usage example::

			lightcurve.get_tuples('jd', 'magpsf', {'attribute': 'magpsf', 'operator': '<', 'value': 18})

		.. seealso:: :func:`get_values`, :func:`get_ntuples`
		"""
		if datapoints := self._get_datapoints(filters, of_upper_limits):
			return [
				(dp['body'][key1], dp['body'][key2]) for dp in datapoints
				if key1 in dp['body'] and key2 in dp['body']
			]
		return None


	def get_ntuples(self,
		params: Sequence[str],
		filters: Optional[Union[Dict[str, Any], Sequence[Dict[str, Any]]]] = None,
		of_upper_limits: bool = False
	) -> Optional[List[Tuple]]:
		"""
		:param params: list of keys
		:param filters: filter criteria for datapoints
		:param of_upper_limits: return upper limits instead of photo points
		
		usage example::

			lightcurve.get_ntuples(["fid", "jd", "magpsf"], {'attribute': 'magpsf', 'operator': '<', 'value': 18})

		.. seealso:: :func:`get_values`, :func:`get_tuples`
		"""
		if datapoints := self._get_datapoints(filters, of_upper_limits):
			return [
				tuple(dp['body'][param] for param in params)
				for dp in datapoints # type: ignore[union-attr]
				if all(dp['body'].get(param, False) for param in params)
			]
		return None


	def get_photopoints(self,
		filters: Optional[Union[Dict[str, Any], Sequence[Dict[str, Any]]]] = None
	) -> Optional[Sequence[DataPoint]]:
		"""Get (filtered) photo points"""
		if filters and self.photopoints:
			return self._apply_filter(self.photopoints, filters)
		return self.photopoints


	def get_upperlimits(self,
		filters: Optional[Union[Dict[str, Any], Sequence[Dict[str, Any]]]] = None
	) -> Optional[Sequence[DataPoint]]:
		"""Get (filtered) upper limits"""
		if filters and self.upperlimits:
			return self._apply_filter(self.upperlimits, filters)
		return self.upperlimits


	# TODO: improve
	def get_pos(
		self, ret: str = "brightest",
		filters: Optional[Union[Dict[str, Any], Sequence[Dict[str, Any]]]] = None,
	) -> Optional[Union[Tuple[Any, Any], Sequence[Tuple[Any, Any]]]]:
		"""
		Calculate the position of the underlying object.

		:param ret:
			- raw: returns ((ra, dec), (ra, dec), ...)
			- mean: returns (<ra>, <dec>)
			- brightest: returns (ra, dec)
			- latest: returns (ra, dec)
		:param filters: filters to apply to photo points

		Get the position of the brightest PhotoPoint in the ZTF G band::

			instance.get_pos(
				"brightest",
				{'attribute': 'alTags', 'operator': 'in', 'value': 'ZTF_G'}
			)

		Get the position of the latest photopoint with a magnitude brighter than 18
		(or an empty array if no photopoint matches this criteria)::

			instance.get_pos(
				"lastest",
				{'attribute': 'magpsf', 'operator': '<', 'value': 18}
			)

		"""

		if ret == "raw":
			return self.get_tuples("ra", "dec", filters=filters)

		if not self.photopoints:
			return None

		pps = self._apply_filter(self.photopoints, filters) \
			if filters is not None else self.photopoints

		if not pps:
			return None

		if ret == "mean":
			ras = [pp['body']["ra"] for pp in pps]
			decs = [pp['body']["dec"] for pp in pps]
			return (sum(ras) / len(ras), sum(decs) / len(decs))

		if ret == "brightest":
			mags = list(pps)
			mags.sort(key=lambda x: x['body']['magpsf'])
			return (mags[-1]['body']['ra'], mags[-1]['body']['dec'])

		if ret == "latest":
			mags = list(pps)
			mags.sort(key=lambda x: x['body']['obs_date'])
			return (mags[-1]['body']['ra'], mags[-1]['body']['dec'])

		raise NotImplementedError("ret method: %s is not implemented" % ret)


	def _get_datapoints(self,
		filters: Optional[Union[Dict[str, Any], Sequence[Dict[str, Any]]]] = None,
		of_upper_limits: bool = False
	) -> Optional[Sequence[DataPoint]]:
		"""	"""

		if filters is None:
			if of_upper_limits:
				return self.upperlimits if self.upperlimits else None
			return self.photopoints

		datapoints = self.upperlimits if of_upper_limits else self.photopoints
		return self._apply_filter(datapoints, filters) if datapoints else None


	@staticmethod
	def _apply_filter(
		datapoints: Sequence[DataPoint],
		filters: Union[Dict[str, Any], Sequence[Dict[str, Any]]]
	) -> Sequence[DataPoint]:
		"""
		:raises ValueError: if datapoints is None or in case of bad filter values
		"""

		if isinstance(filters, dict):
			filters = [filters]
		else:
			if filters is None or not isinstance(filters, list):
				raise ValueError("filters must be of type dict or list")

		for filtre in filters:
			op = ops[filtre['operator']]
			datapoints = [
				dp for dp in datapoints if filtre['attribute'] in dp['body'] and
				op(dp['body'][filtre['attribute']], filtre['value'])
			]

		return datapoints
