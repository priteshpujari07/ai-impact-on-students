# =============================================================================
#  AI Students Dataset — Data Cleaning Script
#  Libraries : pandas, numpy
#  Dataset   : AI_Students_Clean_Dataset_50K.xlsx  (50,000 rows × 17 columns)
#  Purpose   : Load → Inspect → Clean → Validate → Export
#  Author    : Data Analytics Team
# =============================================================================

import pandas as pd
import numpy as np

# ─────────────────────────────────────────────────────────────────────────────
# STEP 1 — LOAD THE DATASET
# ─────────────────────────────────────────────────────────────────────────────

# Read the Excel file — actual data starts from row 3 (header=2)
df_raw = pd.read_excel("AI_Students_Clean_Dataset_50K.xlsx", header=2)

# Row index 0 contains the real column names; rows below are data
df = df_raw.iloc[1:].reset_index(drop=True)

# Assign clean, code-friendly column names
df.columns = [
    "StudentID",
    "Major",
    "YearOfStudy",
    "PreGPA",
    "PostGPA",
    "GPAChange",
    "WeeklyGenAIHours",
    "PrimaryUseCase",
    "PromptSkillLevel",
    "ToolDiversity",
    "PaidSubscription",
    "TraditionalStudyHours",
    "PerceivedAIDependency",
    "InstitutionalPolicy",
    "ExamAnxiety",
    "SkillRetention",
    "BurnoutRisk",
]

print("=" * 60)
print("STEP 1 — DATASET LOADED SUCCESSFULLY")
print(f"  Rows    : {df.shape[0]:,}")
print(f"  Columns : {df.shape[1]}")
print("=" * 60)


# ─────────────────────────────────────────────────────────────────────────────
# STEP 2 — INITIAL INSPECTION (pandas)
# ─────────────────────────────────────────────────────────────────────────────

print("\n--- 2A. First 5 rows ---")
print(df.head())

print("\n--- 2B. Data types of each column ---")
print(df.dtypes)

print("\n--- 2C. Dataset shape ---")
print(f"  Shape : {df.shape}")

print("\n--- 2D. Column names ---")
print(df.columns.tolist())

print("\n--- 2E. Basic statistics (raw — before type conversion) ---")
print(df.describe(include="all"))


# ─────────────────────────────────────────────────────────────────────────────
# STEP 3 — MISSING VALUE ANALYSIS (pandas + numpy)
# ─────────────────────────────────────────────────────────────────────────────

print("\n--- 3A. Null count per column ---")
null_counts = df.isnull().sum()
print(null_counts)

print("\n--- 3B. Null percentage per column ---")
null_pct = (df.isnull().sum() / len(df)) * 100
print(null_pct.round(2))

print("\n--- 3C. Total missing values in dataset ---")
print(f"  Total missing : {df.isnull().sum().sum()}")

# numpy: boolean mask to find rows that have ANY null value
null_mask = np.any(pd.isnull(df.values), axis=1)
print(f"  Rows with at least one null : {null_mask.sum()}")


# ─────────────────────────────────────────────────────────────────────────────
# STEP 4 — DUPLICATE DETECTION (pandas)
# ─────────────────────────────────────────────────────────────────────────────

print("\n--- 4A. Checking for fully duplicate rows ---")
dup_count = df.duplicated().sum()
print(f"  Duplicate rows found : {dup_count}")

print("\n--- 4B. Checking for duplicate StudentIDs ---")
dup_ids = df.duplicated(subset=["StudentID"]).sum()
print(f"  Duplicate Student IDs : {dup_ids}")

# Drop duplicates if any (keep first occurrence)
df = df.drop_duplicates(subset=["StudentID"], keep="first").reset_index(drop=True)
print(f"  Rows after dropping duplicates : {len(df):,}")


# ─────────────────────────────────────────────────────────────────────────────
# STEP 5 — DATA TYPE CONVERSION (pandas + numpy)
# ─────────────────────────────────────────────────────────────────────────────

# ── 5A. StudentID → string (treat as identifier, not number)
df["StudentID"] = df["StudentID"].astype(str).str.strip()

