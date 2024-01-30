#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-photometry/ampel/demo/DemoEvery3PhotoPointT2Unit.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                25.03.2020
# Last Modified Date:  28.09.2021
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from time import time
from typing import ClassVar

from ampel.abstract.AbsPointT2Unit import AbsPointT2Unit
from ampel.content.DataPoint import DataPoint
from ampel.model.DPSelection import DPSelection
from ampel.struct.UnitResult import UnitResult
from ampel.types import UBson


class DemoEvery3PhotoPointT2Unit(AbsPointT2Unit):

	eligible: ClassVar[DPSelection] = DPSelection(
		filter='PPSFilter', sort='jd', select=[2, None, 3]
	)

	def process(self, datapoint: DataPoint) -> UBson | UnitResult:
		return {"id": datapoint['id'], "time": time()}
