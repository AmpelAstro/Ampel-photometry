#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-photometry/ampel/abstract/AbsPagedPhotoT3Unit.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 01.06.2020
# Last Modified Date: 08.06.2020
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Tuple, Optional, Union, Dict
from ampel.type import StockId
from ampel.base import abstractmethod
from ampel.abstract.AbsPagedT3Unit import AbsPagedT3Unit
from ampel.view.TransientView import TransientView
from ampel.struct.JournalTweak import JournalTweak


class AbsPagedPhotoT3Unit(AbsPagedT3Unit[TransientView], abstract=True):
	"""
	Parametrized abstract class for T3 units receiving TransientView instances
	(and potentially LightCurve instances as well)
	"""

	@abstractmethod
	def add(self, views: Tuple[TransientView, ...]) -> Optional[Union[JournalTweak, Dict[StockId, JournalTweak]]]:
		""" Implementing T3 units get SnapViews (or sub-classes) via this this method """
		...
