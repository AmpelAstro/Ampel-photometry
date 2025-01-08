import pickle
from functools import reduce

import pytest

from ampel.view.TransientView import TransientView


@pytest.fixture
def view():
    return TransientView(id="stockystock")


def gather_slots(typ):
    return reduce(list.__add__, [gather_slots(t) for t in typ.__bases__], []) + list(
        getattr(typ, "__slots__", tuple())
    )


def test_reduce(view: TransientView):
    tview = pickle.loads(pickle.dumps(view))
    slots = gather_slots(type(tview))
    assert len(slots) > 1
    for attr in gather_slots(type(tview)):
        assert getattr(tview, attr) == getattr(view, attr)

def test_build_lightcurve():
    view = TransientView(
        id=1,
        t0=[
            {"id": 1, "body": {"jd": 2450000.0, "mag": 12.0}},
            {"id": 2, "body": {"jd": 2450001.0, "mag": 13.0}},
        ],
        t1=[
            {"stock": 1, "link": 1, "dps": [1, 2]},
        ],
    )
    assert view.lightcurve
    assert len(view.lightcurve) == 1
    assert view.lightcurve[0].get_values("jd") == [2450000.0, 2450001.0]
    assert view.lightcurve[0].get_values("mag") == [12.0, 13.0]