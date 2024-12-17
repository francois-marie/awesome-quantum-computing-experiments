import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import colormaps
import re

# Read the CSV file
df = pd.read_csv("data/qec_exp.csv")


# Function to parse code parameters and extract n, k, d
def parse_code_parameters(params):
    # Remove all spaces
    params = params.replace(" ", "")
    # Split on commas separating different code parameters
    code_params_list = re.split(r",(?=\[)", params)
    n_list = []
    k_list = []
    d_list = []
    for code_param in code_params_list:
        if code_param == "1Dwith12qubits":
            continue
        # Remove leading/trailing brackets
        code_param = code_param.strip("[]")
        # Remove text
        code_param = code_param.replace("surfacecode", "").replace("toriccode", "")
        # Split on hyphens in case of multiple codes like [3,1,3]-[5,1,5]
        codes = code_param.split("-")
        for code in codes:
            # Remove any nested brackets
            code = code.strip("[]")
            try:
                n, k, d = code.split(",")
                n_list.append(int(n))
                k_list.append(int(k))
                d_list.append(int(d))
            except Exception as e:
                print(f"Error parsing code parameters '{code}': {e}")
    return n_list, k_list, d_list


# Initialize lists to store parsed data
n_values = []
k_values = []
d_values = []
code_names = []
platforms = []

# Iterate over each row and extract code parameters
for idx, row in df.iterrows():
    code_params = row["Code Parameters"]
    n_list, k_list, d_list = parse_code_parameters(code_params)
    for n, k, d in zip(n_list, k_list, d_list):
        n_values.append(n)
        k_values.append(k)
        d_values.append(d)
        code_names.append(row["Code Name"])
        platforms.append(row["Platform"])

# Create a new DataFrame with extracted values
data = pd.DataFrame(
    {
        "n": n_values,
        "k": k_values,
        "d": d_values,
        "Code Name": code_names,
        "Platform": platforms,
    }
)

# Set the seaborn theme
sns.set(style="whitegrid")

# Create a 3D scatter plot
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection="3d")

# Map 'Code Name' to colors
code_names_unique = data["Code Name"].unique()
colors = colormaps.get_cmap("tab20").resampled(len(code_names_unique))
color_map = dict(zip(code_names_unique, colors.colors))

x_key, x_label = "n", "n (Code Length)"
z_key, z_label = "k", "k (Number of Logical Qubits)"
y_key, y_label = "d", "d (Code Distance)"

# Plot each code type with a different color
for code_name in code_names_unique:
    subset = data[data["Code Name"] == code_name]
    ax.scatter(
        subset[x_key],
        subset[y_key],
        subset[z_key],
        color=color_map[code_name],
        label=code_name,
        s=50,
        edgecolors="k",
    )

ax.set_xlabel(x_label)
ax.set_ylabel(y_label)
ax.set_zlabel(z_label)
ax.set_title("Quantum Error Correction Codes")

ax.legend(loc="upper left", bbox_to_anchor=(1.05, 1))
plt.tight_layout()
plt.show()
