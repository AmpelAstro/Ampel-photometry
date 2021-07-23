#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-photometry/ampel/demo/DemoEvery3PhotoPointT2Unit.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 25.03.2020
# Last Modified Date: 30.05.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from time import time
from typing import Union, ClassVar, Optional
from ampel.types import UBson
from ampel.struct.UnitResult import UnitResult
from ampel.content.DataPoint import DataPoint
from ampel.abstract.AbsPointT2Unit import AbsPointT2Unit
from ampel.model.T2IngestOptions import T2IngestOptions


class DemoEvery3PhotoPointT2Unit(AbsPointT2Unit):

	eligible: ClassVar[Optional[T2IngestOptions]] = {
		'filter': 'PPSFilter', 'sort': 'jd', 'select': [2, None, 3]
	}

	def process(self, datapoint: DataPoint) -> Union[UBson, UnitResult]:
		return {"id": datapoint['id'], "time": time()}
