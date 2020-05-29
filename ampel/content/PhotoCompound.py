#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-photometry/ampel/content/PhotoCompound.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 10.12.2019
# Last Modified Date: 16.02.2020
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Sequence, Optional, Dict
from ampel.content.Compound import Compound


class PhotoCompound(Compound, total=False):

	lastjd: float
	ppsid: Optional[bytes]
	flavor: Optional[Sequence[Dict]]
