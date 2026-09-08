from abc import ABC, abstractmethod
import re
import pandas as pd
from typing import List, Optional

class BaseSection(ABC):
    """Base class for markdown section generators."""
    
    def __init__(self, data: pd.DataFrame):
        self.data = data
        
    @abstractmethod
    def generate_toc(self) -> str:
        """Generate table of contents entries."""
        pass
        
    @abstractmethod
    def generate_content(self) -> str:
        """Generate the main content of the section."""
        pass
        
    @staticmethod
    def format_anchor(text: str) -> str:
        """Format heading text into a GitHub-style markdown anchor."""
        text = text.strip().lower()
        text = re.sub(r"[^\w\s-]", "", text)
        return re.sub(r"\s", "-", text)

class ExperimentSection(BaseSection):
    """Base class for experiment sections with common formatting."""
    
    def format_entry(self, row: pd.Series) -> str:
        """Format a basic experiment entry."""
        suffix = f", {row['Notes']}" if not pd.isna(row.get('Notes')) else ""
        return f"- [{row['Article Title']}]({row['Link']}) ({row['Year']}){suffix}" 