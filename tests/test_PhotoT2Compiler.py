import logging

import pytest

from ampel.content.DataPoint import DataPoint
from ampel.compile.PhotoT2Compiler import PhotoT2Compiler
from ampel.compile.T1PhotoCombiner import T1PhotoCombiner
from ampel.model.ingest.T2IngestModel import T2IngestModel


def test_t2_optimization():
    """
    T2 plans are coalesced separately for channels that request upper limits
    and detections only.
    """
    combiner = T1PhotoCombiner(logger=logging.getLogger())
    compiler = PhotoT2Compiler()

    channels = [f"CHANNEL_{i}" for i in range(1, 4)]

    # 2 channels that use upper limits, 1 that doesn't
    ingest_model = T2IngestModel(unit="SomeUnit", config=0)
    for channel, uls in zip(channels, (True, True, False)):
        compiler.add_ingest_model(channel, ingest_model)
        compiler.set_ingest_options(channel, ingest_model, {"upper_limits": uls})

    # mix of negative (upper limit) and positive (detection) ids
    datapoints = [
        DataPoint({"_id": i, "stock": 0, "body": {"idx": i}}) for i in range(-5, 5)
    ]
    bp = combiner.combine(0, datapoints, channels)
    optimized_t2s = compiler.compile([(c, True) for c in channels], bp)
    assert len(optimized_t2s) == 2, "exactly 2 t2 docs planned"
    assert all(
        k[:2] == ("SomeUnit", 0) for k in optimized_t2s.keys()
    ), "unit and config match for all docs"
    items = list(optimized_t2s.items())
    assert items[0][1] == set(channels[:2])
    assert isinstance(items[0][0][-1], bytes)
    assert items[1][1] == set(channels[2:])
    assert isinstance(items[1][0][-1], tuple)
    assert (
        items[0][0][-1] == items[1][0][-1][-1]
    ), "id of complete compound matches strict id of detection-only compound"
