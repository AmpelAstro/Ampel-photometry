#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-photometry/ampel/demo/DemoFirstUpperLimitT2Unit.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 25.03.2020
# Last Modified Date: 28.09.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from time import time
from typing import Union, ClassVar
from ampel.types import UBson
from ampel.struct.UnitResult import UnitResult
from ampel.content.DataPoint import DataPoint
from ampel.abstract.AbsPointT2Unit import AbsPointT2Unit
from ampel.model.DPSelection import DPSelection


class DemoFirstUpperLimitT2Unit(AbsPointT2Unit):

	eligible: ClassVar[DPSelection] = DPSelection(filter='ULSFilter', sort='jd', select='first')

	def process(self, datapoint: DataPoint) -> Union[UBson, UnitResult]:
		return {"id": datapoint['id'], "time": time()}