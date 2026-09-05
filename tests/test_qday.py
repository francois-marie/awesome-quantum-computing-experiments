import math

from src.qday import crossing_year, crossings, load_targets
from src.rankings import Fit


class TestCrossingYear:
    def test_growth_trend_reaches_target(self):
        # log10(qubits) = 0.2 * (year - 2000): 100 qubits in 2010, 1e5 qubits in 2025.
        f = Fit(slope=0.2, intercept=-400.0, n=5, doubling_time=math.log10(2) / 0.2)
        assert math.isclose(crossing_year(f, 1e5, log=True, direction="up"), 2025.0)

    def test_wrong_direction_never_crosses(self):
        f = Fit(slope=-0.1, intercept=200.0, n=5, doubling_time=math.log10(2) / 0.1)
        assert crossing_year(f, 1e5, log=True, direction="up") is None

    def test_error_trend_going_down(self):
        # log10(error) = -0.1 * (year - 2000): 1e-1 in 2010, 1e-3 in 2030.
        f = Fit(slope=-0.1, intercept=200.0, n=5, doubling_time=math.log10(2) / 0.1)
        assert math.isclose(crossing_year(f, 1e-3, log=True, direction="down"), 2030.0)

    def test_flat_or_missing_fit(self):
        assert crossing_year(None, 10, True, "up") is None
        assert crossing_year(Fit(0.0, 1.0, 3, math.inf), 10, True, "up") is None


class TestTargets:
    def test_targets_load_with_required_fields(self):
        targets = load_targets()
        assert targets
        for t in targets:
            assert t.platform and t.physical_qubits > 0 and t.link.startswith("http")
            if t.physical_error is not None:
                assert 0 < t.physical_error < 1

    def test_crossings_are_consistent(self):
        rows = crossings()
        assert len(rows) == len(load_targets())
        for r in rows:
            if r.qday_year is not None:
                assert r.limiting in ("qubits", "error")
                parts = [y for y in (r.qubits_year, r.error_year) if y is not None]
                assert math.isclose(r.qday_year, max(parts))
            if r.physical_error is None:
                assert r.error_year is None
