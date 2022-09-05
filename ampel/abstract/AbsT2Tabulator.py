#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-lsst/ampel/abstract/AbsT2Tabulator.py
# License           : BSD-3-Clause
# Author            : Marcus Fenner <mf@physik.hu-berlin.de>
# Date              : 25.05.2021
# Last Modified Date: 05.05.2022
# Last Modified By  : Marcus Fenner <mf@physik.hu-berlin.de>

from typing import Any, List, Sequence, Tuple, Iterable

from ampel.base.AmpelABC import AmpelABC
from ampel.base.AmpelBaseModel import AmpelBaseModel
from ampel.base.decorator import abstractmethod
from ampel.content.DataPoint import DataPoint
from ampel.types import StockId
from astropy.table import Table


class AbsT2Tabulator(AmpelABC, AmpelBaseModel, abstract=True):
    """ """

    @abstractmethod
    def get_flux_table(self, dps: Iterable[DataPoint]) -> Table:
        ...

    @abstractmethod
    def get_positions(
        self, dps: Iterable[DataPoint]
    ) -> Sequence[Tuple[float, float, float]]:
        ...

    @abstractmethod
    def get_jd(self, dps: Iterable[DataPoint]) -> Sequence[Any]:
        ...

    @abstractmethod
    def get_stock_id(self, dps: Iterable[DataPoint]) -> set[StockId]:
        ...

    @abstractmethod
    def get_stock_name(self, dps: Iterable[DataPoint]) -> list[str]:
        ...
