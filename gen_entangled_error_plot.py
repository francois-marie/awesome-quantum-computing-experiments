import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
file_path = "data/entangled_state_error_exp.csv"
data = pd.read_csv(file_path)

# Preprocessing: Ensure proper data types
data["Year"] = pd.to_numeric(data["Year"], errors="coerce")  # Convert year to numeric
data["Entangled State Error"] = pd.to_numeric(
    data["Entangled State Error"], errors="coerce"
)  # Convert error to numeric

# Set up the plot
plt.figure()
sns.lineplot(
    x="Year",
    y="Entangled State Error",
    hue="Platform",
    marker="o",
    data=data,
    palette="tab10",
    linewidth=2,
    alpha=0.8,
)

# Customize the plot
plt.title("Entangled State Error vs. Year", fontsize=16)
plt.xlabel("Year", fontsize=14)
plt.ylabel("Entangled State Error", fontsize=14)
plt.yscale("log")  # Use logarithmic scale for better visibility
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.legend(title="Platform", fontsize=12, loc="lower left")
plt.grid(axis="y", linestyle="--", alpha=0.6)

# Show and save the plot
plt.tight_layout()
plt.savefig("out/entangled_state_error_vs_year.png")
plt.show()
