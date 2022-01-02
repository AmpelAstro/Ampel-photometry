#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-photometry/ampel/demo/DemoEvery4PhotoPointT2Unit.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                25.03.2020
# Last Modified Date:  28.09.2021
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from time import time
from typing import ClassVar
from ampel.types import UBson
from ampel.struct.UnitResult import UnitResult
from ampel.content.DataPoint import DataPoint
from ampel.abstract.AbsPointT2Unit import AbsPointT2Unit
from ampel.model.DPSelection import DPSelection


class DemoEvery4PhotoPointT2Unit(AbsPointT2Unit):

	eligible: ClassVar[DPSelection] = DPSelection(
		filter='PPSFilter', sort='jd', select=[2, None, 4]
	)

	def process(self, datapoint: DataPoint) -> UBson | UnitResult:
		return {"id": datapoint['id'], "time": time()}
