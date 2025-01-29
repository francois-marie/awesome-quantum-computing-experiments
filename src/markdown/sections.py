from .base import ExperimentSection
import pandas as pd

class QECSection(ExperimentSection):
    """Generator for Quantum Error Correction section."""
    
    def generate_toc(self) -> str:
        toc = ""
        for code_name in self.data.sort_values(by=["Year", "Article Title"])["Code Name"].unique():
            anchor = self.format_anchor(code_name)
            toc += f"\t- [{code_name}](#{anchor})\n"
        return toc
    
    def generate_content(self) -> str:
        content = "## Quantum Error Correction\n\n"
        for code_name, group in self.data.sort_values(
            by=["Year", "Article Title"]
        ).groupby("Code Name", sort=False):
            content += f"### {code_name}\n\n"
            for _, row in group.iterrows():
                suffix = f", {row['Notes']}" if not pd.isna(row.get('Notes')) else ""
                content += (f"- [{row['Article Title']}]({row['Link']}) ({row['Year']}) - "
                          f"{row['Code Parameters']} on {row['Platform']}{suffix}\n")
            content += "\n"
        return content

class MSDSection(ExperimentSection):
    """Generator for Magic State Distillation section."""
    
    def generate_toc(self) -> str:
        toc = ""
        for code_name in self.data.sort_values(by=["Year", "Article Title"])["Code Name"].unique():
            anchor = self.format_anchor(code_name)
            toc += f"\t- [{code_name}](#{anchor})\n"
        return toc
    
    def generate_content(self) -> str:
        content = "## Magic State Distillation\n\n"
        for code_name, group in self.data.sort_values(
            by=["Year", "Article Title"]
        ).groupby("Code Name", sort=False):
            content += f"### {code_name}\n\n"
            for _, row in group.iterrows():
                suffix = f", {row['Notes']}" if not pd.isna(row.get('Notes')) else ""
                content += (f"- [{row['Article Title']}]({row['Link']}) ({row['Year']}) - "
                          f"on {row['Platform']}{suffix}\n")
            content += "\n"
        return content

class EntangledSection(ExperimentSection):
    """Generator for Entangled State Error section."""
    
    def generate_toc(self) -> str:
        toc = ""
        for platform in self.data.sort_values(by=["Year", "Article Title"])["Platform"].unique():
            anchor = self.format_anchor(platform)
            toc += f"\t- [{platform}](#{anchor})\n"
        return toc
    
    def generate_content(self) -> str:
        content = "## Entangled State Error\n\n"
        for platform, group in self.data.sort_values(
            by=["Year", "Article Title"]
        ).groupby("Platform", sort=False):
            content += f"### {platform}\n\n"
            for _, row in group.iterrows():
                suffix = f", {row['Notes']}" if not pd.isna(row.get('Notes')) else ""
                content += (f"- [{row['Article Title']}]({row['Link']}) ({row['Year']}) - "
                          f"{row['Entangled State Error']} on {row['Platform']}{suffix}\n")
            content += "\n"
        return content

class QubitCountSection(ExperimentSection):
    """Generator for Qubit Count section."""
    
    def generate_toc(self) -> str:
        toc = ""
        for platform in self.data.sort_values(by=["Year", "Article Title"])["Platform"].unique():
            anchor = self.format_anchor(platform)
            toc += f"\t- [{platform}](#{anchor})\n"
        return toc
    
    def generate_content(self) -> str:
        content = "## Qubit Count\n\n"
        for platform, group in self.data.sort_values(
            by=["Year", "Article Title"]
        ).groupby("Platform", sort=False):
            content += f"### {platform}\n\n"
            for _, row in group.iterrows():
                suffix = f", {row['Notes']}" if not pd.isna(row.get('Notes')) else ""
                content += (f"- [{row['Article Title']}]({row['Link']}) ({row['Year']}) - "
                          f"{row['Number of qubits']} qubits on {row['Platform']}{suffix}\n")
            content += "\n"
        return content

class PhysicalQubitsSection(ExperimentSection):
    """Generator for Physical Qubits section."""
    
    def __init__(self, data: pd.DataFrame):
        super().__init__(data)  # Pass the data directly to the base class
    
    def generate_toc(self) -> str:
        toc = ""
        for platform in self.data.sort_values(by=["Year", "Article Title"])["Platform"].unique():
            anchor = self.format_anchor(platform)
            toc += f"\t- [{platform}](#{anchor})\n"
        return toc
    
    def generate_content(self) -> str:
        content = "## Physical Qubits\n\n"
        for platform, group in self.data.sort_values(
            by=["Year", "Article Title"]
        ).groupby("Platform", sort=False):
            content += f"### {platform}\n\n"
            for _, row in group.iterrows():
                # Build coherence time string
                coherence_times = []
                if not pd.isna(row.get('T1')):
                    coherence_times.append(f"T1: {row['T1']}s")
                if not pd.isna(row.get('T2')):
                    coherence_times.append(f"T2: {row['T2']}s")
                coherence_str = ", ".join(coherence_times)
                
                # Build the entry string
                if row.get('Link') and not pd.isna(row['Link']):
                    title_str = f"[{row['Article Title']}]({row['Link']})"
                else:
                    title_str = row['Article Title'] if not pd.isna(row['Article Title']) else row['Code Name']
                
                suffix = f", {row['Notes']}" if not pd.isna(row.get('Notes')) else ""
                content += (f"- {title_str} ({row['Year']}) - {row['Code Name']}, "
                          f"{coherence_str} on {row['Platform']}{suffix}\n")
            content += "\n"
        return content 