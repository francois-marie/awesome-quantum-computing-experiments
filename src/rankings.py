"""Platform rankings per metric: best value to date and pace of improvement.

This is the Python twin of ``site/src/lib/metrics.ts`` and must stay in sync
with it: same metric definitions, same canonical platform names, same
least-squares fit in log space (``scipy.stats.linregress`` on log10 values,
which is what the plot fits use as well).
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass, field
from typing import Callable

import pandas as pd
import yaml
from scipy import stats

PLATFORMS = [
    "Superconducting circuits",
    "Ion traps",
    "Neutral atoms",
    "Semiconductor spins",
    "Photons",
    "NV centers",
    "NMR",
    "Graphene",
]


def canonical_platform(name: str) -> str | None:
    n = (name or "").lower()
    if "supercond" in n:
        return "Superconducting circuits"
    if "ion" in n:
        return "Ion traps"
    if "neutral" in n or "atom" in n:
        return "Neutral atoms"
    if "semicond" in n or "spin" in n or "silicon" in n:
        return "Semiconductor spins"
    if "photon" in n:
        return "Photons"
    if "nv" in n:
        return "NV centers"
    if "nmr" in n:
        return "NMR"
    if "graphene" in n:
        return "Graphene"
    return None


def _num(v) -> float | None:
    try:
        x = float(v)
    except (TypeError, ValueError):
        return None
    return x if math.isfinite(x) else None


def _leading_number(v) -> float | None:
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return None
    m = re.search(r"-?\d+(?:\.\d+)?(?:e-?\d+)?", str(v), re.I)
    return float(m.group(0)) if m else None


def max_distance(params) -> float | None:
    if not isinstance(params, str) or not params:
        return None
    found = re.findall(r"\[\[?\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\]?\]", params)
    return max(float(d) for _, _, d in found) if found else None


@dataclass
class Metric:
    key: str
    label: str
    short: str
    dataset: str
    value: Callable[[pd.Series], float | None]
    better: str  # "min" | "max"
    log: bool
    aggregate: str = "best"  # "best" | "count"


METRICS: list[Metric] = [
    Metric("entangled_error", "Entangled state error", "2Q error", "entangled",
           lambda r: _num(r.get("Entangled State Error")), "min", True),
    Metric("qubit_count", "Qubit count", "Qubits", "qubit_count",
           lambda r: _num(r.get("Number of qubits")), "max", True),
    Metric("t1", "Relaxation time T1", "T1", "physical_qubits", lambda r: _num(r.get("T1")), "max", True),
    Metric("t2", "Coherence time T2", "T2", "physical_qubits", lambda r: _num(r.get("T2")), "max", True),
    Metric("qec_distance", "Largest QEC code distance", "Distance", "qec",
           lambda r: max_distance(r.get("Code Parameters")), "max", False),
    Metric("qec_count", "QEC experiments", "QEC exps", "qec", lambda r: 1.0, "max", False, aggregate="count"),
    Metric("magic_error", "Magic state error", "Magic error", "msd",
           lambda r: (None if (f := _leading_number(r.get("Fidelity"))) is None or f >= 1 else 1 - f), "min", True),
]


def metric_by_key(key: str) -> Metric:
    return next(m for m in METRICS if m.key == key)


@dataclass
class Point:
    year: float
    value: float
    platform: str
    title: str
    link: str


@dataclass
class Fit:
    slope: float
    intercept: float
    n: int
    doubling_time: float


@dataclass
class Ranking:
    platform: str
    best: Point | None
    best_rank: int
    rate: Fit | None
    rate_rank: int


@dataclass
class RankingTable:
    metric: Metric
    platforms: list[str]
    rows: list[Ranking] = field(default_factory=list)


def load_config(path: str = "config.yaml") -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def points(metric: Metric, config: dict | None = None) -> list[Point]:
    config = config or load_config()
    df = pd.read_csv(config["paths"]["data"][metric.dataset], dtype=str)
    out: list[Point] = []
    for _, row in df.iterrows():
        value = metric.value(row)
        year = _num(row.get("Year"))
        platform = canonical_platform(row.get("Platform", ""))
        if value is None or year is None or not platform:
            continue
        out.append(Point(year, value, platform, str(row.get("Article Title", "")), str(row.get("Link", ""))))
    return sorted(out, key=lambda p: (p.year, p.title))


def _is_better(metric: Metric, a: float, b: float) -> bool:
    return a < b if metric.better == "min" else a > b


def best_as_of(metric: Metric, year: float = math.inf, pts: list[Point] | None = None) -> dict[str, Point]:
    pts = points(metric) if pts is None else pts
    out: dict[str, Point] = {}
    for p in pts:
        if p.year > year:
            continue
        cur = out.get(p.platform)
        if metric.aggregate == "count":
            out[p.platform] = Point(p.year, (cur.value + 1) if cur else 1.0, p.platform, p.title, p.link)
        elif cur is None or _is_better(metric, p.value, cur.value):
            out[p.platform] = p
    return out


def fit(metric: Metric, pts: list[tuple[float, float]]) -> Fit | None:
    """OLS of (log10) value against year; identical to the plot fits."""
    if len(pts) < 2 or len({x for x, _ in pts}) < 2:
        return None
    xs = [x for x, _ in pts]
    ys = [math.log10(y) if metric.log else y for _, y in pts]
    res = stats.linregress(xs, ys)
    slope = float(res.slope)
    doubling = math.inf if slope == 0 else abs(math.log10(2) / slope)
    return Fit(slope, float(res.intercept), len(pts), doubling)


def improvement_rate(metric: Metric, platform: str, year: float = math.inf, window: float = math.inf,
                     pts: list[Point] | None = None) -> Fit | None:
    pts = points(metric) if pts is None else pts
    sel = [p for p in pts if p.platform == platform and p.year <= year and p.year > year - window]
    if metric.aggregate == "count":
        pairs = [(p.year, float(i + 1)) for i, p in enumerate(sel)]
    else:
        pairs = [(p.year, p.value) for p in sel]
    f = fit(metric, pairs)
    if f is None:
        return None
    if metric.better == "min":
        f = Fit(-f.slope, f.intercept, f.n, f.doubling_time)
    return f


def latest_year(config: dict | None = None) -> float:
    return max(p.year for m in METRICS for p in points(m, config))


def rankings(metric: Metric, year: float = math.inf, window: float = math.inf,
             platforms: list[str] | None = None, config: dict | None = None) -> RankingTable:
    """Rank platforms on best value and on improvement rate (rank 1 is best; missing data ranks last)."""
    pts = points(metric, config)
    if math.isinf(year) and not math.isinf(window):
        # "As of today" for a finite window means the latest year across all metrics (as on the website).
        year = latest_year(config)
    if platforms is None:
        present = {p.platform for p in pts}
        platforms = [p for p in PLATFORMS if p in present]
    best = best_as_of(metric, year, pts)
    rows = [(p, best.get(p), improvement_rate(metric, p, year, window, pts)) for p in platforms]

    def best_key(row):
        _, b, _ = row
        if b is None:
            return (1, 0.0)
        return (0, b.value if metric.better == "min" else -b.value)

    def rate_key(row):
        _, _, r = row
        return (1, 0.0) if r is None else (0, -r.slope)

    by_best = [r[0] for r in sorted(rows, key=best_key)]
    by_rate = [r[0] for r in sorted(rows, key=rate_key)]
    table = RankingTable(metric, platforms)
    for platform, b, r in rows:
        table.rows.append(Ranking(platform, b, by_best.index(platform) + 1, r, by_rate.index(platform) + 1))
    return table
