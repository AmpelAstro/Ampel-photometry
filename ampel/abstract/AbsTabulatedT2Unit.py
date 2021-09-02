#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-lsst/ampel/abstract/AbsTabulatedT2Unit.py
# License           : BSD-3-Clause
# Author            : mf <mf@physik.hu-berlin.de>
# Date              : 08.08.2021
# Last Modified Date: 02.09.2021
# Last Modified By  : mf <mf@physik.hu-berlin.de>

from typing import Iterable, List, ClassVar, Dict, Sequence, Any
from ampel.view.LightCurve import LightCurve
from ampel.content.T1Document import T1Document
from ampel.content.DataPoint import DataPoint
from ampel.abstract.AbsStateT2Unit import AbsStateT2Unit
from ampel.base.AuxUnitRegister import AuxUnitRegister
from ampel.abstract.AbsT2Tabulator import AbsT2Tabulator
from ampel.model.UnitModel import UnitModel


class AbsTabulatedT2Unit(AbsStateT2Unit, abstract=True):
    """
    Base class for T2s that operate on tabulated data.
    """

    ingest: ClassVar[Dict[str, Any]]
    tabulator: Sequence[UnitModel] = []

    def __init__(self, **kwargs):
        self.tabulator = kwargs['tabulator']
        super().__init__(**kwargs)
        self._tab_engines: Sequence[AbsT2Tabulator] = [AuxUnitRegister.new_unit(model = el, sub_type = AbsT2Tabulator) for el in self.tabulator]

