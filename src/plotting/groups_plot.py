"""Research-group plots built from ``data/research_groups.csv``.

Two figures:

* ``papers_by_org_type``: unique papers per year, stacked by organisation type
  (industry / academic / mixed / unknown).
* ``top_research_groups``: the groups with the most papers in the database,
  coloured by organisation type, with the per-dataset breakdown in the hover.
"""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go

from .base import BasePlot

ORG_TYPES = ["industry", "academic", "mixed", "unknown"]
ORG_LABELS = {"industry": "Industry", "academic": "Academic", "mixed": "Mixed", "unknown": "Unknown"}

DATASET_LABELS = {
    "qec": "QEC",
    "msd": "Magic state",
    "entangled": "Entangled error",
    "qubit_count": "Qubit count",
    "physical_qubits": "Coherence",
}


class GroupsPlotBase(BasePlot):
    """Shared loading: one row per (paper, dataset) joined with its research group."""

    def __init__(self, skip_export=False):
        super().__init__(skip_export=skip_export)
        self.ORG_COLORS = self.config.get("org_type_colors", {})
        self.papers = self._load_papers()

    def _load_papers(self) -> pd.DataFrame:
        groups = pd.read_csv(self.config["paths"]["data"]["research_groups"], dtype=str).fillna("")
        groups["Link"] = groups["Link"].str.strip()
        groups["Research Group"] = groups["Research Group"].str.strip().replace("", "Unknown")
        groups["Org Type"] = groups["Org Type"].str.strip().replace("", "unknown")

        frames = []
        for key, path in self.config["paths"]["data"].items():
            if key == "research_groups":
                continue
            df = pd.read_csv(path, dtype=str).fillna("")
            df = df[df["Link"].str.strip() != ""]
            frames.append(pd.DataFrame({
                "Link": df["Link"].str.strip(),
                "Year": pd.to_numeric(df["Year"], errors="coerce"),
                "Dataset": key,
            }))
        rows = pd.concat(frames, ignore_index=True)
        merged = rows.merge(groups[["Link", "Research Group", "Org Type", "Country"]], on="Link", how="left")
        merged["Research Group"] = merged["Research Group"].fillna("Unknown")
        merged["Org Type"] = merged["Org Type"].fillna("unknown")
        return merged

    def _base_layout(self, title: str, xtitle: str, ytitle: str) -> dict:
        return {
            "title": {"text": title, "font": self.PLOTLY_LAYOUT_DEFAULTS["title"]["font"]},
            "xaxis": {"title": {"text": xtitle}, **self.PLOTLY_LAYOUT_DEFAULTS["xaxis"]},
            "yaxis": {"title": {"text": ytitle}, **self.PLOTLY_LAYOUT_DEFAULTS["yaxis"]},
            "showlegend": True,
            "legend": {**self.PLOTLY_LAYOUT_DEFAULTS["legend"]},
            "font": self.PLOTLY_LAYOUT_DEFAULTS["font"],
            "plot_bgcolor": self.PLOTLY_LAYOUT_DEFAULTS["plot_bgcolor"],
            "paper_bgcolor": self.PLOTLY_LAYOUT_DEFAULTS["paper_bgcolor"],
            "margin": self.PLOTLY_LAYOUT_DEFAULTS["margin"],
            "hovermode": self.PLOTLY_LAYOUT_DEFAULTS["hovermode"],
            "height": self.plot_settings["export"]["height"],
            "width": self.plot_settings["export"]["width"],
        }


class PapersByOrgTypePlot(GroupsPlotBase):
    """Stacked yearly bars of unique papers by organisation type."""

    def create_plot(self):
        papers = self.papers.drop_duplicates("Link").dropna(subset=["Year"])
        papers["Year"] = papers["Year"].astype(int)
        years = list(range(papers["Year"].min(), papers["Year"].max() + 1))
        counts = papers.groupby(["Year", "Org Type"]).size().unstack(fill_value=0).reindex(years, fill_value=0)

        traces = []
        for org in ORG_TYPES:
            if org not in counts.columns or counts[org].sum() == 0:
                continue
            traces.append({
                "type": "bar",
                "name": ORG_LABELS[org],
                "x": [str(y) for y in years],
                "y": counts[org].tolist(),
                "marker": {"color": self.ORG_COLORS.get(org)},
                "hovertemplate": "<b>%{x}</b><br>%{y} %{fullData.name} papers<extra></extra>",
            })

        layout = self._base_layout("Papers per Year by Organisation Type", "Year", "Number of Papers")
        layout["barmode"] = "stack"
        layout["xaxis"]["tickangle"] = -45
        self.fig = go.Figure(data=traces, layout=layout)
        if not self.skip_export:
            self.export_to_multiple(export_name="papers_by_org_type")


class TopResearchGroupsPlot(GroupsPlotBase):
    """Horizontal bars: groups with the most papers, coloured by organisation type."""

    TOP_N = 15

    def create_plot(self):
        papers = self.papers.drop_duplicates(["Link", "Dataset"])
        per_group = papers.groupby("Research Group").agg(
            papers=("Link", "nunique"),
            org=("Org Type", lambda s: s.mode().iat[0] if not s.mode().empty else "unknown"),
        )
        per_group = per_group[per_group.index != "Unknown"].sort_values("papers", ascending=True).tail(self.TOP_N)
        breakdown = papers.groupby(["Research Group", "Dataset"])["Link"].nunique()

        traces = []
        for org in ORG_TYPES:
            subset = per_group[per_group["org"] == org]
            if subset.empty:
                continue
            hover = []
            for name, row in subset.iterrows():
                parts = [f"{DATASET_LABELS[d]}: {n}" for d, n in breakdown.loc[name].items() if n]
                hover.append(f"<b>{name}</b><br>{int(row['papers'])} papers<br>" + "<br>".join(parts))
            traces.append({
                "type": "bar",
                "orientation": "h",
                "name": ORG_LABELS[org],
                "x": subset["papers"].astype(int).tolist(),
                "y": subset.index.tolist(),
                "marker": {"color": self.ORG_COLORS.get(org)},
                "customdata": hover,
                "hovertemplate": "%{customdata}<extra></extra>",
            })

        layout = self._base_layout(f"Top {self.TOP_N} Research Groups by Papers", "Number of Papers", "")
        layout["yaxis"]["categoryorder"] = "array"
        layout["yaxis"]["categoryarray"] = per_group.index.tolist()
        layout["yaxis"]["type"] = "category"
        layout["margin"] = {**layout["margin"], "l": 220}
        self.fig = go.Figure(data=traces, layout=layout)
        if not self.skip_export:
            self.export_to_multiple(export_name="top_research_groups")


def main():
    PapersByOrgTypePlot().create_plot()
    TopResearchGroupsPlot().create_plot()


if __name__ == "__main__":
    main()
