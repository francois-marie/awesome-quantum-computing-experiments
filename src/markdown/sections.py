from .base import ExperimentSection
import pandas as pd

class QECSection(ExperimentSection):
    """Generator for Quantum Error Correction section."""
    
    def _format_code_parameters(self, row) -> str:
        """Format code parameters with special handling for repetition codes."""
        code_name = row['Code Name'].lower()
        code_params = row['Code Parameters']
        
        # Special handling for repetition codes with single brackets
        if ( code_params.startswith('[') and 
            not code_params.startswith('[[')):
            return f"{code_params}, d=1"
        
        return code_params
    
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
                formatted_params = self._format_code_parameters(row)
                content += (f"- [{row['Article Title']}]({row['Link']}) ({row['Year']}) - "
                          f"{formatted_params} on {row['Platform']}{suffix}\n")
            content += "\n"
        return content

class MSDSection(ExperimentSection):
    """Generator for Magic State section."""

    def __init__(self, data: pd.DataFrame):
        super().__init__(data)
        # Clean all columns - replace empty strings with NaN but don't forward fill
        for col in self.data.columns:
            if self.data[col].dtype == 'object':  # Only for string columns
                self.data[col] = self.data[col].replace("", pd.NA)
        
        self._setup_experiment_types()

    def _setup_experiment_types(self):
        """Set up experiment type classifications."""
        if "Experiment Type" in self.data.columns and not self.data["Experiment Type"].isna().all():
            self._setup_from_existing_types()
        else:
            self._setup_from_title_classification()

    def _setup_from_existing_types(self):
        """Setup experiment types from existing CSV column."""
        def get_experiment_types(row):
            exp_type = row.get("Experiment Type", "")
            if pd.isna(exp_type):
                return self._classify_from_title(row['Article Title'])
            
            # Handle compound types - experiments can belong to multiple categories
            exp_type = str(exp_type).strip().lower()
            types = []
            
            if 'preparation' in exp_type:
                types.append('Preparation')
            if 'distillation' in exp_type:
                types.append('Distillation')
            if 'code switching' in exp_type:
                types.append('Code Switching')
            if 'injection' in exp_type:
                types.append('Preparation')  # Treat injection as preparation
            
            return types if types else ['Preparation']
        
        self._create_boolean_columns(get_experiment_types)

    def _setup_from_title_classification(self):
        """Setup experiment types from article titles."""
        def get_experiment_types(row):
            return [self._classify_from_title(row['Article Title'])]
        
        self._create_boolean_columns(get_experiment_types)

    def _classify_from_title(self, title):
        """Classify experiment type from article title."""
        title = title.lower()
        if 'code switching' in title:
            return 'Code Switching'
        if 'distillation' in title or 'purification' in title:
            return 'Distillation'
        return 'Preparation'

    def _create_boolean_columns(self, get_experiment_types_func):
        """Create boolean columns for experiment types."""
        self.data['Is_Preparation'] = False
        self.data['Is_Distillation'] = False
        self.data['Is_Code_Switching'] = False

        if self.data.empty:
            self.data['Experiment Type'] = pd.Series(dtype='object')
            return

        for idx, row in self.data.iterrows():
            types = get_experiment_types_func(row)
            self.data.loc[idx, 'Is_Preparation'] = 'Preparation' in types
            self.data.loc[idx, 'Is_Distillation'] = 'Distillation' in types
            self.data.loc[idx, 'Is_Code_Switching'] = 'Code Switching' in types

        # Keep the primary experiment type for backward compatibility
        self.data['Experiment Type'] = self.data.apply(
            lambda row: get_experiment_types_func(row)[0], axis=1
        )

    def _get_non_empty_values(self, data, column):
        """Get sorted list of non-empty values from a column."""
        return sorted([val for val in data[column].unique() 
                      if pd.notna(val) and str(val).strip()])

    def _split_by_column_presence(self, data, column):
        """Split data into groups with and without values in specified column."""
        has_value = data[data[column].notna() & (data[column].astype(str).str.strip() != "")]
        no_value = data[data[column].isna() | (data[column].astype(str).str.strip() == "")]
        return has_value, no_value

    def generate_toc(self) -> str:
        toc = ""
        
        preparation_data = self.data[self.data['Is_Preparation']]
        distillation_data = self.data[self.data['Is_Distillation']]
        code_switching_data = self.data[self.data['Is_Code_Switching']]

        if not preparation_data.empty:
            toc += "\t- [Preparation](#preparation)\n"
            magic_states = self._get_non_empty_values(preparation_data, "Magic State")
            for magic_state in magic_states:
                header = f"Magic State: {magic_state}"
                anchor = self.format_anchor(header)
                toc += f"\t\t- [{magic_state}](#{anchor})\n"

        if not distillation_data.empty:
            toc += "\t- [Distillation](#distillation)\n"
            protocols = self._get_non_empty_values(distillation_data, "MSD Protocol")
            for protocol in protocols:
                header = f"Protocol: {protocol}"
                anchor = self.format_anchor(header)
                toc += f"\t\t- [{protocol}](#{anchor})\n"

        if not code_switching_data.empty:
            toc += "\t- [Code Switching](#code-switching)\n"
        return toc

    def _generate_grouped_content(self, data, group_column, header_prefix):
        """Generate content for data grouped by a specific column."""
        content = ""
        grouped_data, ungrouped_data = self._split_by_column_presence(data, group_column)
        
        # Add grouped experiments
        for value, group in grouped_data.sort_values(by=["Year", "Article Title"]).groupby(group_column, sort=False):
            header = f"{header_prefix}: {value}"
            content += f"#### {header}\n\n"
            content += self._generate_list_items(group)
        
        # Add ungrouped experiments
        if not ungrouped_data.empty:
            sorted_ungrouped = ungrouped_data.sort_values(by=["Year", "Article Title"])
            content += self._generate_list_items(sorted_ungrouped)
        
        return content

    def generate_content(self) -> str:
        """Generate the complete Magic State section content."""
        content = "## Magic State\n\n"
        
        # Add detailed explanation of magic states
        content += "Magic states are crucial non-Clifford quantum states that enable universal fault-tolerant quantum computation. The main magic states used in experiments are:\n\n"
        content += "- T-gate: $T = \\frac{1}{\\sqrt{2}}\\left(|0\\rangle + e^{i\\pi/4}|1\\rangle\\right)$\n"
        content += "- Hadamard: $H = \\cos(\\pi/8)|0\\rangle + \\sin(\\pi/8)|1\\rangle$\n"
        content += "- M: $M = \\cos(\\theta/2)|0\\rangle + e^{i\\pi/4}\\sin(\\theta/2)|1\\rangle$ with $\\theta = \\cos^{-1}(1/\\sqrt{3})$\n"
        content += "- CZ: $CZ = \\frac{1}{\\sqrt{3}}\\left(|00\\rangle + |10\\rangle + |01\\rangle\\right)$\n\n"
        
        preparation_data = self.data[self.data['Is_Preparation']]
        if not preparation_data.empty:
            content += "### Preparation\n\n"
            content += self._generate_grouped_content(preparation_data, "Magic State", "Magic State")
        
        distillation_data = self.data[self.data['Is_Distillation']]
        if not distillation_data.empty:
            content += "### Distillation\n\n"
            content += self._generate_grouped_content(distillation_data, "MSD Protocol", "Protocol")

        code_switching_data = self.data[self.data['Is_Code_Switching']]
        if not code_switching_data.empty:
            content += "### Code Switching\n\n"
            sorted_code_switching_data = code_switching_data.sort_values(by=["Year", "Article Title"])
            content += self._generate_list_items(sorted_code_switching_data)

        return content

    def _generate_list_items(self, group: pd.DataFrame) -> str:
        items = ""
        for _, row in group.iterrows():
            details = []
            
            # Only add protocol for distillation experiments
            if (row.get('Experiment Type') == 'Distillation' and 
                "MSD Protocol" in row and pd.notna(row["MSD Protocol"])):
                details.append(f"protocol: {row['MSD Protocol']}")

            # Only add QEC code if it's actually present in the original data
            if "QEC Code" in row and pd.notna(row["QEC Code"]) and row["QEC Code"].strip():
                qec_code = row["QEC Code"]
                if 'code switching' in row['Article Title'].lower() and ',' in qec_code:
                    qec_code = qec_code.replace(',', ' ->', 1)
                details.append(f"QEC code: {qec_code}")

            # Only add magic state if it's actually present in the original data
            if "Magic State" in row and pd.notna(row["Magic State"]) and row["Magic State"].strip():
                details.append(f"magic state: {row['Magic State']}")
            
            # Only add fidelity if it's actually present in the original data
            if "Fidelity" in row and pd.notna(row["Fidelity"]) and row["Fidelity"].strip():
                details.append(f"fidelity: {row['Fidelity']}")
            
            # Only add acceptance rate if it's actually present in the original data
            if "Acceptance Rate (%)" in row and pd.notna(row["Acceptance Rate (%)"]) and str(row["Acceptance Rate (%)"]).strip():
                details.append(f"acceptance rate: {row['Acceptance Rate (%)']}%")
            
            # Only add post selection if it's explicitly "Yes"
            if "Post selection" in row and row["Post selection"] == "Yes":
                details.append("post-selected")

            details_str = ", ".join(details)
            notes = f", {row['Notes']}" if "Notes" in row and pd.notna(row["Notes"]) and row["Notes"].strip() else ""

            line = f"- [{row['Article Title']}]({row['Link']}) ({row['Year']}) - on {row['Platform']}"
            if details_str:
                line += f", {details_str}"
            line += f"{notes}\n"
            items += line
        return items

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