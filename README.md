# 📊 LXSCleanSheet

<p align="center">
  <b>Excel Data Cleaning & Quality Assistant built with Streamlit</b><br>
  <i>Clean Data. Clear Insights. Detect · Analyze · Clean · Validate</i>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.13+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/Streamlit-1.65.0-red.svg" alt="Streamlit">
  <img src="https://img.shields.io/badge/Pandas-3.0.6-green.svg" alt="Pandas">
  <img src="https://img.shields.io/badge/License-MIT-purple.svg" alt="License">
</p>

---

## 🌟 Overview

**LXSCleanSheet** is a robust, interactive, and intelligent data cleaning and quality assurance web application designed for professionals working with spreadsheet data (Excel `.xlsx`, `.xls`, and CSV files). Powered by Python, Streamlit, and Pandas, it streamlines the tedious process of data auditing, typo correction, anomaly detection, datatype normalization, and schema validation.

Explore the core application entry point at [app.py](c:/data/Workspaces/lxscleansheet/app.py) and check out the dependencies listed in [requirements.txt](c:/data/Workspaces/lxscleansheet/requirements.txt).

---

## 🚀 Key Features

* **📥 Multi-Format Data Ingestion**: Seamlessly load Excel worksheets (`.xlsx`, `.xls`) with multi-sheet support or CSV files via [reader.py](c:/data/Workspaces/lxscleansheet/core/reader.py).
* **🔍 Comprehensive Data Quality Audit**:
  * **Empty Cells & Columns**: Detect and handle missing values and empty columns ([empty.py](c:/data/Workspaces/lxscleansheet/rules/empty.py)).
  * **Duplicate Detection**: Identify and remove duplicate records ([duplicate.py](c:/data/Workspaces/lxscleansheet/rules/duplicate.py)).
  * **Text Formatting & Normalization**: Trim unwanted whitespace and normalize text casing ([formatting.py](c:/data/Workspaces/lxscleansheet/rules/formatting.py)).
  * **Datatype Normalization**: Automatically parse and standardize dates, currency formats, and numeric types ([datatype.py](c:/data/Workspaces/lxscleansheet/rules/datatype.py)).
  * **Fuzzy Typo Correction**: Detect spelling inconsistencies and typos using fuzzy matching ([typo.py](c:/data/Workspaces/lxscleansheet/rules/typo.py)).
  * **Statistical Anomaly Detection**: Spot and cap data outliers ([anomaly.py](c:/data/Workspaces/lxscleansheet/rules/anomaly.py)).
  * **Schema & Template Validation**: Verify datasets against expected business templates ([template.py](c:/data/Workspaces/lxscleansheet/rules/template.py)).
* **📈 Data Quality Scoring**: Calculate confidence and quality scores ([scoring.py](c:/data/Workspaces/lxscleansheet/core/scoring.py)).
* **🕒 Cleaning History & Tracking**: Keep track of cleaning steps and modifications ([history.py](c:/data/Workspaces/lxscleansheet/core/history.py)).
* **🤖 AI Assistant**: Integrated smart recommendations and insights ([ai_assistant.py](c:/data/Workspaces/lxscleansheet/core/ai_assistant.py)).
* **📤 Flexible Exporting**: Export cleaned datasets back to Excel or CSV formats ([exporter.py](c:/data/Workspaces/lxscleansheet/core/exporter.py)).

---

## 🏗️ Project Architecture

```tree
lxscleansheet/
├── app.py                  # Main Streamlit web application interface
├── requirements.txt        # Python package dependencies
├── core/                   # Core processing engines
│   ├── analyzer.py         # Dataset quality analysis orchestrator
│   ├── ai_assistant.py     # AI insights and suggestions
│   ├── cleaner.py          # Cleaning transformation orchestrator
│   ├── exporter.py         # Excel / CSV export utilities
│   ├── history.py          # Session cleaning history tracker
│   ├── reader.py           # File reader & sheet extractor
│   ├── scoring.py          # Quality confidence scoring engine
│   └── validator.py        # Data validation checks
├── rules/                  # Specific data quality rules & algorithms
│   ├── anomaly.py          # Outlier & anomaly detection
│   ├── datatype.py         # Datatype & currency/date parsing
│   ├── duplicate.py        # Duplicate row handler
│   ├── empty.py            # Missing values & empty columns
│   ├── formatting.py       # Whitespace & casing normalizer
│   ├── template.py         # Schema template verifier
│   └── typo.py             # Fuzzy typo detection
├── utils/                  # Utility helpers
│   └── excel.py            # Excel formatting helper
└── models/                 # Data models
    └── issue.py            # Data issue representation
```

---

## 🛠️ Step-by-Step Guide to Rebuild & Run the Project

Follow these instructions to set up, rebuild, and run **LXSCleanSheet** from scratch on your local machine.

### Prerequisites
* **Python 3.13+** installed on your system.
* **Git** for version control.

### Step 1: Clone or Navigate to the Repository
Open your terminal and navigate to your workspace directory (or clone the repository):
```bash
cd c:\data\Workspaces\lxscleansheet
```

### Step 2: Create and Activate a Python Virtual Environment
It is recommended to isolate project dependencies using a virtual environment:
```powershell
python -m venv .venv
# On Windows (PowerShell):
.venv\Scripts\Activate.ps1
# On Windows (Command Prompt):
.venv\Scripts\activate.bat
```

### Step 3: Install Dependencies
Install all required packages specified in [requirements.txt](c:/data/Workspaces/lxscleansheet/requirements.txt):
```powershell
pip install -r requirements.txt
```

### Step 4: Verify the Installation
Check that Streamlit and core dependencies are correctly installed:
```powershell
streamlit --version
```

### Step 5: Run the Streamlit Application
Launch the web interface locally:
```powershell
streamlit run app.py
```
This will start a local Streamlit server (typically at `http://localhost:8501`) and open the interactive **LXSCleanSheet** dashboard in your default web browser.

---

## 🤝 Contributing

Contributions, bug reports, and feature requests are welcome! Feel free to open issues or submit pull requests.

## 📄 License

This project is licensed under the MIT License.

