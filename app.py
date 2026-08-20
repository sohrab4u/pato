import io
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------------
# 1. Page Configuration & Professional CSS Styling
# ---------------------------------------------------------
st.set_page_config(
    page_title="High-Risk TB Follow-up Analytics",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Main Canvas Background */
    .stApp {
        background-color: #F8FAFC;
    }
    
    /* Layout Container Spacing */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 2rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 100% !important;
    }
    
    /* Professional Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0F172A !important;
        border-right: 1px solid #1E293B !important;
    }
    section[data-testid="stSidebar"] * {
        color: #F8FAFC;
    }
    section[data-testid="stSidebar"] label {
        font-size: 0.8rem !important;
        font-weight: 600 !important;
        color: #94A3B8 !important;
        margin-bottom: 2px !important;
    }
    
    /* Compact File Uploader in Sidebar */
    div[data-testid="stFileUploader"] {
        padding: 0 !important;
        margin-bottom: 8px !important;
    }
    div[data-testid="stFileUploader"] section {
        background-color: #1E293B !important;
        border: 1px dashed #334155 !important;
        border-radius: 6px !important;
        padding: 8px 12px !important;
    }
    div[data-testid="stFileUploader"] section small {
        display: none !important;
    }
    div[data-testid="stFileUploader"] button {
        background: #2563EB !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 4px !important;
        padding: 4px 10px !important;
        font-size: 0.78rem !important;
        font-weight: 600 !important;
    }

    /* Multiselect Tag Chips */
    span[data-baseweb="tag"] {
        background-color: #2563EB !important;
        border-radius: 4px !important;
        font-size: 0.74rem !important;
        color: #FFFFFF !important;
    }

    /* Sidebar Headings & Badges */
    .sidebar-brand-pill {
        display: inline-block;
        background: #1D4ED8;
        color: #FFFFFF !important;
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        margin-bottom: 6px;
    }
    .sidebar-heading {
        font-size: 0.88rem;
        font-weight: 700;
        color: #F8FAFC !important;
        margin-top: 8px;
        margin-bottom: 6px;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .sidebar-sep {
        height: 1px;
        background-color: #334155;
        margin: 12px 0 10px 0;
    }

    /* Executive Top Hero Header */
    .top-hero-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-left: 6px solid #2563EB;
        border-radius: 10px;
        padding: 16px 22px;
        margin-bottom: 16px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .hero-title-main {
        font-size: 1.35rem;
        font-weight: 800;
        color: #0F172A;
        margin: 0;
        line-height: 1.2;
    }
    .hero-meta-subtitle {
        font-size: 0.82rem;
        color: #64748B;
        margin-top: 4px;
        font-weight: 500;
    }
    .live-status-pill {
        background-color: #ECFDF5;
        color: #059669;
        border: 1px solid #A7F3D0;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }

    /* Executive Metric Cards */
    .metric-card-wrapper {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 16px 18px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
        position: relative;
        overflow: hidden;
    }
    .metric-accent-line {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
    }
    .accent-blue { background: #2563EB; }
    .accent-green { background: #10B981; }
    .accent-amber { background: #F59E0B; }
    .accent-purple { background: #8B5CF6; }

    .metric-label-text {
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: #64748B;
        margin-bottom: 4px;
    }
    .metric-value-text {
        font-size: 1.7rem;
        font-weight: 800;
        color: #0F172A;
        line-height: 1.1;
    }
    .metric-sub-note {
        font-size: 0.72rem;
        color: #94A3B8;
        margin-top: 4px;
        font-weight: 500;
    }

    /* Tab Custom Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 2px solid #E2E8F0;
        margin-bottom: 16px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 6px 6px 0 0;
        font-size: 0.88rem;
        font-weight: 600;
        color: #64748B;
        padding: 8px 16px;
    }
    .stTabs [aria-selected="true"] {
        color: #2563EB !important;
        border-bottom: 2px solid #2563EB !important;
        background-color: #EFF6FF !important;
    }

    /* Standard Dataframe styling */
    .stDataFrame {
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        background: #FFFFFF;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# 2. Data Processing & Auto-Detection Helpers
# ---------------------------------------------------------
def find_column(df, possible_names):
    col_map = {str(c).strip().lower().replace("_", " ").replace("-", " "): c for c in df.columns}
    for name in possible_names:
        clean_name = name.strip().lower().replace("_", " ").replace("-", " ")
        if clean_name in col_map:
            return col_map[clean_name]
    return None

def normalize_text(series):
    return (
        series.fillna("Unknown")
        .astype(str)
        .str.strip()
        .replace({"": "Unknown", "nan": "Unknown", "None": "Unknown", "NAN": "Unknown"})
        .str.title()
    )

def safe_unique_list(series_list):
    combined = set()
    for s in series_list:
        for item in s:
            if pd.notna(item):
                item_str = str(item).strip()
                if item_str and item_str.lower() not in ["none", "nan", "null"]:
                    combined.add(item_str)
    return sorted(list(combined), key=lambda x: str(x).lower())

@st.cache_data(show_spinner=False)
def load_csv(file):
    try:
        return pd.read_csv(file, encoding="utf-8")
    except UnicodeDecodeError:
        file.seek(0)
        return pd.read_csv(file, encoding="latin1")

@st.cache_data(show_spinner=False)
def load_excel(file):
    return pd.read_excel(file)

# ---------------------------------------------------------
# 3. Sidebar Setup (File Ingestion + Cascade Filters)
# ---------------------------------------------------------
with st.sidebar:
    st.markdown('<div class="sidebar-brand-pill">TB Care Analytics</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-heading">📁 File Ingestion</div>', unsafe_allow_html=True)
    
    csv_file = st.file_uploader("1. Patient Line List (CSV)", type=["csv"], help="Upload CSV containing High-Risk TB patient records.")
    excel_file = st.file_uploader("2. Follow-up Report (Excel)", type=["xlsx", "xls"], help="Upload Excel containing user follow-up progress.")
    
    st.markdown('<div class="sidebar-sep"></div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# 4. Empty State Handler
# ---------------------------------------------------------
if not csv_file or not excel_file:
    st.markdown(
        """
        <div class="top-hero-card">
            <div>
                <h1 class="hero-title-main">High-Risk TB Patient Follow-up Monitoring Dashboard</h1>
                <div class="hero-meta-subtitle">Automated Multi-District TB Patient Follow-up & Performance Analytics System</div>
            </div>
            <div class="live-status-pill" style="background-color: #FEF3C7; color: #D97706; border-color: #FDE68A;">
                ● Awaiting Data Upload
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    st.info("👈 **Please upload both data files using the left sidebar to generate the interactive dashboard.**")
    st.stop()

# ---------------------------------------------------------
# 5. Schema Validation & Data Ingestion
# ---------------------------------------------------------
df_csv_raw = load_csv(csv_file)
df_excel_raw = load_excel(excel_file)

col_p_dist = find_column(df_csv_raw, ["Current Facility District", "District", "District Name"])
col_p_tu = find_column(df_csv_raw, ["Current Facility TBU", "Current Facility TU", "TU", "Tuberculosis Unit", "TBU"])
col_p_id = find_column(df_csv_raw, ["Episode ID", "Patient ID", "Nikshay ID", "ID"])

col_f_dist = find_column(df_excel_raw, ["District", "Current Facility District", "District Name"])
col_f_tu = find_column(df_excel_raw, ["Facility Name", "Current Facility TBU", "Current Facility TU", "TU", "TBU"])
col_f_user = find_column(df_excel_raw, ["User Name", "User", "Followed Up By", "Staff Name"])
col_f_count = find_column(df_excel_raw, ["Followed Up Patient Count", "Follow up count", "Count", "Followed Up Count"])
col_f_id = find_column(df_excel_raw, ["Episode ID", "Patient ID", "Nikshay ID", "ID"])

if not col_p_dist or not col_p_tu:
    st.error("❌ The CSV file must have identifiable 'District' and 'TU/TBU' columns.")
    st.stop()

if not col_f_dist:
    st.error("❌ The Excel file must have an identifiable 'District' column.")
    st.stop()

# ---------------------------------------------------------
# 6. Data Cleaning & Line-List Relational Mapping
# ---------------------------------------------------------
df_pt = df_csv_raw.copy()
df_pt["District_Clean"] = normalize_text(df_pt[col_p_dist])
df_pt["TU_Clean"] = normalize_text(df_pt[col_p_tu])

if col_p_id:
    df_pt = df_pt.dropna(subset=[col_p_id]).drop_duplicates(subset=[col_p_id])
else:
    df_pt = df_pt.drop_duplicates()

df_fu = df_excel_raw.copy()
df_fu["District_Clean"] = normalize_text(df_fu[col_f_dist])
df_fu["TU_Clean"] = normalize_text(df_fu[col_f_tu]) if col_f_tu else "Unknown"
df_fu["User_Clean"] = normalize_text(df_fu[col_f_user]) if col_f_user else "Unassigned"

if col_f_count:
    df_fu["Followup_Count_Num"] = pd.to_numeric(df_fu[col_f_count], errors="coerce").fillna(0).astype(int)
else:
    df_fu["Followup_Count_Num"] = 1

has_patient_level_fu = bool(col_f_id and col_p_id and set(df_fu[col_f_id].dropna()).intersection(set(df_pt[col_p_id].dropna())))

if has_patient_level_fu:
    fu_matched_ids = set(df_fu.dropna(subset=[col_f_id])[col_f_id])
    df_pt["Follow-up Status"] = df_pt[col_p_id].isin(fu_matched_ids).map({True: "Completed", False: "Pending"})
    if col_f_user:
        fu_user_map = df_fu.dropna(subset=[col_f_id]).drop_duplicates(subset=[col_f_id]).set_index(col_f_id)[col_f_user].to_dict()
        df_pt["Follow-up User"] = df_pt[col_p_id].map(fu_user_map).fillna("Unassigned")
else:
    df_pt["Follow-up Status"] = "Aggregated Record"
    df_pt["Follow-up User"] = "See User Tab"

# ---------------------------------------------------------
# 7. Cascading Sidebar Filters
# ---------------------------------------------------------
with st.sidebar:
    st.markdown('<div class="sidebar-heading">🔍 Dynamic Filters</div>', unsafe_allow_html=True)
    
    # District Multi-Select
    all_districts = safe_unique_list([df_pt["District_Clean"].unique(), df_fu["District_Clean"].unique()])
    select_all_dist = st.checkbox("Select All Districts", value=True)
    
    if select_all_dist:
        selected_districts = st.multiselect("Filter Districts", options=all_districts, default=all_districts)
    else:
        selected_districts = st.multiselect("Filter Districts", options=all_districts, default=[])

    if not selected_districts:
        st.warning("⚠️ Please select at least one district.")
        st.stop()

    # TU Cascading Select
    pt_tus = df_pt[df_pt["District_Clean"].isin(selected_districts)]["TU_Clean"].unique()
    fu_tus = df_fu[df_fu["District_Clean"].isin(selected_districts)]["TU_Clean"].unique()
    available_tus = safe_unique_list([pt_tus, fu_tus])
    tu_choice = st.selectbox("Filter TU (Tuberculosis Unit)", ["All"] + available_tus)

    # User Cascading Select
    fu_user_scoped = df_fu[df_fu["District_Clean"].isin(selected_districts)].copy()
    if tu_choice != "All":
        fu_user_scoped = fu_user_scoped[fu_user_scoped["TU_Clean"] == tu_choice]
    available_users = safe_unique_list([fu_user_scoped["User_Clean"].unique()])
    user_choice = st.selectbox("Filter User (Field Staff)", ["All"] + available_users)

# ---------------------------------------------------------
# 8. Apply Filters & Calculate Metrics
# ---------------------------------------------------------
filtered_pt = df_pt[df_pt["District_Clean"].isin(selected_districts)].copy()
filtered_fu = df_fu[df_fu["District_Clean"].isin(selected_districts)].copy()

if tu_choice != "All":
    filtered_pt = filtered_pt[filtered_pt["TU_Clean"] == tu_choice]
    filtered_fu = filtered_fu[filtered_fu["TU_Clean"] == tu_choice]

if user_choice != "All":
    filtered_fu = filtered_fu[filtered_fu["User_Clean"] == user_choice]
    if has_patient_level_fu:
        filtered_pt = filtered_pt[filtered_pt["Follow-up User"] == user_choice]

kpi_total_patients = len(filtered_pt)

if has_patient_level_fu:
    kpi_completed = len(filtered_pt[filtered_pt["Follow-up Status"] == "Completed"])
else:
    kpi_completed = int(filtered_fu["Followup_Count_Num"].sum())

kpi_pending = max(0, kpi_total_patients - kpi_completed)
kpi_rate = round((kpi_completed / kpi_total_patients * 100), 2) if kpi_total_patients > 0 else 0.0

# ---------------------------------------------------------
# 9. Top Hero Header Banner
# ---------------------------------------------------------
if len(selected_districts) == len(all_districts):
    scope_dist_txt = "All Districts"
elif len(selected_districts) <= 3:
    scope_dist_txt = ", ".join(selected_districts)
else:
    scope_dist_txt = f"{len(selected_districts)} Districts Selected"

st.markdown(
    f"""
    <div class="top-hero-card">
        <div>
            <h1 class="hero-title-main">High-Risk TB Patient Follow-up Monitoring Dashboard</h1>
            <div class="hero-meta-subtitle">
                Active Scope: <strong>{scope_dist_txt}</strong> &nbsp;|&nbsp; TU: <strong>{tu_choice}</strong> &nbsp;|&nbsp; Staff: <strong>{user_choice}</strong>
            </div>
        </div>
        <div class="live-status-pill">
            <span style="font-size: 8px;">●</span> System Active
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# 10. Metric KPI Cards
# ---------------------------------------------------------
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(
        f"""
        <div class="metric-card-wrapper">
            <div class="metric-accent-line accent-blue"></div>
            <div class="metric-label-text">Total High-Risk Patients</div>
            <div class="metric-value-text">{kpi_total_patients:,}</div>
            <div class="metric-sub-note">Line-listed cases</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with c2:
    st.markdown(
        f"""
        <div class="metric-card-wrapper">
            <div class="metric-accent-line accent-green"></div>
            <div class="metric-label-text">Follow-up Completed</div>
            <div class="metric-value-text">{kpi_completed:,}</div>
            <div class="metric-sub-note">Verified completed records</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with c3:
    st.markdown(
        f"""
        <div class="metric-card-wrapper">
            <div class="metric-accent-line accent-amber"></div>
            <div class="metric-label-text">Pending Follow-up</div>
            <div class="metric-value-text">{kpi_pending:,}</div>
            <div class="metric-sub-note">Awaiting field completion</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with c4:
    st.markdown(
        f"""
        <div class="metric-card-wrapper">
            <div class="metric-accent-line accent-purple"></div>
            <div class="metric-label-text">Follow-up Rate</div>
            <div class="metric-value-text">{kpi_rate}%</div>
            <div class="metric-sub-note">Overall coverage achieved</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")

# ---------------------------------------------------------
# 11. Data Aggregations for Tables & Visualizations
# ---------------------------------------------------------
# District Level Aggregation
d_pt = filtered_pt.groupby("District_Clean").size().reset_index(name="Total High-Risk Patients")
if has_patient_level_fu:
    d_fu = filtered_pt[filtered_pt["Follow-up Status"] == "Completed"].groupby("District_Clean").size().reset_index(name="Follow-up Completed")
else:
    d_fu = filtered_fu.groupby("District_Clean")["Followup_Count_Num"].sum().reset_index(name="Follow-up Completed")

district_df = pd.merge(d_pt, d_fu, on="District_Clean", how="outer").fillna(0)
district_df["Total High-Risk Patients"] = district_df["Total High-Risk Patients"].astype(int)
district_df["Follow-up Completed"] = district_df["Follow-up Completed"].astype(int)
district_df["Pending Follow-up"] = (district_df["Total High-Risk Patients"] - district_df["Follow-up Completed"]).clip(lower=0)
district_df["Follow-up %"] = (
    (district_df["Follow-up Completed"] / district_df["Total High-Risk Patients"].replace(0, pd.NA) * 100)
    .fillna(0)
    .round(2)
)
district_df = district_df.rename(columns={"District_Clean": "District"}).sort_values(by="Total High-Risk Patients", ascending=False)

# TU Level Aggregation
t_pt = filtered_pt.groupby(["District_Clean", "TU_Clean"]).size().reset_index(name="Total High-Risk Patients")
if has_patient_level_fu:
    t_fu = filtered_pt[filtered_pt["Follow-up Status"] == "Completed"].groupby(["District_Clean", "TU_Clean"]).size().reset_index(name="Follow-up Completed")
else:
    t_fu = filtered_fu.groupby(["District_Clean", "TU_Clean"])["Followup_Count_Num"].sum().reset_index(name="Follow-up Completed")

tu_df = pd.merge(t_pt, t_fu, on=["District_Clean", "TU_Clean"], how="outer").fillna(0)
tu_df["Total High-Risk Patients"] = tu_df["Total High-Risk Patients"].astype(int)
tu_df["Follow-up Completed"] = tu_df["Follow-up Completed"].astype(int)
tu_df["Pending Follow-up"] = (tu_df["Total High-Risk Patients"] - tu_df["Follow-up Completed"]).clip(lower=0)
tu_df["Follow-up %"] = (
    (tu_df["Follow-up Completed"] / tu_df["Total High-Risk Patients"].replace(0, pd.NA) * 100)
    .fillna(0)
    .round(2)
)
tu_df = tu_df.rename(columns={"District_Clean": "District", "TU_Clean": "TU"}).sort_values(by="Total High-Risk Patients", ascending=False)

# User Level Aggregation
if has_patient_level_fu:
    user_df = (
        filtered_pt[filtered_pt["Follow-up Status"] == "Completed"]
        .groupby(["District_Clean", "TU_Clean", "Follow-up User"])
        .size()
        .reset_index(name="Patients Followed Up")
        .rename(columns={"District_Clean": "District", "TU_Clean": "TU", "Follow-up User": "User"})
    )
else:
    user_df = (
        filtered_fu.groupby(["District_Clean", "TU_Clean", "User_Clean"])["Followup_Count_Num"]
        .sum()
        .reset_index(name="Patients Followed Up")
        .rename(columns={"District_Clean": "District", "TU_Clean": "TU", "User_Clean": "User"})
    )

total_user_fu = user_df["Patients Followed Up"].sum()
user_df["Follow-up %"] = (
    (user_df["Patients Followed Up"] / total_user_fu * 100).fillna(0).round(2) if total_user_fu > 0 else 0.0
)
user_df = user_df.sort_values(by="Patients Followed Up", ascending=False)

# ---------------------------------------------------------
# 12. Tabbed Analytical Workspace
# ---------------------------------------------------------
tab_dist, tab_tu, tab_staff, tab_patients = st.tabs(
    ["📊 District Overview", "🏥 TU-Wise Analysis", "👥 Field Staff Performance", "📋 Patient Line-List"]
)

# Plotly styling standard
plotly_theme = dict(
    plot_bgcolor="#FFFFFF",
    paper_bgcolor="#FFFFFF",
    font=dict(family="Plus Jakarta Sans", size=11, color="#475569"),
    margin=dict(l=10, r=10, t=25, b=10),
)

with tab_dist:
    col_d1, col_d2 = st.columns([6, 6])
    with col_d1:
        st.markdown("**District Follow-up vs Pending Status**")
        fig_d = go.Figure()
        fig_d.add_trace(go.Bar(name="Completed", x=district_df["District"].head(15), y=district_df["Follow-up Completed"].head(15), marker_color="#10B981"))
        fig_d.add_trace(go.Bar(name="Pending", x=district_df["District"].head(15), y=district_df["Pending Follow-up"].head(15), marker_color="#EF4444"))
        fig_d.update_layout(barmode="stack", height=320, legend=dict(orientation="h", y=1.12, x=0.25), **plotly_theme)
        fig_d.update_xaxes(showgrid=False)
        fig_d.update_yaxes(gridcolor="#F1F5F9")
        st.plotly_chart(fig_d, use_container_width=True)
    with col_d2:
        st.markdown("**District Breakdown Report**")
        st.dataframe(district_df, use_container_width=True, height=320)

with tab_tu:
    col_t1, col_t2 = st.columns([6, 6])
    with col_t1:
        st.markdown("**Top 15 Tuberculosis Units (TUs) by Patient Volume**")
        fig_t = px.bar(
            tu_df.head(15),
            x="TU",
            y=["Follow-up Completed", "Pending Follow-up"],
            barmode="group",
            color_discrete_sequence=["#2563EB", "#F59E0B"],
        )
        fig_t.update_layout(height=320, legend=dict(orientation="h", y=1.12, x=0.25), **plotly_theme)
        fig_t.update_xaxes(showgrid=False)
        fig_t.update_yaxes(gridcolor="#F1F5F9")
        st.plotly_chart(fig_t, use_container_width=True)
    with col_t2:
        st.markdown("**TU Analytical Performance Report**")
        st.dataframe(tu_df, use_container_width=True, height=320)

with tab_staff:
    col_u1, col_u2 = st.columns([5, 7])
    with col_u1:
        st.markdown("**Top Follow-up Staff Output**")
        fig_u = px.bar(
            user_df.head(15),
            x="Patients Followed Up",
            y="User",
            orientation="h",
            color="Patients Followed Up",
            color_continuous_scale="Blues",
        )
        fig_u.update_layout(yaxis=dict(autorange="reversed"), height=320, **plotly_theme)
        fig_u.update_xaxes(gridcolor="#F1F5F9")
        fig_u.update_yaxes(showgrid=False)
        st.plotly_chart(fig_u, use_container_width=True)
    with col_u2:
        st.markdown("**Staff Performance Report**")
        st.dataframe(user_df, use_container_width=True, height=320)

with tab_patients:
    st.markdown("**Line-List Patient Records in Active Scope**")
    display_cols = [c for c in filtered_pt.columns if c not in ["District_Clean", "TU_Clean"]]
    st.dataframe(filtered_pt[display_cols].head(1000), use_container_width=True, height=350)
    if len(filtered_pt) > 1000:
        st.caption(f"Showing first 1,000 records of {len(filtered_pt):,} matching patients.")

st.markdown("---")

# ---------------------------------------------------------
# 13. Multi-Format Export Center
# ---------------------------------------------------------
st.markdown("### 📥 Export Reports & Analytics")

def build_excel_export(p_df, d_df, t_df, u_df):
    out = io.BytesIO()
    with pd.ExcelWriter(out, engine="openpyxl") as writer:
        d_df.to_excel(writer, sheet_name="District Summary", index=False)
        t_df.to_excel(writer, sheet_name="TU Summary", index=False)
        u_df.to_excel(writer, sheet_name="User Performance", index=False)
        p_df.to_excel(writer, sheet_name="Filtered Patients", index=False)
    return out.getvalue()

c_exp1, c_exp2 = st.columns(2)
with c_exp1:
    excel_payload = build_excel_export(filtered_pt[display_cols], district_df, tu_df, user_df)
    st.download_button(
        label="📊 Download Multi-Sheet Summary Report (Excel)",
        data=excel_payload,
        file_name="High_Risk_TB_Analysis_Report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
    )
with c_exp2:
    csv_payload = filtered_pt[display_cols].to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📋 Download Filtered Line-List (CSV)",
        data=csv_payload,
        file_name="Filtered_Patient_LineList.csv",
        mime="text/csv",
        use_container_width=True,
    )