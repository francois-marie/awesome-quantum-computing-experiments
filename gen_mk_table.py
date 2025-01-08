import pandas as pd

# Paths to the CSV files and README.md
qec_csv_path = "data/qec_exp.csv"
msd_csv_path = "data/msd_exp.csv"
entangled_csv_path = "data/entangled_state_error_exp.csv"
readme_path = "README.md"

# Load CSV files
qec_data = pd.read_csv(qec_csv_path)
msd_data = pd.read_csv(msd_csv_path)
entangled_data = pd.read_csv(entangled_csv_path)


# Function to format entries in the markdown
def format_entry(row, section: str):
    if pd.isna(row["Notes"]):
        suffix = ""
    else:
        suffix = f", {row['Notes']}"
    if section == "qec":
        return f"- [{row['Article Title']}]({row['Link']}) ({row['Year']}) - {row['Code Parameters']} on {row['Platform']}{suffix}"
    elif section == "msd":
        return f"- [{row['Article Title']}]({row['Link']}) ({row['Year']}) - on {row['Platform']}{suffix}"
    elif section == "entangled":
        return f"- [{row['Article Title']}]({row['Link']}) ({row['Year']}) - {row['Entangled State Error']} on {row['Platform']}{suffix}"
    else:
        raise NotImplementedError(f"The section type {section} is incorrect.")


# Generate content for Quantum Error Correction section
qec_section = "## Quantum Error Correction\n\n"
qec_toc = ""

for code_name, group in qec_data.sort_values(by=["Year", "Article Title"]).groupby(
    "Code Name", sort=False
):
    anchor = (
        code_name.lower()
        .replace(" ", "-")
        .replace("[", "")
        .replace("]", "")
        .replace(",", "")
    )
    qec_toc += f"\t- [{code_name}](#{anchor})\n"
    qec_section += f"### {code_name}\n\n"
    entries = group.apply(format_entry, args=("qec",), axis=1)
    qec_section += "\n".join(entries) + "\n\n"

# Generate content for Magic State Distillation section
msd_section = "## Magic State Distillation\n\n"
msd_toc = ""

for code_name, group in msd_data.sort_values(by=["Year", "Article Title"]).groupby(
    "Code Name", sort=False
):
    anchor = (
        code_name.lower()
        .replace(" ", "-")
        .replace("[", "")
        .replace("]", "")
        .replace(",", "")
    )
    msd_toc += f"\t- [{code_name}](#{anchor})\n"
    msd_section += f"### {code_name}\n\n"
    entries = group.apply(format_entry, args=("msd",), axis=1)
    msd_section += "\n".join(entries) + "\n\n"


# Generate content for Entangled State Error section
entangled_section = "## Entangled State Error\n\n"
entangled_toc = ""

for platform, group in entangled_data.sort_values(by=["Year", "Article Title"]).groupby(
    "Platform", sort=False
):
    anchor = (
        platform.lower()
        .replace(" ", "-")
        .replace("[", "")
        .replace("]", "")
        .replace(",", "")
    )
    entangled_toc += f"\t- [{platform}](#{anchor})\n"
    entangled_section += f"### {platform}\n\n"
    entries = group.apply(format_entry, args=("entangled",), axis=1)
    entangled_section += "\n".join(entries) + "\n\n"


# Define README structure
readme_content = f"""# Awesome Quantum Computing Experiments

A curated list of notable quantum computing experiments, focused primarily on the implementation of quantum error correction codes.

![Plot](out/qec_exp.png)
![Plot](out/qec_time_evolution.png)
![Plot](out/entangled_state_error_vs_year.png)

## Table of Contents

- [Quantum Error Correction](#quantum-error-correction)
{qec_toc}
- [Magic State Distillation](#magic-state-distillation)
{msd_toc}
- [Entangled State Error](#entangled-state-error)
{entangled_toc}

{qec_section}

{msd_section}

{entangled_section}

## Contributing

Contributions are welcome! If you have suggestions for new entries, please submit a pull request or open an issue.

## License

This work is licensed under a [CC0 1.0 Universal (Public Domain Dedication)](LICENSE).
To the extent possible under law, the authors have dedicated all copyright and related and neighboring rights to this work to the public domain worldwide.
For more information, see [Creative Commons CC0 1.0 Legal Code](https://creativecommons.org/publicdomain/zero/1.0/).
"""

# Write to README.md
with open(readme_path, "w") as f:
    f.write(readme_content)

print("README.md has been successfully updated.")
