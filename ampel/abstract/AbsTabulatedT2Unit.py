#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-lsst/ampel/abstract/AbsTabulatedT2Unit.py
# License           : BSD-3-Clause
# Author            : Marcus Fenner <mf@physik.hu-berlin.de>
# Date              : 08.08.2021
# Last Modified Date: 05.05.2022
# Last Modified By  : Marcus Fenner <mf@physik.hu-berlin.de>

import math
from collections.abc import Iterable, Sequence
from typing import Any, ClassVar, Literal

from astropy.table import Table, vstack

from ampel.abstract.AbsT2Tabulator import AbsT2Tabulator
from ampel.base.AmpelABC import AmpelABC
from ampel.base.AmpelUnit import AmpelUnit
from ampel.base.AuxUnitRegister import AuxUnitRegister
from ampel.content.DataPoint import DataPoint
from ampel.model.UnitModel import UnitModel
from ampel.types import StockId


class AbsTabulatedT2Unit(AmpelABC, AmpelUnit, abstract=True):
    """
    Base class for T2s that operate on tabulated data.
    """

    ingest: ClassVar[dict[str, Any]]
    tabulator: Sequence[UnitModel] = []

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._tab_engines: Sequence[AbsT2Tabulator] = [
            AuxUnitRegister.new_unit(model=el, sub_type=AbsT2Tabulator)
            for el in self.tabulator
        ]

    def get_flux_table(
        self,
        dps: Iterable[DataPoint],
        jd_start: None | float = None,
        jd_end: None | float = None,
    ) -> Table:
        tables = [tab.get_flux_table(dps) for tab in self._tab_engines]
        if len(tables) == 1:
            table = tables[0]
        elif len(tables) > 1:
            table = vstack(tables, join_type="exact")
        else:
            raise NotImplementedError
        table.sort("time")
        if jd_start and not math.isinf(jd_start):
            mask = table["time"] < jd_start
            table = table[~mask]
        if jd_end and not math.isinf(jd_end):
            mask = table["time"] < jd_end
            table = table[~mask]
        return table

    def get_stock_id(
        self,
        dps: Iterable[DataPoint],
    ) -> list[StockId]:
        return [
            stock
            for tab in self._tab_engines
            for stock in tab.get_stock_id(dps)
        ]

    def get_stock_name(
        self,
        dps: Iterable[DataPoint],
    ) -> list[str | int]:
        return [
            name
            for tab in self._tab_engines
            for name in tab.get_stock_name(dps)
        ]

    def get_positions(
        self, dps: Iterable[DataPoint]
    ) -> list[tuple[float, float, float]]:
        """
        Get a tuple (time, ra, dec)
        """
        return [
            pos for tab in self._tab_engines for pos in tab.get_positions(dps)
        ]

    def get_pos(
        self, dps: Iterable[DataPoint], which: Literal["mean", "last", "first"] = "mean"
    ) -> tuple[float, float]:
        positions = self.get_positions(dps)

        if which == "mean":
            import numpy as np

            return (
                np.mean(list(zip(*positions, strict=False))[1]),
                np.mean(list(zip(*positions, strict=False))[2]),
            )
        if which == "last":
            return sorted(positions, key=lambda x: x[0])[-1][1:3]
        if which == "first":
            return sorted(positions, key=lambda x: x[0])[0][1:3]
        raise NotImplementedError
