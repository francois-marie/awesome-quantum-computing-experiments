import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
file_path = "data/qubit_count.csv"
data = pd.read_csv(file_path)

# Preprocessing: Ensure proper data types
data["Year"] = pd.to_numeric(data["Year"], errors="coerce")  # Convert year to numeric
data["Number of qubits"] = pd.to_numeric(
    data["Number of qubits"], errors="coerce"
)  # Convert qubit count to numeric

# Set up the plot
plt.figure()
sns.lineplot(
    x="Year",
    y="Number of qubits",
    hue="Platform",
    marker="o",
    data=data,
    palette="tab10",
    linewidth=2,
    alpha=0.8,
)

# Customize the plot
plt.title("Number of Qubits vs. Year by Platform", fontsize=16)
plt.xlabel("Year", fontsize=14)
plt.ylabel("Number of Qubits", fontsize=14)
plt.yscale("log")  # Use logarithmic scale for better visibility
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.legend(title="Platform", fontsize=12, loc="upper left")
plt.grid(axis="y", linestyle="--", alpha=0.6)

# Show and save the plot
plt.tight_layout()
plt.savefig("out/qubit_count_vs_year.png")
plt.show() 