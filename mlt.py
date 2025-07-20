import re
import pandas as pd
import json

# Step 1: Read SQL file
with open("data.sql", "r", encoding="utf-8") as f:
    sql_text = f.read()

# Step 2: Extract INSERT values (e.g., 'S02', 786, 879, 62, 9, 48644)
matches = re.findall(r"INSERT INTO retail_data VALUES\s*\((.*?)\);", sql_text, re.DOTALL)
if not matches:
    matches = re.findall(r"VALUES\s*\((.*?)\)", sql_text)

# Step 3: Parse each row
rows = []
for line in matches:
    # Remove parentheses if present and split by comma
    parts = [x.strip().strip("'") for x in line.split(",")]
    if len(parts) == 6:  # Ensure valid row
        rows.append(parts)

# Step 4: Convert to DataFrame
df = pd.DataFrame(rows, columns=["Store_ID", "Footfall", "Promo_Spend", "Avg_Basket", "Returns", "Net_Sales"])

# Step 5: Convert relevant columns to numeric
df["Net_Sales"] = df["Net_Sales"].astype(float)
df["Avg_Basket"] = df["Avg_Basket"].astype(float)
df["Footfall"] = df["Footfall"].astype(float)

# Step 6: Compute correlation matrix
corr = df[["Avg_Basket", "Net_Sales", "Footfall"]].corr()

# Step 7: Extract required correlations
correlations = {
    "Avg_Basket-Net_Sales": corr.loc["Avg_Basket", "Net_Sales"],
    "Avg_Basket-Footfall": corr.loc["Avg_Basket", "Footfall"],
    "Net_Sales-Footfall": corr.loc["Net_Sales", "Footfall"]
}

# Step 8: Find the strongest (absolute) correlation
strongest_pair = max(correlations.items(), key=lambda x: abs(x[1]))
result = {
    "pair": strongest_pair[0],
    "correlation": round(strongest_pair[1], 2)
}

# Step 9: Write to JSON file
with open("result.json", "w") as f:
    json.dump(result, f)

print("✅ JSON file created: result.json")
print(result)
