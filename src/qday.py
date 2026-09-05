"""Q-day estimates: when do platform trends meet the requirements of published
resource estimates for breaking RSA-2048 / ECC-256?

Each target in ``data/qday_targets.csv`` states, for one platform, the number
of physical qubits and (optionally) the physical two-qubit error rate a
proposal needs. For every platform we fit the all-time exponential trend of
the demonstrated qubit count and of the entangled-state error (the same
least-squares fits in log space as the plots) and extrapolate the year each
requirement is met. The Q-day estimate for a target is the later of the two
crossing years. This is a straight-line extrapolation, not a forecast.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path

import pandas as pd

from .rankings import Fit, Point, fit, load_config, metric_by_key, points

QUBITS = metric_by_key("qubit_count")
ERROR = metric_by_key("entangled_error")


@dataclass
class Target:
    target: str
    problem: str
    platform: str
    physical_qubits: float
    physical_error: float | None
    runtime: str
    year: float | None
    first_author: str
    title: str
    link: str
    notes: str


@dataclass
class Crossing:
    target: str
    problem: str
    platform: str
    physical_qubits: float
    physical_error: float | None
    qubits_year: float | None
    error_year: float | None
    qday_year: float | None
    limiting: str | None  # "qubits" | "error" | None
    runtime: str
    link: str
    notes: str


@dataclass
class PlatformTrend:
    platform: str
    qubits_fit: Fit | None
    error_fit: Fit | None
    qubits_points: list[Point]
    error_points: list[Point]
    qubits_last_year: float | None
    error_last_year: float | None


def load_targets(config: dict | None = None) -> list[Target]:
    config = config or load_config()
    df = pd.read_csv(config["paths"]["data"]["qday_targets"], dtype=str).fillna("")
    out: list[Target] = []
    for _, r in df.iterrows():
        out.append(Target(
            target=r["Target"].strip(),
            problem=r["Problem"].strip(),
            platform=r["Platform"].strip(),
            physical_qubits=float(r["Physical Qubits"]),
            physical_error=float(r["Physical Error Rate"]) if r["Physical Error Rate"].strip() else None,
            runtime=r["Runtime"].strip(),
            year=float(r["Year"]) if r["Year"].strip() else None,
            first_author=r["First Author"].strip(),
            title=r["Article Title"].strip(),
            link=r["Link"].strip(),
            notes=r["Notes"].strip(),
        ))
    return out


def crossing_year(f: Fit | None, target: float, log: bool = True, direction: str = "up") -> float | None:
    """Year at which the fitted trend reaches ``target`` (None if it never does)."""
    if f is None or f.slope == 0:
        return None
    y = math.log10(target) if log else target
    year = (y - f.intercept) / f.slope
    moving_right_way = f.slope > 0 if direction == "up" else f.slope < 0
    if not moving_right_way or not math.isfinite(year):
        return None
    return year


def platform_trend(platform: str, config: dict | None = None) -> PlatformTrend:
    q = [p for p in points(QUBITS, config) if p.platform == platform]
    e = [p for p in points(ERROR, config) if p.platform == platform]
    return PlatformTrend(
        platform=platform,
        qubits_fit=fit(QUBITS, [(p.year, p.value) for p in q]),
        error_fit=fit(ERROR, [(p.year, p.value) for p in e]),
        qubits_points=q,
        error_points=e,
        qubits_last_year=max((p.year for p in q), default=None),
        error_last_year=max((p.year for p in e), default=None),
    )


def crossings(config: dict | None = None) -> list[Crossing]:
    config = config or load_config()
    trends: dict[str, PlatformTrend] = {}
    out: list[Crossing] = []
    for t in load_targets(config):
        trend = trends.setdefault(t.platform, platform_trend(t.platform, config))
        qy = crossing_year(trend.qubits_fit, t.physical_qubits, log=True, direction="up")
        ey = crossing_year(trend.error_fit, t.physical_error, log=True, direction="down") if t.physical_error else None
        # A requirement already met counts as met in the year of the best result.
        best_q = max((p.value for p in trend.qubits_points), default=0)
        if best_q >= t.physical_qubits:
            qy = min(p.year for p in trend.qubits_points if p.value >= t.physical_qubits)
        if t.physical_error is not None and trend.error_points:
            best_e = min(p.value for p in trend.error_points)
            if best_e <= t.physical_error:
                ey = min(p.year for p in trend.error_points if p.value <= t.physical_error)
        candidates = [(y, name) for y, name in ((qy, "qubits"), (ey, "error")) if y is not None]
        if t.physical_error is not None and (ey is None or qy is None):
            qday, limiting = None, None  # one requirement never met by the trend
        elif candidates:
            qday, limiting = max(candidates)
        else:
            qday, limiting = None, None
        out.append(Crossing(
            target=t.target, problem=t.problem, platform=t.platform,
            physical_qubits=t.physical_qubits, physical_error=t.physical_error,
            qubits_year=qy, error_year=ey, qday_year=qday, limiting=limiting,
            runtime=t.runtime, link=t.link, notes=t.notes,
        ))
    return out


def export_json(path: str | Path = "out/figures/qday.json", config: dict | None = None) -> Path:
    """Write crossings and trends for the website."""
    config = config or load_config()
    rows = crossings(config)
    platforms = sorted({r.platform for r in rows})
    trends = {}
    for platform in platforms:
        t = platform_trend(platform, config)
        trends[platform] = {
            "qubits_fit": asdict(t.qubits_fit) if t.qubits_fit else None,
            "error_fit": asdict(t.error_fit) if t.error_fit else None,
            "qubits_last_year": t.qubits_last_year,
            "error_last_year": t.error_last_year,
        }
    payload = {
        "generated_from": ["data/qday_targets.csv", "data/qubit_count.csv", "data/entangled_state_error_exp.csv"],
        "crossings": [asdict(r) for r in rows],
        "trends": trends,
    }
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(payload, f, indent=1, ensure_ascii=False)
    return path


if __name__ == "__main__":
    for c in crossings():
        print(f"{c.platform:24} {c.target:28} qubits→{c.qubits_year and round(c.qubits_year, 1)} "
              f"error→{c.error_year and round(c.error_year, 1)} Q-day≈{c.qday_year and round(c.qday_year, 1)} ({c.limiting})")
    print(export_json())
