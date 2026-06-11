import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(layout="wide", page_title="Cybersecurity Threat Assessment")

BASE_DIR = Path(__file__).resolve().parent
csv_path = BASE_DIR.parent / "data" / "raw-data.csv"

df = pd.read_csv(csv_path)
df['Financial Loss (in Billion $)'] = df['Financial Loss (in Million $)'] / 1000

# ==========================================
# DARK THEME GLOBAL
# ==========================================
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        * { font-family: 'Inter', sans-serif; }

        .stApp { background-color: #0f172a; color: #f1f5f9; }

        /* ---- Sidebar ---- */
        section[data-testid="stSidebar"] {
            background-color: #1e293b;
            border-right: 1px solid #334155;
        }
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3 {
            color: #f1f5f9 !important;
            font-size: 15px;
            font-weight: 600;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            margin-bottom: 12px;
        }

        /* Multiselect labels */
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] .stMultiSelect label p {
            color: #cbd5e1 !important;
            font-size: 12px !important;
            font-weight: 500 !important;
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }

        /* Multiselect box — semua layer container */
        section[data-testid="stSidebar"] .stMultiSelect [data-baseweb="select"],
        section[data-testid="stSidebar"] .stMultiSelect [data-baseweb="select"] > div,
        section[data-testid="stSidebar"] .stMultiSelect [data-baseweb="select"] > div > div,
        section[data-testid="stSidebar"] .stMultiSelect div[class*="multiValue"],
        section[data-testid="stSidebar"] div[data-testid="stMultiSelect"] > div,
        section[data-testid="stSidebar"] div[data-testid="stMultiSelect"] > div > div {
            background-color: #0f172a !important;
            border-color: #334155 !important;
        }

        /* Wrapper terluar multiselect */
        section[data-testid="stSidebar"] .stMultiSelect > div {
            background-color: #0f172a !important;
            border: 1px solid #334155 !important;
            border-radius: 8px !important;
        }

        /* Teks dalam multiselect */
        section[data-testid="stSidebar"] .stMultiSelect [data-baseweb="select"] span,
        section[data-testid="stSidebar"] .stMultiSelect input,
        section[data-testid="stSidebar"] .stMultiSelect input::placeholder {
            color: #f1f5f9 !important;
            background-color: transparent !important;
        }

        /* Tag/chip terpilih */
        section[data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] {
            background-color: #ef4444 !important;
            border-radius: 6px !important;
        }
        section[data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] span {
            color: #ffffff !important;
            font-size: 12px !important;
        }

        /* Header toolbar Streamlit */
        header[data-testid="stHeader"] {
            background-color: #0f172a !important;
            border-bottom: 1px solid #1e293b !important;
        }

        /* Divider */
        hr { border-color: #1e293b !important; margin: 0.5rem 0 !important; }

        /* Markdown paragraph */
        .stMarkdown p { color: #f1f5f9; }

        /* Insight box */
        .insight-box {
            background-color: #1e293b;
            border-left: 4px solid #3b82f6;
            border-radius: 8px;
            padding: 14px 20px;
            margin: 4px 0 20px 0;
            color: #94a3b8;
            font-size: 13px;
            font-style: italic;
            line-height: 1.6;
        }

        /* Section heading */
        .section-heading {
            color: #f1f5f9;
            font-size: 18px;
            font-weight: 600;
            margin: 0 0 16px 0;
            padding-bottom: 10px;
            border-bottom: 1px solid #1e293b;
        }

        /* KPI card wrapper spacing */
        .block-container { padding-top: 1.5rem !important; }

        /* Remove default streamlit top padding */
        .stPlotlyChart { border-radius: 12px; overflow: hidden; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# SIDEBAR FILTERS
# ==========================================
st.sidebar.header("Filters")

year_options = sorted(df['Year'].unique())
selected_years = st.sidebar.multiselect("Year", year_options, default=year_options)

country_options = sorted(df['Country'].unique())
selected_countries = st.sidebar.multiselect("Country", country_options, default=country_options)

attack_type_options = sorted(df['Attack Type'].unique())
selected_attack_types = st.sidebar.multiselect("Attack Type", attack_type_options, default=attack_type_options)

industry_options = sorted(df['Target Industry'].unique())
selected_industries = st.sidebar.multiselect("Target Industry", industry_options, default=industry_options)

filtered_df = df[
    (df['Year'].isin(selected_years)) &
    (df['Country'].isin(selected_countries)) &
    (df['Attack Type'].isin(selected_attack_types)) &
    (df['Target Industry'].isin(selected_industries))
]

# ==========================================
# TITLE
# ==========================================
st.markdown("""
    <h1 style='color:#f1f5f9; font-size:40px; font-weight:700; margin-bottom:4px;'>
        Cybersecurity Threat Assessment Dashboard
    </h1>
    <p style='color:#64748b; font-size:13px; margin-top:0; margin-bottom:16px;'>
        Monitoring global cyber incidents, financial exposure, and response performance
    </p>
""", unsafe_allow_html=True)
st.divider()

# ==========================================
# KPI CARDS
# ==========================================
total_loss = filtered_df['Financial Loss (in Billion $)'].sum()
total_attacks = filtered_df.shape[0]
avg_response_time = filtered_df['Incident Resolution Time (in Hours)'].mean()

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div style="background:linear-gradient(135deg,#1d4ed8,#2563eb);
                    padding:20px 24px; border-radius:12px; border:1px solid #3b82f6;">
            <p style="color:#bfdbfe; margin:0 0 6px 0; font-size:12px;
                      font-weight:600; letter-spacing:0.08em; text-transform:uppercase;">
                Total Financial Loss
            </p>
            <p style="color:#ffffff; margin:0; font-size:30px; font-weight:700; line-height:1;">
                ${:,.2f}B
            </p>
        </div>
    """.format(total_loss), unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div style="background:linear-gradient(135deg,#6d28d9,#7c3aed);
                    padding:20px 24px; border-radius:12px; border:1px solid #8b5cf6;">
            <p style="color:#ddd6fe; margin:0 0 6px 0; font-size:12px;
                      font-weight:600; letter-spacing:0.08em; text-transform:uppercase;">
                Total Attacks
            </p>
            <p style="color:#ffffff; margin:0; font-size:30px; font-weight:700; line-height:1;">
                {:,}
            </p>
        </div>
    """.format(total_attacks), unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div style="background:linear-gradient(135deg,#0f766e,#0d9488);
                    padding:20px 24px; border-radius:12px; border:1px solid #14b8a6;">
            <p style="color:#99f6e4; margin:0 0 6px 0; font-size:12px;
                      font-weight:600; letter-spacing:0.08em; text-transform:uppercase;">
                Avg Response Time
            </p>
            <p style="color:#ffffff; margin:0; font-size:30px; font-weight:700; line-height:1;">
                {:.2f}H
            </p>
        </div>
    """.format(avg_response_time), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.divider()

# ==========================================
# CHART THEME
# ==========================================
def chart_layout(extra=None):
    base = dict(
        paper_bgcolor='#1e293b',
        plot_bgcolor='#1e293b',
        font=dict(color='#ffffff', size=13),
        title_font=dict(color='#ffffff', size=15),
        legend=dict(font=dict(color='#ffffff')),
        margin=dict(t=50, b=20, l=20, r=20),
        xaxis=dict(gridcolor='#334155', color='#ffffff', tickfont=dict(color='#ffffff')),
        yaxis=dict(gridcolor='#334155', color='#ffffff', tickfont=dict(color='#ffffff'))
    )
    if extra:
        base.update(extra)
    return base

# ==========================================
# ROW 1: Financial Loss by Industry | by Country
# ==========================================
st.markdown("<p class='section-heading'>Financial Loss Overview</p>", unsafe_allow_html=True)
col_l, col_r = st.columns(2)

with col_l:
    loss_industry = (
        filtered_df.groupby('Target Industry')['Financial Loss (in Billion $)']
        .sum().sort_values(ascending=True).reset_index()
    )
    fig1 = px.bar(
        loss_industry, x='Financial Loss (in Billion $)', y='Target Industry',
        orientation='h', title='Financial Loss by Target Industry',
        text='Financial Loss (in Billion $)'
    )
    fig1.update_traces(texttemplate='$%{text:.2f}B', textposition='outside', marker_color='#3b82f6')
    fig1.update_layout(**chart_layout())
    st.plotly_chart(fig1, use_container_width=True)

with col_r:
    loss_country = (
        filtered_df.groupby('Country')['Financial Loss (in Billion $)']
        .sum().sort_values(ascending=True).reset_index()
    )
    fig2 = px.bar(
        loss_country, x='Financial Loss (in Billion $)', y='Country',
        orientation='h', title='Financial Loss by Country',
        text='Financial Loss (in Billion $)'
    )
    fig2.update_traces(texttemplate='$%{text:.2f}B', textposition='outside', marker_color='#8b5cf6')
    fig2.update_layout(**chart_layout())
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("""
    <div class="insight-box">
        💡 <b>Insight:</b> Financial Loss per Industri maupun per Negara menunjukkan distribusi yang sangat merata — selisih antara nilai tertinggi dan terendah kurang dari $5B untuk industri dan kurang dari $3B untuk negara. Hal ini mengindikasikan serangan siber tidak mengincar sektor atau wilayah tertentu secara spesifik.
    </div>
""", unsafe_allow_html=True)

st.divider()

# ==========================================
# ROW 2: Attack Count by Year | Avg Response Time by Year
# ==========================================
st.markdown("<p class='section-heading'>Time Series Analysis</p>", unsafe_allow_html=True)
col_l2, col_r2 = st.columns(2)

with col_l2:
    year_counts = filtered_df['Year'].value_counts().sort_index().reset_index()
    year_counts.columns = ['Year', 'Attack Count']
    fig3 = px.line(
        year_counts, x='Year', y='Attack Count',
        markers=True, title='Attack Count by Year'
    )
    fig3.update_traces(line_color='#38bdf8', marker=dict(color='#38bdf8'))
    fig3.update_layout(**chart_layout(
        extra=dict(xaxis=dict(tickmode='linear', dtick=1, gridcolor='#334155',
                              color='#ffffff', tickfont=dict(color='#ffffff')))
    ))
    st.plotly_chart(fig3, use_container_width=True)

with col_r2:
    year_resolution = (
        filtered_df.groupby('Year')['Incident Resolution Time (in Hours)']
        .mean().reset_index()
    )
    year_resolution.columns = ['Year', 'Avg Resolution Time (Hours)']
    fig4 = px.line(
        year_resolution, x='Year', y='Avg Resolution Time (Hours)',
        markers=True, title='Average Resolution Time by Year'
    )
    fig4.update_traces(line_color='#34d399', marker=dict(color='#34d399'))
    fig4.update_layout(**chart_layout(
        extra=dict(xaxis=dict(tickmode='linear', dtick=1, gridcolor='#334155',
                              color='#ffffff', tickfont=dict(color='#ffffff')))
    ))
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("""
    <div class="insight-box">
        💡 <b>Insight:</b> Jumlah serangan maupun rata-rata resolution time keduanya tidak menunjukkan tren yang konsisten — keduanya fluktuatif dari tahun ke tahun tanpa pola naik atau turun yang jelas. Attack count mencapai titik terendah di 2019 dan kembali memuncak di 2022, sementara resolution time bergerak dalam rentang ~35.5–38.5 jam, mengindikasikan bahwa faktor tahun tidak berpengaruh signifikan terhadap kedua metrik ini.
    </div>
""", unsafe_allow_html=True)

st.divider()

# ==========================================
# ROW 3: Security Vulnerability Type | Attack Source
# ==========================================
st.markdown("<p class='section-heading'>Attack Distribution</p>", unsafe_allow_html=True)
col_l3, col_r3 = st.columns(2)

with col_l3:
    vuln_counts = filtered_df['Security Vulnerability Type'].value_counts().reset_index()
    vuln_counts.columns = ['Security Vulnerability Type', 'Count']
    fig5 = px.pie(
        vuln_counts, names='Security Vulnerability Type', values='Count',
        title='Attack Count by Security Vulnerability Type'
    )
    fig5.update_traces(textfont=dict(color='#ffffff', size=13))
    fig5.update_layout(**chart_layout())
    st.plotly_chart(fig5, use_container_width=True)

with col_r3:
    source_counts = filtered_df['Attack Source'].value_counts().reset_index()
    source_counts.columns = ['Attack Source', 'Count']
    fig6 = px.pie(
        source_counts, names='Attack Source', values='Count',
        title='Attack Count by Attack Source'
    )
    fig6.update_traces(textfont=dict(color='#ffffff', size=13))
    fig6.update_layout(**chart_layout())
    st.plotly_chart(fig6, use_container_width=True)

st.markdown("""
    <div class="insight-box">
        💡 <b>Insight:</b> Distribusi Security Vulnerability Type maupun Attack Source terbilang merata antar kategori, mengindikasikan tidak ada satu vektor serangan yang dominan secara signifikan dibanding yang lain. Meski selisihnya kecil, Weak Passwords tetap dapat ditekan dengan menerapkan SPO password yang mewajibkan kombinasi karakter kuat dan penggantian berkala, sehingga berpotensi mengurangi ~24.3% vektor serangan yang seharusnya paling mudah dicegah. Dari sisi Attack Source, Insider threat menyumbang 25.1% — angka yang signifikan mengingat serangan dari dalam jauh lebih sulit dideteksi. Disarankan untuk melakukan pengecekan dan audit akses anggota instansi/organisasi secara berkala guna memitigasi risiko ini sejak dini.
    </div>
""", unsafe_allow_html=True)
