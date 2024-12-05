from functools import reduce

import pytest

from ampel.view.TransientView import TransientView


@pytest.fixture
def view():
    return TransientView("stockystock")


def gather_slots(typ):
    return reduce(list.__add__, [gather_slots(t) for t in typ.__bases__], []) + list(
        getattr(typ, "__slots__", tuple())
    )


def test_reduce(view: TransientView):
    cls, args = view.__reduce__()
    tview = cls(*args)
    slots = gather_slots(type(tview))
    assert slots
    for attr in gather_slots(type(tview)):
        assert getattr(tview, attr) == getattr(view, attr)