# ── 5B. Numeric columns — convert from object to float/int
numeric_float_cols = [
    "PreGPA",
    "PostGPA",
    "GPAChange",
    "WeeklyGenAIHours",
    "TraditionalStudyHours",
    "SkillRetention",
]
numeric_int_cols = [
    "ToolDiversity",
    "PerceivedAIDependency",
    "ExamAnxiety",
]

for col in numeric_float_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce").astype(float)

for col in numeric_int_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")
    df[col] = df[col].fillna(df[col].median()).astype(int)

# ── 5C. Categorical string columns — strip whitespace
cat_cols = [
    "Major",
    "YearOfStudy",
    "PrimaryUseCase",
    "PromptSkillLevel",
    "PaidSubscription",
    "InstitutionalPolicy",
    "BurnoutRisk",
]
for col in cat_cols:
    df[col] = df[col].astype(str).str.strip()

print("\n--- 5D. Data types AFTER conversion ---")
print(df.dtypes)


# ─────────────────────────────────────────────────────────────────────────────
# STEP 6 — STRING STANDARDIZATION (pandas)
# ─────────────────────────────────────────────────────────────────────────────

# Title-case categorical columns for consistency
for col in cat_cols:
    df[col] = df[col].str.title()

# Fix known category values that get mangled by title-case
df["PaidSubscription"] = df["PaidSubscription"].replace({"Yes": "Yes", "No": "No"})
df["BurnoutRisk"]      = df["BurnoutRisk"].replace({"High": "High", "Medium": "Medium", "Low": "Low"})

print("\n--- 6. Unique values per categorical column (after standardization) ---")
for col in cat_cols:
    print(f"  {col:28s}: {sorted(df[col].unique().tolist())}")


# ─────────────────────────────────────────────────────────────────────────────
# STEP 7 — OUTLIER DETECTION (numpy + pandas)
# ─────────────────────────────────────────────────────────────────────────────

print("\n--- 7A. Outlier detection using IQR method (numpy) ---")

