
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Textile Industry Dashboard",
    page_icon="🧵",
    layout="wide"
)

# Screen colors
NAVY = "#17324D"
BLUE = "#2878B5"
TEAL = "#19A7A0"
GOLD = "#F2B134"
LIGHT = "#F3F7FA"

# Application styling
st.markdown(f"""
<style>
.stApp {{
    background-color: {LIGHT};
}}
[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, {NAVY}, {BLUE});
}}
[data-testid="stSidebar"] * {{
    color: white;
}}
.hero {{
    background: linear-gradient(110deg, {NAVY}, {BLUE});
    padding: 25px;
    border-radius: 15px;
    color: white;
}}
.hero h1 {{
    color: white;
}}
div[data-testid="stMetric"] {{
    background: white;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #DCE6ED;
}}
</style>
""", unsafe_allow_html=True)

# Sample textile production data
default_data = pd.DataFrame({
    "Month": [
        "May", "June", "July",
        "August", "September", "October"
    ],
    "Department": [
        "Spinning", "Weaving", "Dyeing",
        "Finishing", "Spinning", "Weaving"
    ],
    "Production (kg)": [
        8200, 7600, 6900, 7200, 8800, 8100
    ],
    "Defective (%)": [
        2.4, 3.1, 4.2, 2.8, 1.9, 2.6
    ],
    "Energy (kWh)": [
        4100, 3900, 4600, 3700, 4200, 4000
    ]
})

if "textile_data" not in st.session_state:
    st.session_state.textile_data = default_data.copy()

# Sidebar navigation
st.sidebar.title("🧵 Textile Hub")
st.sidebar.write("Textile Industry Management")

page = st.sidebar.radio(
    "Select Page",
    [
        "Dashboard",
        "Departments",
        "Production Data",
        "About Project"
    ]
)

st.sidebar.markdown("---")
st.sidebar.subheader("🎨 Screen Colors")

for name, color in [
    ("Navy", NAVY),
    ("Blue", BLUE),
    ("Teal", TEAL),
    ("Gold", GOLD)
]:
    st.sidebar.markdown(
        f'<div style="background:{color};padding:8px;'
        f'border-radius:6px;margin-bottom:5px;'
        f'color:white;">{name}: {color}</div>',
        unsafe_allow_html=True
    )

data = st.session_state.textile_data

def header(title, subtitle):
    st.markdown(
        f'<div class="hero"><h1>{title}</h1>'
        f'<p>{subtitle}</p></div>',
        unsafe_allow_html=True
    )

# PAGE 1: Dashboard
if page == "Dashboard":

    header(
        "Textile Industry Dashboard",
        "Monitor production, quality and energy consumption."
    )

    total = data["Production (kg)"].sum()
    defects = data["Defective (%)"].mean()
    energy = data["Energy (kWh)"].sum()
    departments = data["Department"].nunique()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Production", f"{total:,.0f} kg")
    col2.metric("Average Defects", f"{defects:.1f}%")
    col3.metric("Energy Used", f"{energy:,.0f} kWh")
    col4.metric("Departments", departments)

    left, right = st.columns(2)

    with left:
        st.subheader("Monthly Production")

        fig = px.bar(
            data,
            x="Month",
            y="Production (kg)",
            color="Department",
            color_discrete_sequence=[
                BLUE, TEAL, GOLD, NAVY
            ]
        )

        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.subheader("Quality Control")

        fig = px.line(
            data,
            x="Month",
            y="Defective (%)",
            markers=True,
            color_discrete_sequence=[TEAL]
        )

        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Production Records")
    st.dataframe(data, use_container_width=True, hide_index=True)

    st.info("These figures are sample data for demonstration.")

# PAGE 2: Departments
elif page == "Departments":

    header(
        "Textile Departments",
        "Learn about the main manufacturing processes."
    )

    st.subheader("🧶 1. Spinning")
    st.write(
        "Spinning converts textile fibres into yarn. "
        "Processes include opening, cleaning, carding, "
        "drawing and spinning."
    )

    st.subheader("🧵 2. Weaving")
    st.write(
        "Weaving interlaces warp and weft yarns "
        "to produce woven fabric."
    )

    st.subheader("🎨 3. Dyeing")
    st.write(
        "Dyeing adds color to fibres, yarns or fabrics."
    )

    st.subheader("✨ 4. Finishing")
    st.write(
        "Finishing improves fabric appearance, "
        "softness and performance."
    )

    st.subheader("👕 5. Garment Manufacturing")
    st.write(
        "Fabric is cut, stitched, inspected and packed "
        "to make garments."
    )

    st.divider()
    choice = st.selectbox(
        "Choose a department for quality checks",
        ["Spinning", "Weaving", "Dyeing", "Finishing", "Garmenting"]
    )

    quality_checks = {
        "Spinning": "Yarn count, evenness, twist and strength.",
        "Weaving": "Fabric width, ends, picks and weaving defects.",
        "Dyeing": "Shade matching, pH, temperature and color fastness.",
        "Finishing": "GSM, width, shrinkage and fabric hand feel.",
        "Garmenting": "Measurements, seams and stitching defects."
    }

    st.success(quality_checks[choice])

# PAGE 3: Production Data
elif page == "Production Data":

    header(
        "Production Data",
        "Edit and download textile production records."
    )

    edited_data = st.data_editor(
        data,
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True
    )

    st.session_state.textile_data = edited_data

    csv = edited_data.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇️ Download Production Data",
        data=csv,
        file_name="textile_production.csv",
        mime="text/csv"
    )

    st.warning(
        "Data changes are stored only for the current app session. "
        "Download your CSV to keep a copy."
    )

# PAGE 4: About Project
elif page == "About Project":

    header(
        "About This Project",
        "A Streamlit application for textile industry students."
    )

    st.subheader("Project Objectives")

    st.write("""
    - Display textile production information.
    - Monitor production and defective percentages.
    - Explore textile manufacturing departments.
    - Edit and download production records.
    - Present information with colorful charts.
    """)

    st.subheader("Technologies Used")

    st.write("""
    - Python
    - Streamlit
    - Pandas
    - Plotly
    """)

    st.subheader("How to Run")

    st.code(
        "pip install -r requirements.txt\n"
        "streamlit run App.py",
        language="bash"
    )

    st.info(
        "The built-in production figures are examples, "
        "not verified factory data."
    )

st.markdown("---")
st.caption("Textile Hub | Student Project | Built with Streamlit")
