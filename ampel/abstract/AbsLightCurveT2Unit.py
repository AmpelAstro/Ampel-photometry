#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-photometry/ampel/abstract/AbsLightCurveT2Unit.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 13.12.2017
# Last Modified Date: 01.03.2020
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Iterable, ClassVar, Dict, Any
from ampel.view.LightCurve import LightCurve
from ampel.content.Compound import Compound
from ampel.content.DataPoint import DataPoint
from ampel.abstract.AbsCustomStateT2Unit import AbsCustomStateT2Unit


class AbsLightCurveT2Unit(AbsCustomStateT2Unit[LightCurve], abstract=True):
	"""
	Base class for T2s that operate on light curves.
	"""

	#: Light curve compilation settings.
	#: These are extracted in :meth:`AbsT2Ingester.add_ingest_models() <ampel.abstract.ingest.AbsT2Ingester.AbsT2Ingester.add_ingest_models>`, combined
	#: with default settings from other sources, passed to :meth:`PhotoT2Compiler.set_ingest_options() <ampel.ingest.compile.PhotoT2Compiler.PhotoT2Compiler.set_ingest_options>`, and used in :meth:`PhotoT2Compiler.compile() <ampel.ingest.compile.PhotoT2Compiler.PhotoT2Compiler.compile>`.
	#: 
	#: upper_limits:
	#:   - True: compound id computed using photopoint & upperlimit ids
	#:   - False: compound id computed using photopoint ids only
	ingest: ClassVar[Dict[str, Any]] = {'upper_limits': True}


	@staticmethod
	def build(compound: Compound, datapoints: Iterable[DataPoint]) -> LightCurve:
		return LightCurve.build(compound, datapoints)
