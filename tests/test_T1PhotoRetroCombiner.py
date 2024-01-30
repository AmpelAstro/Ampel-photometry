import pytest

from ampel.content.DataPoint import DataPoint
from ampel.log.AmpelLogger import AmpelLogger
from ampel.t1.T1PhotoRetroCombiner import T1PhotoRetroCombiner


@pytest.fixture
def ampel_logger():
    return AmpelLogger.get_logger()


def test_prev_det_sequences(ampel_logger):
    """
    Sequences of previous detections are emitted in order
    """
    t1_combiner = T1PhotoRetroCombiner(access=[], policy=[], logger=ampel_logger)
    ids = [-1, 1, -2, 2, 3, -4, -5, 6, 7]
    dps: list[DataPoint] = [{"id": id} for id in ids]
    results = t1_combiner.combine(dps)
    assert len(results) == 5
    assert [r.dps for r in results] == [
        ids[: i + 1] for i, id in enumerate(ids) if id > 0
    ]
