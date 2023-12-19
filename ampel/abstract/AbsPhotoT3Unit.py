#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File:                Ampel-photometry/ampel/abstract/AbsPhotoT3Unit.py
# License:             BSD-3-Clause
# Author:              valery brinnel <firstname.lastname@gmail.com>
# Date:                01.06.2020
# Last Modified Date:  19.04.2021
# Last Modified By:    valery brinnel <firstname.lastname@gmail.com>

from ampel.abstract.AbsT3Unit import AbsT3Unit
from ampel.view.TransientView import TransientView


class AbsPhotoT3Unit(AbsT3Unit[TransientView], abstract=True):
	"""
	Parametrized abstract class for T3 units receiving TransientView instances
	(and potentially LightCurve instances as well)
	"""
	_View = TransientView
	pass
