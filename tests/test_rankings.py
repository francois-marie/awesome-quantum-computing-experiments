import math

import numpy as np
from scipy import stats

from src.rankings import (
    METRICS,
    Metric,
    Point,
    best_as_of,
    canonical_platform,
    fit,
    max_distance,
    rankings,
)


def metric(key: str) -> Metric:
    return next(m for m in METRICS if m.key == key)


class TestHelpers:
    def test_canonical_platform_merges_spellings(self):
        assert canonical_platform("Superconducting circuit") == "Superconducting circuits"
        assert canonical_platform("Superconducting qubits") == "Superconducting circuits"
        assert canonical_platform("Semiconductor") == "Semiconductor spins"
        assert canonical_platform("Trapped-ion") == "Ion traps"
        assert canonical_platform("") is None

    def test_max_distance(self):
        assert max_distance("[[25, 1, 5]]") == 5
        assert max_distance("[3,1,3]-[29,1,29]") == 29
        assert max_distance("[[9,1,3]], [[25,1,5]], [[49,1,7]]") == 7
        assert max_distance("1D with 12 qubits") is None


class TestFit:
    def test_log_fit_matches_linregress(self):
        m = metric("entangled_error")
        pts = [(2010, 0.1), (2015, 0.01), (2020, 0.002)]
        f = fit(m, pts)
        ref = stats.linregress([x for x, _ in pts], [np.log10(y) for _, y in pts])
        assert math.isclose(f.slope, ref.slope)
        assert math.isclose(f.intercept, ref.intercept)
        assert math.isclose(f.doubling_time, abs(math.log10(2) / ref.slope))

    def test_fit_needs_two_distinct_years(self):
        m = metric("qubit_count")
        assert fit(m, [(2020, 10)]) is None
        assert fit(m, [(2020, 10), (2020, 20)]) is None


class TestRankings:
    def test_best_as_of_respects_year_and_direction(self):
        m = metric("entangled_error")
        pts = [
            Point(2010, 0.1, "Ion traps", "a", ""),
            Point(2020, 0.001, "Ion traps", "b", ""),
            Point(2015, 0.01, "Neutral atoms", "c", ""),
        ]
        assert best_as_of(m, 2016, pts)["Ion traps"].value == 0.1
        assert best_as_of(m, math.inf, pts)["Ion traps"].value == 0.001

    def test_rankings_on_real_data_are_consistent(self):
        for m in METRICS:
            table = rankings(m)
            ranks = sorted(r.best_rank for r in table.rows)
            assert ranks == list(range(1, len(table.rows) + 1))
            with_data = [r for r in table.rows if r.best]
            assert with_data, m.key
            top = min(with_data, key=lambda r: r.best_rank)
            for r in with_data:
                if m.better == "min":
                    assert top.best.value <= r.best.value
                else:
                    assert top.best.value >= r.best.value
