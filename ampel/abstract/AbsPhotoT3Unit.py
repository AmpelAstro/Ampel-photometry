#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-photometry/ampel/abstract/AbsPagedPhotoT3Unit.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 01.06.2020
# Last Modified Date: 19.04.2021
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import ClassVar, Type
from ampel.abstract.AbsT3Unit import AbsT3Unit
from ampel.view.TransientView import TransientView


class AbsPhotoT3Unit(AbsT3Unit[TransientView], abstract=True):
	"""
	Parametrized abstract class for T3 units receiving TransientView instances
	(and potentially LightCurve instances as well)
	"""
	_View: ClassVar[Type] = TransientView # avoid introspection at run-time
	
	pass