outlier_summary = {}
for col in numeric_float_cols:
    q1  = np.percentile(df[col].dropna(), 25)
    q3  = np.percentile(df[col].dropna(), 75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    outliers    = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
    outlier_summary[col] = len(outliers)
    print(f"  {col:26s} | Q1={q1:.3f} Q3={q3:.3f} IQR={iqr:.3f} | "
          f"Bounds=[{lower_bound:.3f}, {upper_bound:.3f}] | Outliers={len(outliers)}")

print("\n--- 7B. Outlier detection using Z-score method (numpy) ---")
for col in numeric_float_cols:
    values = df[col].dropna().values
    mean   = np.mean(values)
    std    = np.std(values)
    z_scores       = np.abs((df[col] - mean) / std)
    extreme_count  = (z_scores > 3).sum()
    print(f"  {col:26s} | Mean={mean:.3f} Std={std:.3f} | Z>3 outliers={extreme_count}")


# ─────────────────────────────────────────────────────────────────────────────
# STEP 8 — DATA VALIDATION (pandas + numpy)
# ─────────────────────────────────────────────────────────────────────────────

print("\n--- 8A. GPA Range Validation (should be 0.0 – 4.0) ---")
invalid_pre  = df[(df["PreGPA"]  < 0) | (df["PreGPA"]  > 4.0)]
invalid_post = df[(df["PostGPA"] < 0) | (df["PostGPA"] > 4.0)]
print(f"  PreGPA  out of range [0, 4.0] : {len(invalid_pre)}")
print(f"  PostGPA out of range [0, 4.0] : {len(invalid_post)}")

print("\n--- 8B. GPAChange Consistency Check ---")
# GPAChange should equal PostGPA - PreGPA (within rounding tolerance)
df["_calculated_change"] = (df["PostGPA"] - df["PreGPA"]).round(3)
df["_stored_change"]     = df["GPAChange"].round(3)
mismatch = df[np.abs(df["_calculated_change"] - df["_stored_change"]) > 0.01]
print(f"  GPAChange mismatches found : {len(mismatch)}")
# Drop helper columns
df.drop(columns=["_calculated_change", "_stored_change"], inplace=True)

print("\n--- 8C. Skill Retention Range Validation (should be 0 – 100) ---")
invalid_ret = df[(df["SkillRetention"] < 0) | (df["SkillRetention"] > 100)]
print(f"  SkillRetention out of [0, 100] : {len(invalid_ret)}")

print("\n--- 8D. Weekly GenAI Hours Validation (should be 0 – 40) ---")
invalid_hrs = df[(df["WeeklyGenAIHours"] < 0) | (df["WeeklyGenAIHours"] > 40)]
print(f"  WeeklyGenAIHours out of [0, 40] : {len(invalid_hrs)}")

print("\n--- 8E. ToolDiversity Range Validation (should be 1 – 5) ---")
invalid_td = df[(df["ToolDiversity"] < 1) | (df["ToolDiversity"] > 5)]
print(f"  ToolDiversity out of [1, 5] : {len(invalid_td)}")

print("\n--- 8F. Exam Anxiety & AI Dependency Range (should be 1 – 10) ---")
invalid_ea  = df[(df["ExamAnxiety"]           < 1) | (df["ExamAnxiety"]           > 10)]
invalid_dep = df[(df["PerceivedAIDependency"] < 1) | (df["PerceivedAIDependency"] > 10)]
print(f"  ExamAnxiety out of [1, 10]           : {len(invalid_ea)}")
print(f"  PerceivedAIDependency out of [1, 10] : {len(invalid_dep)}")


# ─────────────────────────────────────────────────────────────────────────────
# STEP 9 — FEATURE ENGINEERING (pandas + numpy)
# ─────────────────────────────────────────────────────────────────────────────

# ── 9A. GPA Improvement flag (1 = improved, 0 = not improved)
df["GPAImproved"] = np.where(df["GPAChange"] > 0, 1, 0)

# ── 9B. AI Usage Category based on weekly hours
df["AIUsageCategory"] = pd.cut(
    df["WeeklyGenAIHours"],
    bins=[-1, 0, 5, 15, 40],
    labels=["No Usage", "Light", "Moderate", "Heavy"],
)

# ── 9C. GPA Performance Band
df["GPABand"] = pd.cut(
    df["PostGPA"],
    bins=[0, 2.0, 2.5, 3.0, 3.5, 4.0],
    labels=["Below 2.0", "2.0–2.5", "2.5–3.0", "3.0–3.5", "3.5–4.0"],
    include_lowest=True,
)

# ── 9D. Study Hours Ratio (AI hours / Traditional hours) — numpy divide
df["AIToTraditionalRatio"] = np.where(
    df["TraditionalStudyHours"] > 0,
    np.round(df["WeeklyGenAIHours"] / df["TraditionalStudyHours"], 3),
    np.nan,
)

# ── 9E. High Risk Flag — student has High Burnout + High AI Dependency (>=7)
df["HighRiskStudent"] = np.where(
    (df["BurnoutRisk"] == "High") & (df["PerceivedAIDependency"] >= 7), 1, 0
)

print("\n--- 9. New engineered columns added ---")
new_cols = ["GPAImproved", "AIUsageCategory", "GPABand", "AIToTraditionalRatio", "HighRiskStudent"]
print(df[new_cols].head(10).to_string())


# ─────────────────────────────────────────────────────────────────────────────
# STEP 10 — DESCRIPTIVE STATISTICS (pandas + numpy)
# ─────────────────────────────────────────────────────────────────────────────

print("\n--- 10A. Full descriptive statistics (numeric columns) ---")
print(df[numeric_float_cols + numeric_int_cols].describe().round(3).to_string())

print("\n--- 10B. Value counts — Major ---")
print(df["Major"].value_counts())

print("\n--- 10C. Value counts — BurnoutRisk ---")
print(df["BurnoutRisk"].value_counts())

print("\n--- 10D. Value counts — YearOfStudy ---")
print(df["YearOfStudy"].value_counts())

print("\n--- 10E. Value counts — AIUsageCategory ---")
print(df["AIUsageCategory"].value_counts())

print("\n--- 10F. Correlation matrix (numpy) ---")
num_data   = df[numeric_float_cols].dropna()
corr_matrix = np.corrcoef(num_data.T)
corr_df     = pd.DataFrame(corr_matrix, index=numeric_float_cols, columns=numeric_float_cols)
print(corr_df.round(3).to_string())

print("\n--- 10G. Group-by: Average GPA Change by Major ---")
print(df.groupby("Major")["GPAChange"].agg(["mean", "median", "std", "count"]).round(3))

print("\n--- 10H. Group-by: Burnout Risk by Prompt Skill Level ---")
print(df.groupby(["PromptSkillLevel", "BurnoutRisk"])["StudentID"].count().unstack(fill_value=0))

print("\n--- 10I. Pivot Table: Avg Skill Retention by Major & Year ---")
pivot = df.pivot_table(
    values="SkillRetention",
    index="Major",
    columns="YearOfStudy",
    aggfunc=np.mean,
).round(2)
print(pivot.to_string())

print("\n--- 10J. numpy: Mean, Median, Std for all numeric columns ---")
for col in numeric_float_cols:
    arr = df[col].dropna().values
    print(f"  {col:30s} | mean={np.mean(arr):.3f}  "
          f"median={np.median(arr):.3f}  std={np.std(arr):.3f}  "
          f"min={np.min(arr):.3f}  max={np.max(arr):.3f}")


# ─────────────────────────────────────────────────────────────────────────────
# STEP 11 — FINAL CLEANED DATASET SUMMARY
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 60)
print("STEP 11 — FINAL CLEANED DATASET SUMMARY")
print("=" * 60)
print(f"  Total rows              : {len(df):,}")
print(f"  Total columns           : {len(df.columns)}")
print(f"  Original columns        : 17")
print(f"  Engineered columns added: 5")
print(f"  Missing values remaining: {df.isnull().sum().sum()}")
print(f"  Duplicate rows remaining: {df.duplicated().sum()}")
print(f"  % Students GPA Improved : {df['GPAImproved'].mean()*100:.1f}%")
print(f"  High Risk Students      : {df['HighRiskStudent'].sum():,}")
print("=" * 60)

