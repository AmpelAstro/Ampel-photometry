#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-lsst/ampel/abstract/AbsTabulatedT2Unit.py
# License           : BSD-3-Clause
# Author            : mf <mf@physik.hu-berlin.de>
# Date              : 08.08.2021
# Last Modified Date: 13.09.2021
# Last Modified By  : mf <mf@physik.hu-berlin.de>

from typing import List, ClassVar, Dict, Sequence, Any, Union, Optional
from ampel.view.LightCurve import LightCurve
from ampel.content.T1Document import T1Document
from ampel.content.DataPoint import DataPoint
from ampel.base.AmpelABC import AmpelABC
from ampel.base.LogicalUnit import LogicalUnit
from ampel.base.AuxUnitRegister import AuxUnitRegister
from ampel.abstract.AbsT2Tabulator import AbsT2Tabulator
from ampel.model.UnitModel import UnitModel

from astropy.table import vstack, Table

class AbsTabulatedT2Unit(AmpelABC, LogicalUnit, abstract=True):
    """
    Base class for T2s that operate on tabulated data.
    """

    ingest: ClassVar[Dict[str, Any]]
    tabulator: Sequence[UnitModel] = []

    def __init__(self, **kwargs):
        self.tabulator = kwargs['tabulator']
        super().__init__(**kwargs)
        self._tab_engines: Sequence[AbsT2Tabulator] = [AuxUnitRegister.new_unit(model = el, sub_type = AbsT2Tabulator) for el in self.tabulator]

    def get_flux_table(self, dps: Union[LightCurve, List[DataPoint]], compound: Optional[T1Document] = None) -> Table:
        tables = [tab.get_flux_table(dps, compound) for tab in self._tab_engines]
        if len(tables) == 1:
            table = tables[0]
        elif len(tables) > 1:
            table = vstack(tables)
        else:
            raise NotImplementedError
        table.sort('time')
        return table
