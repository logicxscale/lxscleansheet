import streamlit as st
import pandas as pd

from core.reader import read_data
from core.analyzer import analyze_dataset
from core.validator import validate_dataframe
from core.exporter import export_data
from core.scoring import calculate_confidence_score
from core.history import CleaningHistoryTracker

from rules.empty import fill_empty_cells, drop_empty_columns, get_empty_cells_rows
from rules.duplicate import remove_duplicates, get_duplicate_rows
from rules.formatting import trim_whitespace
from rules.datatype import normalize_datatypes, normalize_dates, normalize_currency
from rules.typo import fix_typo, get_typo_rows
from rules.anomaly import cap_anomalies, get_anomaly_rows
from rules.template import check_schema_template

st.set_page_config(page_title="LXSCleanSheet", layout="wide", page_icon="📊")

# Header HTML matching reference
st.markdown("""
<style>
.header-container {
    background-color: #0f172a;
    padding: 1.5rem;
    border-radius: 10px;
    margin-bottom: 1.5rem;
    color: white;
}
.header-top {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1.5rem;
    margin-bottom: 1rem;
}
.logo-container {
    background-color: #10b981;
    border-radius: 12px;
    padding: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
}
.logo-icon {
    width: 28px;
    height: 28px;
    stroke: white;
    stroke-width: 2;
    fill: none;
}
.title-container {
    display: flex;
    flex-direction: column;
}
.main-title {
    font-size: 24px;
    font-weight: 600;
    margin: 0;
    line-height: 1.2;
}
.lxs { color: #ffffff; }
.cleansheet { color: #10b981; }
.sub-title {
    font-size: 14px;
    color: #cbd5e1;
    margin: 3px 0 0 0;
}
.divider {
    height: 1px;
    background-color: #334155;
    margin: 0;
    width: 100%;
}
.header-bottom {
    text-align: center;
    margin-top: 1rem;
}
.tagline {
    font-size: 16px;
    font-weight: 600;
    margin-bottom: 0.3rem;
    color: #ffffff;
}
.features {
    font-size: 13px;
    color: #94a3b8;
}
</style>

<div class="header-container">
    <div class="header-top">
        <div class="logo-container">
            <svg class="logo-icon" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                <line x1="3" y1="9" x2="21" y2="9"></line>
                <line x1="9" y1="9" x2="9" y2="21"></line>
            </svg>
        </div>
        <div class="title-container">
            <div class="main-title"><span class="lxs">LXS</span><span class="cleansheet">CleanSheet</span></div>
            <p class="sub-title">Excel Data Cleaning &amp; Quality Assistant</p>
        </div>
    </div>
    <div class="divider"></div>
    <div class="header-bottom">
        <div class="tagline">Clean Data. Clear Insights.</div>
        <div class="features">Detect &middot; Analyze &middot; Clean &middot; Validate &middot; Compare</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Session state initialization
if 'df' not in st.session_state:
    st.session_state.df = None
if 'original_df' not in st.session_state:
    st.session_state.original_df = None
if 'history_tracker' not in st.session_state:
    st.session_state.history_tracker = CleaningHistoryTracker()

# Sidebar file uploader & navigation
with st.sidebar:
    st.title("📁 File & Templates")
    uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx", "xls"])
    
    if uploaded_file is not None:
        if st.session_state.original_df is None:
            try:
                df = read_data(uploaded_file)
                st.session_state.original_df = df.copy()
                st.session_state.df = df.copy()
                st.session_state.history_tracker.log("Upload", f"Loaded file with shape {df.shape}")
                st.success("Loaded successfully!")
            except Exception as e:
                st.error(f"Error: {e}")
                
    if st.session_state.df is not None:
        if st.button("Reset to Original"):
            st.session_state.df = st.session_state.original_df.copy()
            st.session_state.history_tracker.log("Reset", "Dataset reset to original state")
            st.rerun()
            
    st.markdown("---")
    st.subheader("🧭 Navigation Menu (Phase 1-3)")
    menu = st.radio(
        "Choose phase:",
        [
            "1. Preview, Score & Schema",
            "2. Missing & Empty Data",
            "3. Duplicates & Formatting",
            "4. Normalization (Date/Currency)",
            "5. Typo & Fuzzy Matching",
            "6. Anomaly Detection",
            "7. Before/After Comparison",
            "8. Cleaning History & Audit Log",
            "9. Validation & Export"
        ]
    )

if st.session_state.df is None:
    st.info("👈 Please upload an Excel file via the sidebar to start the workflow.")
else:
    df = st.session_state.df
    original_df = st.session_state.original_df
    analysis = analyze_dataset(df)
    score = calculate_confidence_score(df)

    if menu == "1. Preview, Score & Schema":
        st.subheader("📊 Dataset Preview, Confidence Score & Schema")
        
        # Confidence Score Metric
        col_m1, col_m2, col_m3 = st.columns(3)
        col_m1.metric("Data Quality Score", f"{score} / 100", delta=f"{score - calculate_confidence_score(original_df)} vs Original")
        col_m2.metric("Total Rows", df.shape[0])
        col_m3.metric("Total Columns", df.shape[1])
        
        st.markdown("---")
        st.subheader("📋 Schema / Template Validation")
        template_input = st.text_input("Expected Columns (comma-separated, optional):", "")
        if template_input:
            expected_cols = [c.strip() for c in template_input.split(",")]
            schema_res = check_schema_template(df, expected_cols)
            st.write(f"**Match Percentage:** {schema_res['match_percentage']:.1f}%")
            st.write("**Missing Columns:**", schema_res['missing'])
            st.write("**Extra Columns:**", schema_res['extra'])
        else:
            st.info("Enter comma-separated column names above to validate against a target schema template.")

        st.markdown("---")
        st.subheader("Data Preview (First 10 Rows)")
        st.dataframe(df.head(10), use_container_width=True)

    elif menu == "2. Missing & Empty Data":
        st.subheader("🧹 Missing Cells & Empty Columns")
        st.write(f"**Empty Cells Detected:** {analysis['empty_cells']}")
        
        if analysis['empty_cells'] > 0:
            st.write("Rows with Empty Cells:")
            st.dataframe(get_empty_cells_rows(df))
            
            approve_fill = st.checkbox("Approve filling missing cells (0 for numeric, 'Unknown' for text)")
            if st.button("Apply Fill Missing Cells"):
                if approve_fill:
                    st.session_state.df = fill_empty_cells(df)
                    st.session_state.history_tracker.log("Missing Cells", f"Filled {analysis['empty_cells']} missing cells")
                    st.success("Empty cells filled successfully!")
                    st.rerun()
                else:
                    st.warning("Please check the approval box before applying.")
                
        st.write(f"**Empty Columns Detected:** {analysis['empty_columns']}")
        if analysis['empty_columns']:
            approve_drop = st.checkbox("Approve dropping empty columns")
            if st.button("Apply Drop Empty Columns"):
                if approve_drop:
                    st.session_state.df = drop_empty_columns(df, analysis['empty_columns'])
                    st.session_state.history_tracker.log("Empty Columns", f"Dropped columns: {analysis['empty_columns']}")
                    st.success("Empty columns dropped!")
                    st.rerun()
                else:
                    st.warning("Please check the approval box before applying.")

    elif menu == "3. Duplicates & Formatting":
        st.subheader("👯 Duplicates & Whitespace Formatting")
        st.write(f"**Duplicate Rows:** {analysis['duplicates']}")
        if analysis['duplicates'] > 0:
            st.write("Duplicate Rows:")
            st.dataframe(get_duplicate_rows(df))
            
            approve_dup = st.checkbox("Approve removing duplicate rows")
            if st.button("Apply Remove Duplicates"):
                if approve_dup:
                    st.session_state.df = remove_duplicates(df)
                    st.session_state.history_tracker.log("Duplicates", f"Removed {analysis['duplicates']} duplicate rows")
                    st.success("Duplicates removed!")
                    st.rerun()
                else:
                    st.warning("Please check the approval box before applying.")
                
        st.markdown("---")
        st.write("**Whitespace Cleaning**")
        approve_ws = st.checkbox("Approve trimming leading/trailing whitespaces")
        if st.button("Apply Trim Whitespaces"):
            if approve_ws:
                st.session_state.df = trim_whitespace(df)
                st.session_state.history_tracker.log("Formatting", "Trimmed whitespace from string columns")
                st.success("Whitespaces trimmed!")
                st.rerun()
            else:
                st.warning("Please check the approval box before applying.")

    elif menu == "4. Normalization (Date/Currency)":
        st.subheader("🔄 Datatype & Format Normalization")
        
        st.write("**Detected Date Columns:**", analysis["date_cols"])
        if analysis["date_cols"]:
            approve_date = st.checkbox("Approve date normalization for detected columns")
            if st.button("Apply Date Normalization"):
                if approve_date:
                    st.session_state.df = normalize_dates(df, analysis["date_cols"])
                    st.session_state.history_tracker.log("Normalization", f"Normalized dates in {analysis['date_cols']}")
                    st.success("Dates normalized!")
                    st.rerun()
                else:
                    st.warning("Please check approval box.")
                
        st.markdown("---")
        st.write("**Detected Currency/Number Columns:**", analysis["currency_cols"])
        if analysis["currency_cols"]:
            approve_curr = st.checkbox("Approve currency/number normalization")
            if st.button("Apply Currency Normalization"):
                if approve_curr:
                    st.session_state.df = normalize_currency(df, analysis["currency_cols"])
                    st.session_state.history_tracker.log("Normalization", f"Normalized currency/numbers in {analysis['currency_cols']}")
                    st.success("Currency numbers normalized!")
                    st.rerun()
                else:
                    st.warning("Please check approval box.")

    elif menu == "5. Typo & Fuzzy Matching":
        st.subheader("🔍 Typo Detection & Fuzzy Matching")
        typos = analysis["typos"]
        if typos:
            for col, pairs in typos.items():
                st.write(f"Column: **{col}**")
                for idx, (p1, p2) in enumerate(pairs):
                    col1, col2, col3 = st.columns([2, 2, 1])
                    col1.write(f"'{p1}'")
                    col2.write(f"'{p2}'")
                    if col3.button(f"Merge to '{p1}'", key=f"{col}_{p1}_{p2}_{idx}"):
                        st.session_state.df = fix_typo(df, col, p2, p1)
                        st.session_state.history_tracker.log("Typo Fix", f"Merged '{p2}' to '{p1}' in {col}")
                        st.success(f"Replaced '{p2}' with '{p1}'")
                        st.rerun()
                    st.write(f"Rows with '{p2}' in {col}:")
                    st.dataframe(get_typo_rows(df, col, p2))
        else:
            st.write("No major typos or close matches found.")

    elif menu == "6. Anomaly Detection":
        st.subheader("⚡ Anomaly & Outlier Detection (IQR Method)")
        anomalies = analysis["anomalies"]
        if anomalies:
            for col, info in anomalies.items():
                st.write(f"Column: **{col}** — Outliers found: {info['count']} (Range: {info['lower_bound']:.2f} to {info['upper_bound']:.2f})")
                st.write(f"Outliers in {col}:")
                st.dataframe(get_anomaly_rows(df, col, info['lower_bound'], info['upper_bound']))
                if st.button(f"Cap Outliers in {col}", key=f"cap_{col}"):
                    st.session_state.df = cap_anomalies(df, col, info['lower_bound'], info['upper_bound'])
                    st.session_state.history_tracker.log("Anomaly Capping", f"Capped outliers in {col}")
                    st.success(f"Capped outliers for {col}!")
                    st.rerun()
        else:
            st.write("No numeric outliers detected.")

    elif menu == "7. Before/After Comparison":
        st.subheader("⚖️ Before vs After Cleaning Comparison")
        col_b, col_a = st.columns(2)
        with col_b:
            st.markdown("### 🔴 Original Dataset")
            st.write(f"Shape: {original_df.shape}")
            st.metric("Original Confidence Score", f"{calculate_confidence_score(original_df)} / 100")
            st.dataframe(original_df.head(10), use_container_width=True)
        with col_a:
            st.markdown("### 🟢 Current Cleaned Dataset")
            st.write(f"Shape: {df.shape}")
            st.metric("Current Confidence Score", f"{score} / 100")
            st.dataframe(df.head(10), use_container_width=True)

    elif menu == "8. Cleaning History & Audit Log":
        st.subheader("📜 Cleaning History & Audit Log")
        logs = st.session_state.history_tracker.get_logs()
        if logs:
            log_df = pd.DataFrame(logs)
            st.dataframe(log_df, use_container_width=True)
        else:
            st.info("No cleaning actions recorded yet.")

    elif menu == "9. Validation & Export":
        st.subheader("✅ Final Validation & Export")
        validation = validate_dataframe(df)
        st.json(validation)
        
        st.markdown("---")
        excel_bytes = export_data(df)
        st.download_button(
            label="📥 Download Cleaned Excel File",
            data=excel_bytes,
            file_name="cleaned_dataset.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
