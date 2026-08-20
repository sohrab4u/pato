import io
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------------
# 1. Page Configuration & Layout Styling
# ---------------------------------------------------------
st.set_page_config(
    page_title="High-Risk TB Patient Follow-up Portal",
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
    
    .main {
        background-color: #F8FAFC;
    }
    
    /* Professional Compact Sidebar - Zero Scroll */
    section[data-testid="stSidebar"] {
        background-color: #0F172A !important;
        padding-top: 1.2rem !important;
        padding-bottom: 0.5rem !important;
        width: 300px !important;
    }
    section[data-testid="stSidebar"] * {
        color: #F1F5F9 !important;
    }
    section[data-testid="stSidebar"] .stSelectbox label, 
    section[data-testid="stSidebar"] .stMultiSelect label {
        font-size: 0.82rem !important;
        font-weight: 600 !important;
        color: #94A3B8 !important;
        margin-bottom: 2px !important;
    }
    section[data-testid="stSidebar"] .stCheckbox label {
        font-size: 0.8rem !important;
        color: #CBD5E1 !important;
    }
    
    /* Multiselect tag badge */
    span[data-baseweb="tag"] {
        background-color: #2563EB !important;
        border-radius: 4px !important;
    }

    /* Main Hero Header */
    .hero-banner {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        border-radius: 10px;
        padding: 16px 20px;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .hero-title {
        font-size: 1.35rem;
        font-weight: 800;
        color: #FFFFFF;
        margin: 0;
    }
    .hero-subtitle {
        font-size: 0.82rem;
        color: #94A3B8;
        margin-top: 2px;
    }
    .status-pill {
        background: #10B98122;
        color: #10B981;
        border: 1px solid #10B98144;
        padding: 3px 10px;
        border-radius: 16px;
        font-size: 0.75rem;
        font-weight: 600;
    }

    /* KPI Cards */
    .kpi-card {
        background: #FFFFFF;
        border-radius: 8px;
        padding: 14px 18px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        border: 1px solid #E2E8F0;
        position: relative;
        overflow: hidden;
    }
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
    }
    .kpi-blue::before { background: #3B82F6; }
    .kpi-green::before { background: #10B981; }
    .kpi-amber::before { background: #F59E0B; }
    .kpi-purple::before { background: #8B5CF6; }

    .kpi-label {
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: #64748B;
        margin-bottom: 4px;
    }
    .kpi-value {
        font-size: 1.65rem;
        font-weight: 800;
        color: #0F172A;
        line-height: 1.1;
    }
    .kpi-desc {
        font-size: 0.72rem;
        color: #94A3B8;
        margin-top: 3px;
    }

    /* Upload Container Panel */
    .upload-box {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 14px;
        margin-bottom: 16px;
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
    return series.astype(str).str.strip().str.title()

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
# 3. Main Workspace: File Upload Section
# ---------------------------------------------------------
st.markdown(
    """
    <div class="hero-banner">
        <div>
            <div class="hero-title">High-Risk TB Patient Follow-up Portal</div>
            <div class="hero-subtitle">State & District-Level Treatment Follow-up Monitoring System</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Render File Uploaders on Main Workspace
with st.expander("📂 File Ingestion (Upload CSV & Excel)", expanded=True):
    col_up1, col_up2 = st.columns(2)
    with col_up1:
        csv_file = st.file_uploader("1. High-Risk Patient Line List (CSV)", type=["csv"], help="Upload CSV containing patient records.")
    with col_up2:
        excel_file = st.file_uploader("2. Follow-up Report (Excel)", type=["xlsx", "xls"], help="Upload Excel containing user follow-up progress.")

if not csv_file or not excel_file:
    st.info("👆 Please upload both the **High-Risk Patient CSV** and the **Follow-up Excel** file above to activate the analytics.")
    
    # Clean sidebar placeholder when waiting for files
    with st.sidebar:
        st.markdown("### 🩺 Navigation")
        st.caption("Awaiting data upload...")
    st.stop()

# ---------------------------------------------------------
# 4. Ingestion & Column Schema Mapping
# ---------------------------------------------------------
df_csv_raw = load_csv(csv_file)
df_excel_raw = load_excel(excel_file)

# Dynamic column detection
col_p_dist = find_column(df_csv_raw, ["Current Facility District", "District", "District Name"])
col_p_tu = find_column(df_csv_raw, ["Current Facility TBU", "Current Facility TU", "TU", "Tuberculosis Unit", "TBU"])
col_p_id = find_column(df_csv_raw, ["Episode ID", "Patient ID", "Nikshay ID", "ID"])

col_f_dist = find_column(df_excel_raw, ["District", "Current Facility District", "District Name"])
col_f_tu = find_column(df_excel_raw, ["Facility Name", "Current Facility TBU", "Current Facility TU", "TU", "TBU"])
col_f_user = find_column(df_excel_raw, ["User Name", "User", "Followed Up By", "Staff Name"])
col_f_count = find_column(df_excel_raw, ["Followed Up Patient Count", "Follow up count", "Count", "Followed Up Count"])
col_f_id = find_column(df_excel_raw, ["Episode ID", "Patient ID", "Nikshay ID", "ID"])

if not col_p_dist or not col_p_tu:
    st.error("CSV file must have identifiable 'District' and 'TU/TBU' columns.")
    st.stop()

if not col_f_dist:
    st.error("Excel file must have an identifiable 'District' column.")
    st.stop()

# ---------------------------------------------------------
# 5. Clean & Standardize Datasets
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
df_fu["User_Clean"] = df_fu[col_f_user].astype(str).str.strip() if col_f_user else "Unassigned"

if col_f_count:
    df_fu["Followup_Count_Num"] = pd.to_numeric(df_fu[col_f_count], errors="coerce").fillna(0).astype(int)
else:
    df_fu["Followup_Count_Num"] = 1

# Check for line-list matching vs aggregate matching
has_patient_level_fu = bool(col_f_id and col_p_id and set(df_fu[col_f_id]).intersection(set(df_pt[col_p_id])))

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
# 6. Clean, Zero-Scroll Sidebar Controls
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("### 🔍 Filter Controls")
    
    # 1. Multi-District Selection
    all_districts = sorted(list(set(df_pt["District_Clean"]).union(set(df_fu["District_Clean"]))))
    select_all = st.checkbox("Select All Districts", value=True)
    
    if select_all:
        selected_districts = st.multiselect("Districts", options=all_districts, default=all_districts)
    else:
        selected_districts = st.multiselect("Districts", options=all_districts, default=[])

    if not selected_districts:
        st.warning("Select at least one district.")
        st.stop()

    # 2. TU Selection (Cascaded)
    tu_pool = set(df_pt[df_pt["District_Clean"].isin(selected_districts)]["TU_Clean"]).union(
        set(df_fu[df_fu["District_Clean"].isin(selected_districts)]["TU_Clean"])
    )
    available_tus = sorted(list(tu_pool))
    tu_choice = st.selectbox("TU (Tuberculosis Unit)", ["All"] + available_tus)

    # 3. User Selection (Cascaded)
    fu_user_scoped = df_fu[df_fu["District_Clean"].isin(selected_districts)].copy()
    if tu_choice != "All":
        fu_user_scoped = fu_user_scoped[fu_user_scoped["TU_Clean"] == tu_choice]
    available_users = sorted(fu_user_scoped["User_Clean"].dropna().unique().tolist())
    user_choice = st.selectbox("User (Field Staff)", ["All"] + available_users)

# ---------------------------------------------------------
# 7. Apply Filters & Compute Metrics
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

# Accurate KPI aggregations
kpi_total_patients = len(filtered_pt)

if has_patient_level_fu:
    kpi_completed = len(filtered_pt[filtered_pt["Follow-up Status"] == "Completed"])
else:
    kpi_completed = int(filtered_fu["Followup_Count_Num"].sum())

kpi_pending = max(0, kpi_total_patients - kpi_completed)
kpi_rate = round((kpi_completed / kpi_total_patients * 100), 2) if kpi_total_patients > 0 else 0.0

# ---------------------------------------------------------
# 8. Scope Subheader & KPI Cards
# ---------------------------------------------------------
if len(selected_districts) == len(all_districts):
    scope_dist_txt = "All Districts"
elif len(selected_districts) <= 3:
    scope_dist_txt = ", ".join(selected_districts)
else:
    scope_dist_txt = f"{len(selected_districts)} Districts Selected"

st.caption(f"Active Scope: **{scope_dist_txt}** | TU: **{tu_choice}** | User: **{user_choice}**")

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(
        f"""
        <div class="kpi-card kpi-blue">
            <div class="kpi-label">Total High-Risk Patients</div>
            <div class="kpi-value">{kpi_total_patients:,}</div>
            <div class="kpi-desc">Line-listed cases</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with c2:
    st.markdown(
        f"""
        <div class="kpi-card kpi-green">
            <div class="kpi-label">Follow-up Completed</div>
            <div class="kpi-value">{kpi_completed:,}</div>
            <div class="kpi-desc">Verified follow-ups</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with c3:
    st.markdown(
        f"""
        <div class="kpi-card kpi-amber">
            <div class="kpi-label">Pending Follow-up</div>
            <div class="kpi-value">{kpi_pending:,}</div>
            <div class="kpi-desc">Pending completion</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with c4:
    st.markdown(
        f"""
        <div class="kpi-card kpi-purple">
            <div class="kpi-label">Follow-up Rate</div>
            <div class="kpi-value">{kpi_rate}%</div>
            <div class="kpi-desc">Coverage achieved</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")

# ---------------------------------------------------------
# 9. Dynamic Aggregation Tables
# ---------------------------------------------------------
# District Level Table
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

# TU Level Table
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

# User Level Table
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
# 10. Visualizations & Analytical Views
# ---------------------------------------------------------
tab_charts, tab_tu_view, tab_users, tab_pt_details = st.tabs(
    ["📊 District Overview", "🏥 TU-Level Breakdown", "👥 Staff Performance", "📋 Filtered Patient Line-List"]
)

with tab_charts:
    col_g1, col_g2 = st.columns([7, 5])
    with col_g1:
        st.markdown("**Follow-up vs Pending by District**")
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(name="Completed", x=district_df["District"].head(15), y=district_df["Follow-up Completed"].head(15), marker_color="#10B981"))
        fig_bar.add_trace(go.Bar(name="Pending", x=district_df["District"].head(15), y=district_df["Pending Follow-up"].head(15), marker_color="#EF4444"))
        fig_bar.update_layout(barmode="stack", height=380, margin=dict(l=10, r=10, t=20, b=10), legend=dict(orientation="h", y=1.1, x=0.3))
        st.plotly_chart(fig_bar, use_container_width=True)
    with col_g2:
        st.markdown("**District Summary Table**")
        st.dataframe(district_df, use_container_width=True, height=380)

with tab_tu_view:
    col_tu1, col_tu2 = st.columns([6, 6])
    with col_tu1:
        st.markdown("**Top 15 TUs by High-Risk Patient Volume**")
        fig_tu = px.bar(
            tu_df.head(15),
            x="TU",
            y=["Follow-up Completed", "Pending Follow-up"],
            barmode="group",
            color_discrete_sequence=["#3B82F6", "#F59E0B"],
        )
        fig_tu.update_layout(height=380, margin=dict(l=10, r=10, t=20, b=10), legend=dict(orientation="h", y=1.1, x=0.3))
        st.plotly_chart(fig_tu, use_container_width=True)
    with col_tu2:
        st.markdown("**TU Analytical Table**")
        st.dataframe(tu_df, use_container_width=True, height=380)

with tab_users:
    col_u1, col_u2 = st.columns([5, 7])
    with col_u1:
        st.markdown("**Top Staff by Follow-up Output**")
        fig_u = px.bar(
            user_df.head(15),
            x="Patients Followed Up",
            y="User",
            orientation="h",
            color="Patients Followed Up",
            color_continuous_scale="Blues",
        )
        fig_u.update_layout(yaxis=dict(autorange="reversed"), height=380, margin=dict(l=10, r=10, t=20, b=10))
        st.plotly_chart(fig_u, use_container_width=True)
    with col_u2:
        st.markdown("**User Follow-up Table**")
        st.dataframe(user_df, use_container_width=True, height=380)

with tab_pt_details:
    st.markdown("**Patient Records in Active Filter Scope**")
    display_cols = [c for c in filtered_pt.columns if c not in ["District_Clean", "TU_Clean"]]
    st.dataframe(filtered_pt[display_cols].head(1000), use_container_width=True, height=380)
    if len(filtered_pt) > 1000:
        st.caption(f"Displaying first 1,000 records of {len(filtered_pt):,} matching patients.")

st.markdown("---")

# ---------------------------------------------------------
# 11. Multi-Format Excel / CSV Export
# ---------------------------------------------------------
st.markdown("### 📥 Download Filtered Reports")

def build_excel(p_df, d_df, t_df, u_df):
    out = io.BytesIO()
    with pd.ExcelWriter(out, engine="openpyxl") as writer:
        d_df.to_excel(writer, sheet_name="District Summary", index=False)
        t_df.to_excel(writer, sheet_name="TU Summary", index=False)
        u_df.to_excel(writer, sheet_name="User Performance", index=False)
        p_df.to_excel(writer, sheet_name="Filtered Patients", index=False)
    return out.getvalue()

c_exp1, c_exp2 = st.columns(2)
with c_exp1:
    excel_payload = build_excel(filtered_pt[display_cols], district_df, tu_df, user_df)
    st.download_button(
        label="📊 Download Complete Analysis (Multi-Sheet Excel)",
        data=excel_payload,
        file_name="TB_High_Risk_Filtered_Report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
    )
with c_exp2:
    csv_payload = filtered_pt[display_cols].to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📋 Download Filtered Patients (CSV)",
        data=csv_payload,
        file_name="Filtered_High_Risk_Patients.csv",
        mime="text/csv",
        use_container_width=True,
    )