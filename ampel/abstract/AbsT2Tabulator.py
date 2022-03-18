#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-lsst/ampel/abstract/AbsT2Tabulator.py
# License           : BSD-3-Clause
# Author            : Marcus Fenner <mf@physik.hu-berlin.de>
# Date              : 25.05.2021
# Last Modified Date: 21.03.2022
# Last Modified By  : Marcus Fenner <mf@physik.hu-berlin.de>

from typing import Any, List, Sequence, Tuple, Union

from ampel.base.AmpelABC import AmpelABC
from ampel.base.AmpelBaseModel import AmpelBaseModel
from ampel.base.decorator import abstractmethod
from ampel.content.DataPoint import DataPoint
from astropy.table import Table


class AbsT2Tabulator(AmpelABC, AmpelBaseModel, abstract=True):
    """ """

    @abstractmethod
    def get_flux_table(self, dps: List[DataPoint]) -> Table:
        ...

    @abstractmethod
    def get_pos(self, dps: List[DataPoint]) -> Sequence[Tuple[Any, Any]]:
        ...

    @abstractmethod
    def get_jd(self, dps: List[DataPoint]) -> Sequence[Any]:
        ...

    @abstractmethod
    def get_stock_id(self, dps: List[DataPoint]) -> set[int]:
        ...

    @abstractmethod
    def get_stock_name(self, dps: List[DataPoint]) -> list[str]:
        ...
