import pandas as pd

# Paths to the CSV files and README.md
qec_csv_path = "data/qec_exp.csv"
readme_path = "README.md"

# Load CSV files
qec_data = pd.read_csv(qec_csv_path)


# Function to format entries in the markdown
def format_entry(row):
    if pd.isna(row["Notes"]):
        suffix = ""
    else:
        suffix = f", {row['Notes']}"
    return f"- [{row['Article Title']}]({row['Link']}) ({row['Year']}) - {row['Code Parameters']} on {row['Platform']}{suffix}"


# Generate content for Quantum Error Correction section
qec_section = "## Quantum Error Correction\n\n"
qec_toc = ""

for code_name, group in qec_data.sort_values("Year").groupby("Code Name", sort=False):
    anchor = (
        code_name.lower()
        .replace(" ", "-")
        .replace("[", "")
        .replace("]", "")
        .replace(",", "")
    )
    qec_toc += f"\t- [{code_name}](#{anchor})\n"
    qec_section += f"### {code_name}\n\n"
    entries = group.apply(format_entry, axis=1)
    qec_section += "\n".join(entries) + "\n\n"

# Define README structure
readme_content = f"""# Awesome Quantum Computing Experiments

A curated list of notable quantum computing experiments, focused primarily on the implementation of quantum error correction codes.

![Plot](out/qec_exp.png)
![Plot](out/qec_time_evolution.png)

## Table of Contents

- [Quantum Error Correction](#quantum-error-correction)
{qec_toc}

{qec_section}

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
