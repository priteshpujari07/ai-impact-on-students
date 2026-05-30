# 🎓 AI Impact on Students — Data Analysis & Interactive Dashboard

> **Is AI a Tutor or a Cheat Code?**
> A full end-to-end data analysis project on 50,000 student records exploring how Generative AI tools affect academic performance, burnout, and skill retention.

---

## 📌 Project Overview

This project analyzes the real-world impact of AI tools (ChatGPT, Copilot, Gemini, etc.) on student academic outcomes across 5 major disciplines. It covers the complete data analytics pipeline — from raw data cleaning to an interactive executive dashboard built for CEO/CFO-level presentation.

| Item | Detail |
|------|--------|
| 📊 Dataset | [AI Impact on Students — Kaggle](https://www.kaggle.com/datasets/laveshjadon/ai-impact-on-students) |
| 📁 Records | 50,000 students × 17 features |
| 🧰 Tools Used | Python · pandas · numpy · Chart.js · HTML/CSS/JS |
| 🎯 Goal | Clean data → Analyze → Visualize → Present insights |

---

## 📂 Repository Structure

```
ai-impact-on-students/
│
├── 📄 README.md                          ← You are here
│
├── 📊 data/
│   ├── AI_Students_Clean_Dataset_50K.xlsx   ← Raw dataset (from Kaggle)
│   └── AI_Students_Cleaned.xlsx             ← Cleaned + engineered dataset
│
├── 🐍 scripts/
│   └── data_cleaning_script.py              ← Full pandas & numpy cleaning pipeline
│
├── 📈 dashboard/
│   └── ai_students_dashboard.html           ← Interactive executive dashboard
│
└── 📋 outputs/
    └── AI_Students_Summary_Statistics.xlsx  ← Summary stats (6 analysis sheets)
```

---

## 🔍 Key Insights from the Data

### 1. 📈 AI Helps — But Not Equally
- **87.5%** of students improved their GPA after using AI tools
- Average GPA improvement: **+0.203 points** across all majors
- **STEM students** benefit the most (avg +0.217), followed by Medical (+0.201)

### 2. 🔥 STEM Has the Highest Burnout Risk
- **30%** of STEM students are in the High Burnout category
- Humanities students have the lowest burnout rate at **20.7%**
- Burnout is NOT caused by skill level — Advanced, Intermediate & Beginner students all show ~25% high burnout

### 3. 🏛️ Institutional Policy Matters More Than Expected
- Schools with a **Strict Ban** on AI → students show **29.8% burnout** and lowest GPA change (+0.187)
- Schools that **Allowed AI With Citation** → best GPA outcomes (+0.208)
- Banning AI increases student stress without improving academic results

### 4. 🧠 HOW You Use AI Matters More Than How Much
- Students using AI for **Debugging / Troubleshooting** get the highest GPA gains (+0.249)
- Students using AI for **Direct Answer Generation** get the lowest (+0.133)
- The use case, not the hours, drives academic improvement

### 5. ⚠️ Heavy AI Use Hurts Skill Retention
- Students with **No AI usage**: Skill Retention = **77.6%**
- Students with **Heavy AI usage (15–40 hrs/wk)**: Skill Retention drops to **72.7%**
- Moderate usage (5–15 hrs/wk) shows the best balance: GPA +0.227 with 77% retention

### 6. 📚 Traditional Study > AI Hours for GPA
- Correlation of **Traditional Study Hours → GPA Change: r = +0.376**
- Correlation of **GenAI Hours → GPA Change: r = −0.047**
- Traditional study still drives academic performance; AI is a supplement, not a replacement

### 7. 💰 Paid Subscriptions: Marginal Edge
- Paid users: avg GPA change = **+0.207**
- Free users: avg GPA change = **+0.200**
- Difference is small — the tool matters less than how the student uses it

### 8. 🚨 4.7% Students Are High-Risk
- **2,330 students** have both High Burnout AND High AI Dependency (score ≥ 7)
- These students need targeted intervention from institutions

---

## 🛠️ Data Cleaning Pipeline

**File:** `scripts/data_cleaning_script.py`

```python
# Libraries used
import pandas as pd
import numpy as np
```

### Steps Performed:
| Step | Operation | Method |
|------|-----------|--------|
| 1 | Load Excel file with correct header row | `pd.read_excel()` |
| 2 | Inspect shape, dtypes, column names | `df.info()`, `df.describe()` |
| 3 | Null value analysis | `df.isnull().sum()`, `np.any()` |
| 4 | Duplicate detection & removal | `df.duplicated()`, `df.drop_duplicates()` |
| 5 | Type conversion (object → float/int) | `pd.to_numeric()`, `.astype()` |
| 6 | String standardization (strip, title-case) | `.str.strip()`, `.str.title()` |
| 7 | Outlier detection (IQR + Z-score) | `np.percentile()`, `np.std()` |
| 8 | Data validation (range checks per column) | Boolean masks |
| 9 | Feature engineering (5 new columns) | `pd.cut()`, `np.where()` |
| 10 | Descriptive stats, groupby, pivot, correlation | `df.groupby()`, `np.corrcoef()` |
| 11 | Export cleaned file + summary stats | `pd.ExcelWriter()` |

### New Engineered Columns:
| Column | Description |
|--------|-------------|
| `GPAImproved` | 1 if GPA increased, 0 if not |
| `AIUsageCategory` | None / Light / Moderate / Heavy |
| `GPABand` | GPA performance tier (2.0–4.0) |
| `AIToTraditionalRatio` | GenAI hours / Traditional study hours |
| `HighRiskStudent` | 1 if High Burnout + AI Dependency >= 7 |

---

## 📊 Interactive Dashboard

**File:** `dashboard/ai_students_dashboard.html`

Open directly in any browser — no installation needed.

### Dashboard Features:
- **6 KPI cards** — Total Students, Avg GPA Change, % Improved, AI Hours, Burnout %, Retention %
- **6 live filters** — Major, Year of Study, Burnout Risk, Policy, Skill Level, GenAI Hours slider
- **8 interactive charts** — Bar, Scatter, Donut, Line, Heatmap, Grouped Bar
- **Smart Insights panel** — auto-computed findings classified as Opportunity / Risk / Watch
- **Raw Data Explorer** — sortable, searchable, paginated table

---

## ▶️ How to Run

### Option 1 — Run the Python Script
```bash
# Install required libraries
pip install pandas numpy openpyxl

# Place the dataset in the same folder as the script
# Then run:
python scripts/data_cleaning_script.py
```

### Option 2 — Open the Dashboard
```bash
# No installation needed — just open in browser
open dashboard/ai_students_dashboard.html
# or double-click the file in your file explorer
```

---

## 🧰 Tech Stack

| Technology | Purpose |
|------------|---------|
| Python 3.x | Data processing |
| pandas | Data loading, cleaning, analysis |
| numpy | Statistical computations, outlier detection |
| openpyxl | Excel export |
| HTML / CSS / JS | Dashboard structure & styling |
| Chart.js | Interactive data visualizations |

---

## 📁 Dataset

- **Source:** [Kaggle — AI Impact on Students](https://www.kaggle.com/datasets/laveshjadon/ai-impact-on-students)
- **Author:** Lavesh Jadon
- **Size:** 50,000 rows × 17 columns
- **License:** Refer to Kaggle dataset page

---

## 👤 Author

**Pritesh Pujari**
🔗 [LinkedIn](https://www.linkedin.com/in/pritesh-pujari-analyst)
🐙 [GitHub](https://github.com/priteshpujari07)

---

## ⭐ If you found this useful, give it a star!

```
git clone https://github.com/priteshpujari07/ai-impact-on-students.git
```
