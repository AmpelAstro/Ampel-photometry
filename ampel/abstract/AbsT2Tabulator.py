#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-lsst/ampel/abstract/AbsT2Tabulator.py
# License           : BSD-3-Clause
# Author            : mf <mf@physik.hu-berlin.de>
# Date              : 25.05.2021
# Last Modified Date: 13.09.2021
# Last Modified By  : mf <mf@physik.hu-berlin.de>

from typing import Sequence, Optional, List, Any, Tuple, Union
from ampel.base.AmpelBaseModel import AmpelBaseModel
from ampel.base.AmpelABC import AmpelABC
from ampel.content.DataPoint import DataPoint
from astropy.table import Table
from ampel.view.LightCurve import LightCurve
from ampel.base.decorator import abstractmethod
from ampel.content.T1Document import T1Document

class AbsT2Tabulator(AmpelABC, AmpelBaseModel, abstract=True):
    """ """
    @abstractmethod
    def get_flux_table(self, dps: Union[LightCurve, List[DataPoint]], compound: Optional[T1Document] = None) -> Table:
        ...

    @abstractmethod
    def get_pos(self, dps: Union[LightCurve, List[DataPoint]], compound: Optional[T1Document] = None) -> Sequence[Tuple[Any, Any]]:
        ...

    @abstractmethod
    def get_jd(self, dps: Union[LightCurve, List[DataPoint]], compound: Optional[T1Document] = None) -> Sequence[Any]:
        ...