print("\n--- Final column list ---")
for i, col in enumerate(df.columns, 1):
    print(f"  {i:02d}. {col}")


# ─────────────────────────────────────────────────────────────────────────────
# STEP 12 — EXPORT CLEANED FILE (pandas)
# ─────────────────────────────────────────────────────────────────────────────

# Export full cleaned dataset
output_file = "AI_Students_Cleaned.xlsx"
df.to_excel(output_file, index=False)
print(f"\n✅  Cleaned dataset exported → {output_file}")

# Export summary statistics sheet
summary_stats = df[numeric_float_cols + numeric_int_cols].describe().round(3)
with pd.ExcelWriter("AI_Students_Summary_Statistics.xlsx", engine="openpyxl") as writer:
    summary_stats.to_excel(writer, sheet_name="Descriptive Stats")
    df.groupby("Major")["GPAChange"].agg(["mean", "median", "std", "count"]).round(3).to_excel(
        writer, sheet_name="GPA by Major"
    )
    df.groupby("BurnoutRisk")["SkillRetention"].agg(["mean", "std", "count"]).round(3).to_excel(
        writer, sheet_name="Retention by Burnout"
    )
    df.groupby("InstitutionalPolicy")["GPAChange"].agg(["mean", "std", "count"]).round(3).to_excel(
        writer, sheet_name="GPA by Policy"
    )
    df.groupby("PaidSubscription")[["GPAChange", "SkillRetention"]].mean().round(3).to_excel(
        writer, sheet_name="Paid vs Free"
    )
    df["AIUsageCategory"].value_counts().to_excel(
        writer, sheet_name="AI Usage Distribution"
    )

print("✅  Summary statistics exported → AI_Students_Summary_Statistics.xlsx")
print("\n🎯  All cleaning steps complete. Ready to submit to HR & College.\n")
