import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils.data import charger_donnees, get_stas

st.set_page_config(
    page_title="Fraude Bancaire",
    page_icon=":bank:",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "mode_sombre" not in st.session_state:
    st.session_state.mode_sombre = True

sombre = st.session_state.mode_sombre = True

if sombre:
    bg = "#0d0f14"
    bgcard = "#181c26"
    bordure = "rgba(255, 255, 255, 0.07)"
    txt1 = "e8eaf0"
    txt2 = "8892a4"
    txt3 = "4a5568"
    bleu = "#63b3ed"
    rouge = "#fc8181"
    vert = "#68d391"
    orange = "#f6ad55"
    sidebar_bg = "#0a0c10"
    pbg = "#181c26"
    pfront = "#8892a4"
    pgrid = "rgba(255, 255, 255, 0.05)"
else:
    bg = "#f0f2f8"
    bgcard = "#ffffff"
    bordure = "rgba(0, 0, 0, 0.8)"
    txt1 = "1a202c"
    txt2 = "4a5568"
    txt3 = "a0aec0"
    bleu = "#3182ce"
    rouge = "#e53e3e"
    vert = "#276749"
    orange = "#dd6b20"
    sidebar_bg = "#1a202c"
    pbg = "#ffffff"
    pfront = "#4a5568"
    pgrid = "rgba(0, 0, 0, 0.6)"

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap');
    html, body, [class*="css"]  {{
        font-family: 'Syne', sans-serif !important;
    }}
    .stApp {{
        background-color: {bg} !important;
    }}
    .block-container {{
        padding: 2rem 2rem 2rem 2rem !important;
        max-width: 100% !important;
    }}
    [data-testid="stSidebarNav"] {{
        display: none !important;
    }}
    header[data-testid="stHeader"] {{
        display: none !important;
    }}
    #MainMenu {{
        display: none !important;
    }}
    footer {{
        display: none !important;
    }}
    [data-testid="stSidebar"] {{
        background-color: {sidebar_bg} !important;
        min-width: 220px !important;
        max-width: 220px !important;
        border-right: 1px solid {bordure} !important;
    }}
    [data-testid="stSidebar"] * {{
        color: #c8d0e0 !important;
    }}
    h1, h2, h3{{
        color: #{txt1} !important;
        font-family: 'Syne', sans-serif !important;
    }}
    .stButton>button {{
        background: linear-gradient(135deg, {bleu}, #4299e1) !important;
        color: white !important;
        border: none !important;
        boder-radius: 8px !important;
        font-family: 'Syne', sans-serif !important;
        font-weight: 500 !important;
    }}

    .kpi-card {{
        background-color: {bgcard};
        border: 1px solid {bordure};
        border-radius: 12px;
        padding: 20px;
    }}
    .kpi-label {{
    font-size: 11px;
    font-weight: 700;
    color: {txt3};
    letter-spacing: 1px;
    text-transform: uppercase;
    font-family: 'Space Mono', monospace !important;
    margin-bottom: 8px;
}}
.kpi-valeur {{
    font-size: 30px;
    font-weight: 800;
    color: {txt1};
    font-family: 'Syne', sans-serif !important;
    line-height: 1;
    margin-bottom: 6px;
}}
.kpi-valeur.rouge {{ color: {rouge}; }}
.kpi-valeur.bleu  {{ color: {bleu};  }}
.kpi-sous {{
    font-size: 11px;
    color: {txt3};
    font-family: 'Space Mono', monospace !important;
}}
.badge {{
    display: inline-block;
    padding: 3px 8px;
    border-radius: 4px;
    font-size: 10px;
    font-weight: 700;
    font-family: 'Space Mono', monospace !important;
}}
.badge.rouge {{
    background: rgba(252,129,129,0.15);
    color: {rouge};
    border: 1px solid rgba(252,129,129,0.3);
}}
.badge.vert {{
    background: rgba(104,211,145,0.12);
    color: {vert};
    border: 1px solid rgba(104,211,145,0.25);
}}
.badge.orange {{
    background: rgba(246,173,85,0.15);
    color: {orange};
    border: 1px solid rgba(246,173,85,0.3);
}}

/* Barre de navigation */
.nav-item {{
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 9px 12px;
    border-radius: 7px;
    margin-bottom: 2px;
    font-size: 13px;
    font-weight: 600;
    color: #8892a4 !important;
}}
.nav-item.actif {{
    background: rgba(99,179,237,0.18);
    color: {bleu} !important;
}}
.nav-point {{
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: {bleu};
    margin-left: auto;
}}


/* Tableau des alertes */
.tableau-alertes {{
    width: 100%;
    border-collapse: collapse;
}}
.tableau-alertes th {{
    font-size: 10px;
    font-weight: 700;
    color: {txt3};
    letter-spacing: 1px;
    text-transform: uppercase;
    font-family: 'Space Mono', monospace !important;
    padding: 8px 12px;
    text-align: left;
    border-bottom: 1px solid {bordure};
}}
.tableau-alertes td {{
    padding: 12px;
    font-size: 12px;
    color: {txt2};
    font-family: 'Space Mono', monospace !important;
    border-bottom: 1px solid {bordure};
}}
.tableau-alertes tr:last-child td {{
    border-bottom: none;
}}
.id-entite {{
    color: {bleu} !important;
    font-weight: 700;
}}
.tag-anomalie {{
    display: inline-block;
    padding: 3px 7px;
    border-radius: 4px;
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 0.8px;
    font-family: 'Space Mono', monospace !important;
    background: rgba(252,129,129,0.12);
    color: {rouge};
    border: 1px solid rgba(252,129,129,0.2);
}}
.btn-investig {{
    padding: 4px 10px;
    border-radius: 5px;
    font-size: 10px;
    font-weight: 700;
    font-family: 'Space Mono', monospace !important;
    background: rgba(99,179,237,0.12);
    color: {bleu};
    border: 1px solid rgba(99,179,237,0.25);
}}
.session-badge {{
    margin: auto 12px 16px;
    padding: 10px 12px;
    background: rgba(104,211,145,0.08);
    border: 1px solid rgba(104,211,145,0.2);
    border-radius: 8px;
    font-size: 11px;
    color: #68d391 !important;
    font-family: 'Space Mono', monospace !important;
}}
.pied-page {{
    display: flex;
    justify-content: space-between;
    padding: 14px 0 0;
    border-top: 1px solid {bordure};
    margin-top: 20px;
    font-size: 11px;
    color: {txt3};
    font-family: 'Space Mono', monospace !important;
}}

    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    # Logo et nom
    st.markdown(f"""
    <div style='display:flex;align-items:center;gap:10px;
                padding:20px 16px 12px;
                border-bottom:1px solid rgba(255,255,255,0.06);
                margin-bottom:8px'>
        <div style='width:32px;height:32px;
                    background:linear-gradient(135deg,#63b3ed,#4299e1);
                    border-radius:8px;display:flex;align-items:center;
                    justify-content:center;font-size:16px'>🛡️</div>
        <span style='font-family:Syne,sans-serif;font-weight:800;
                     font-size:15px;color:#e8eaf0;letter-spacing:1.5px'>
            VIGILANCE AI
        </span>
    </div>

    <div style='margin:8px 12px 16px;padding:10px 12px;
                background:rgba(255,255,255,0.04);
                border-radius:8px;
                border:1px solid rgba(255,255,255,0.06)'>
        <div style='font-size:13px;font-weight:700;color:#e8eaf0'>
            Investigateur Principal
        </div>
        <div style='font-size:11px;color:#8892a4;
                    font-family:Space Mono,monospace'>
            Sécurité Institutionnelle
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Menu de navigation
    pages = [
        ("", "Tableau de Bord",   True),
        ("",  "Exploration",       False),
        ("", "Nettoyage",         False),
        ("", "Analyse",           False),
        ("",  "Visualisations",    False),
        ("", "Profil des Fraudes",False),
    ]
    for icone, nom, actif in pages:
        classe = "nav-item actif" if actif else "nav-item"
        point  = "<span class='nav-point'></span>" if actif else ""
        st.markdown(
            f"<div class='{classe}'>{icone}&nbsp;&nbsp;{nom}{point}</div>",
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Bouton thème clair / sombre
    label_theme = "☀️ Mode Clair" if sombre else "🌙 Mode Sombre"
    if st.button(label_theme, use_container_width=True):
        st.session_state.mode_sombre = not sombre
        st.rerun()

    st.markdown(f"""
    <br>
    <div class='session-badge'>
        🟢 &nbsp;Session Active<br>
        <span style='opacity:0.7'>Système: v1.0.0</span>
    </div>
    """, unsafe_allow_html=True)
# ── Chargement des données ───────────────────────────────────
df_brut, df = charger_donnees()
stats       = get_stas(df)

# ── Barre du haut ────────────────────────────────────────────
st.markdown(
"<div style='display:flex;align-items:center;justify-content:space-between;"
"margin-bottom:24px;padding-bottom:16px;border-bottom:1px solid " + bordure + "'>"
"<div style='display:flex;align-items:center;gap:10px'>"
"<div style='width:28px;height:28px;background:rgba(99,179,237,0.12);border:1px solid rgba(99,179,237,0.3);"
"border-radius:6px;display:flex;align-items:center;justify-content:center;font-size:14px'>🛡️</div>"
"<span style='font-size:18px;font-weight:800;color:#e8eaf0;letter-spacing:2px;text-transform:uppercase;"
"font-family:Space Mono,monospace'>OVERVIEW</span>"
"</div>"
"<div style='display:flex;align-items:center;gap:12px'>"
"<div style='display:flex;align-items:center;gap:8px;background:" + bgcard + ";border:1px solid " + bordure + ";"
"border-radius:8px;padding:8px 14px;min-width:280px'>"
"<span style='font-size:13px;color:" + txt3 + "'>🔍</span>"
"<span style='font-size:12px;color:" + txt3 + ";font-family:Space Mono,monospace'>Rechercher des dossiers d'enquête...</span>"
"</div>"
"<div style='display:flex;align-items:center;gap:7px;background:" + bgcard + ";border:1px solid " + bordure + ";"
"border-radius:8px;padding:8px 14px;cursor:pointer'>"
"<span style='font-size:13px'>⚙️</span>"
"<span style='font-size:12px;font-weight:600;color:" + txt2 + ";font-family:Space Mono,monospace'>Filtres globaux</span>"
"</div>"
"</div>"
"</div>",
unsafe_allow_html=True)

# ── Cartes KPI ───────────────────────────────────────────────
# On crée 4 colonnes côte à côte
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class='kpi-card'>
        <div class='kpi-label'>Total Transactions</div>
        <div class='kpi-valeur'>{stats['total']:,}</div>
        <div class='kpi-sous'>
            <span class='badge vert'>↑ +12.5% vs semaine passée</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class='kpi-card'>
        <div class='kpi-label'>Taux de Fraude</div>
        <div class='kpi-valeur rouge'>{stats['taux_fraude']}%</div>
        <div class='kpi-sous'>
            <span class='badge rouge'>⚠ Seuil Critique</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class='kpi-card'>
        <div class='kpi-label'>Cas de Fraude</div>
        <div class='kpi-valeur'>{stats['nb_fraudes']}</div>
        <div class='kpi-sous'>
            <span class='badge orange'>
                ⏳ {min(stats['nb_fraudes'], 24)} En Attente de Révision
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class='kpi-card'>
        <div class='kpi-label'>Indice de Risque</div>
        <div class='kpi-valeur bleu'>Modéré</div>
        <div class='kpi-sous'>
            <span class='badge vert'>● Stable</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Graphique + Alertes par région ───────────────────────────
col_graphique, col_region = st.columns([3, 2], gap="medium")

with col_graphique:
    st.markdown(f"""
    <div style='font-size:12px;font-weight:700;color:{txt1};
                letter-spacing:1.2px;text-transform:uppercase;
                font-family:Space Mono,monospace;margin-bottom:4px'>
        Vélocité des Transactions
    </div>
    <div style='font-size:11px;color:{txt2};margin-bottom:12px'>
        Surveillance du débit sur 24 heures
    </div>
    """, unsafe_allow_html=True)

    # On simule des données sur 24h avec une anomalie à 07:00
    np.random.seed(42)
    heures     = list(range(24))
    valeurs    = np.random.randint(20, 80, 24)
    valeurs[7] = 95  # pic anormal

    couleurs = [rouge if i == 7 else "rgba(99,179,237,0.4)" for i in range(24)]

    fig_vel = go.Figure(go.Bar(
        x=[f"{h:02d}:00" for h in heures],
        y=valeurs,
        marker_color=couleurs,
        marker_line_width=0,
    ))

    # Annotation sur le pic
    fig_vel.add_annotation(
        x="07:00", y=95,
        text="ANOMALIE DÉTECTÉE",
        showarrow=True,
        arrowhead=2,
        arrowcolor=rouge,
        bgcolor="rgba(252,129,129,0.2)",
        bordercolor=rouge,
        font=dict(color=rouge, size=9, family="Space Mono"),
        ax=0, ay=-30
    )

    fig_vel.update_layout(
        height=280,
        paper_bgcolor=pbg,
        plot_bgcolor=pbg,
        font=dict(color=pfront, family="Syne"),
        margin=dict(l=10, r=10, t=10, b=10),
        showlegend=False,
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            color=pfront,
            tickfont=dict(size=9, family="Space Mono"),
            tickvals=[f"{h:02d}:00" for h in [0,4,8,12,16,20,23]],
            ticktext=["00:00","04:00","08:00","12:00","16:00","20:00","23:59"]
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor=pgrid,
            zeroline=False,
            color=pfront,
            tickfont=dict(size=9, family="Space Mono")
        ),
    )
    st.plotly_chart(fig_vel, use_container_width=True,
                    config={"displayModeBar": False})

with col_region:
    st.markdown(f"""
    <div style='font-size:12px;font-weight:700;color:{txt1};
                letter-spacing:1.2px;text-transform:uppercase;
                font-family:Space Mono,monospace;margin-bottom:16px'>
        Alertes de Fraude par Région
    </div>
    """, unsafe_allow_html=True)

    # Calcul des vraies données par région
    fraudes_region = df.groupby("region")["fraude"].sum().sort_values(ascending=False)
    max_val        = fraudes_region.max()

    for region, nb in fraudes_region.items():
        pct       = int(nb / max_val * 100)
        est_rouge = "rouge" if nb == max_val else ""
        couleur_b = rouge if nb == max_val else bleu
        st.markdown(f"""
        <div style='display:flex;align-items:center;
                    padding:10px 0;
                    border-bottom:1px solid {bordure}'>
            <div style='font-size:12px;font-weight:600;
                        color:{txt1};width:100px'>{region}</div>
            <div style='flex:1;margin:0 12px;height:4px;
                        background:{bordure};border-radius:2px'>
                <div style='height:100%;width:{pct}%;
                            background:{couleur_b};
                            border-radius:2px'></div>
            </div>
            <div style='font-size:11px;font-weight:700;
                        color:{couleur_b};
                        font-family:Space Mono;
                        white-space:nowrap'>{int(nb)} Alertes</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Tableau des alertes critiques ────────────────────────────
st.markdown(
"<div style='background:" + bgcard + ";border:1px solid " + bordure + ";border-radius:12px;padding:20px'>"
"<div style='display:flex;align-items:center;gap:8px;margin-bottom:16px'>"
"<span style='font-size:16px;color:" + rouge + "'>⚠</span>"
"<span style='font-size:14px;font-weight:700;color:" + txt1 + ";font-family:Syne'>Alertes Critiques Suspectes</span>"
"<div style='width:8px;height:8px;border-radius:50%;background:" + vert + ";margin-left:12px'></div>"
"<span style='font-size:10px;color:" + vert + ";font-family:Space Mono'>Surveillance en Direct</span>"
"<span style='margin-left:auto;font-size:10px;font-weight:700;color:" + bleu + ";font-family:Space Mono;cursor:pointer'>VOIR TOUTES LES ALERTES</span>"
"</div>"
"<div style='display:grid;grid-template-columns:1fr 1.2fr 1.5fr 1.2fr 1fr 0.8fr;border-top:1px solid " + bordure + "'>"
"<div style='font-size:10px;font-weight:700;color:" + txt3 + ";letter-spacing:1px;text-transform:uppercase;font-family:Space Mono;padding:8px 12px;border-bottom:1px solid " + bordure + "'>HORODATAGE</div>"
"<div style='font-size:10px;font-weight:700;color:" + txt3 + ";letter-spacing:1px;text-transform:uppercase;font-family:Space Mono;padding:8px 12px;border-bottom:1px solid " + bordure + "'>ID ENTITÉ</div>"
"<div style='font-size:10px;font-weight:700;color:" + txt3 + ";letter-spacing:1px;text-transform:uppercase;font-family:Space Mono;padding:8px 12px;border-bottom:1px solid " + bordure + "'>SCORE DE RISQUE</div>"
"<div style='font-size:10px;font-weight:700;color:" + txt3 + ";letter-spacing:1px;text-transform:uppercase;font-family:Space Mono;padding:8px 12px;border-bottom:1px solid " + bordure + "'>TYPE D'ANOMALIE</div>"
"<div style='font-size:10px;font-weight:700;color:" + txt3 + ";letter-spacing:1px;text-transform:uppercase;font-family:Space Mono;padding:8px 12px;border-bottom:1px solid " + bordure + "'>LOCALISATION</div>"
"<div style='font-size:10px;font-weight:700;color:" + txt3 + ";letter-spacing:1px;text-transform:uppercase;font-family:Space Mono;padding:8px 12px;border-bottom:1px solid " + bordure + "'>ACTION</div>"
"<div style='font-size:12px;color:" + txt2 + ";font-family:Space Mono;padding:12px;border-bottom:1px solid " + bordure + "'>14:23:45</div>"
"<div style='font-size:12px;color:" + bleu + ";font-weight:700;font-family:Space Mono;padding:12px;border-bottom:1px solid " + bordure + "'>USR-9482-TU</div>"
"<div style='padding:12px;border-bottom:1px solid " + bordure + ";display:flex;align-items:center;gap:8px'><div style='width:92px;height:4px;border-radius:2px;background:linear-gradient(90deg," + orange + "," + rouge + ")'></div><span style='color:" + rouge + ";font-weight:700;font-size:11px;font-family:Space Mono'>92%</span></div>"
"<div style='padding:12px;border-bottom:1px solid " + bordure + "'><span style='display:inline-block;padding:3px 7px;border-radius:4px;font-size:9px;font-weight:700;font-family:Space Mono;background:rgba(252,129,129,0.12);color:" + rouge + ";border:1px solid rgba(252,129,129,0.2)'>VÉLOCITÉ RAPIDE</span></div>"
"<div style='font-size:12px;color:" + txt2 + ";font-family:Space Mono;padding:12px;border-bottom:1px solid " + bordure + "'>Singapour (SGP)</div>"
"<div style='padding:12px;border-bottom:1px solid " + bordure + "'><span style='padding:4px 10px;border-radius:5px;font-size:10px;font-weight:700;font-family:Space Mono;background:rgba(99,179,237,0.12);color:" + bleu + ";border:1px solid rgba(99,179,237,0.25)'>ENQUÊTER</span></div>"
"<div style='font-size:12px;color:" + txt2 + ";font-family:Space Mono;padding:12px;border-bottom:1px solid " + bordure + "'>14:18:12</div>"
"<div style='font-size:12px;color:" + bleu + ";font-weight:700;font-family:Space Mono;padding:12px;border-bottom:1px solid " + bordure + "'>VND-0012-BT</div>"
"<div style='padding:12px;border-bottom:1px solid " + bordure + ";display:flex;align-items:center;gap:8px'><div style='width:74px;height:4px;border-radius:2px;background:linear-gradient(90deg," + orange + "," + rouge + ")'></div><span style='color:" + rouge + ";font-weight:700;font-size:11px;font-family:Space Mono'>74%</span></div>"
"<div style='padding:12px;border-bottom:1px solid " + bordure + "'><span style='display:inline-block;padding:3px 7px;border-radius:4px;font-size:9px;font-weight:700;font-family:Space Mono;background:rgba(252,129,129,0.12);color:" + rouge + ";border:1px solid rgba(252,129,129,0.2)'>VIOLATION GÉOFENCE</span></div>"
"<div style='font-size:12px;color:" + txt2 + ";font-family:Space Mono;padding:12px;border-bottom:1px solid " + bordure + "'>Moscou (RUS)</div>"
"<div style='padding:12px;border-bottom:1px solid " + bordure + "'><span style='padding:4px 10px;border-radius:5px;font-size:10px;font-weight:700;font-family:Space Mono;background:rgba(99,179,237,0.12);color:" + bleu + ";border:1px solid rgba(99,179,237,0.25)'>ENQUÊTER</span></div>"
"<div style='font-size:12px;color:" + txt2 + ";font-family:Space Mono;padding:12px'>14:05:33</div>"
"<div style='font-size:12px;color:" + bleu + ";font-weight:700;font-family:Space Mono;padding:12px'>CRD-8821-UP</div>"
"<div style='padding:12px;display:flex;align-items:center;gap:8px'><div style='width:88px;height:4px;border-radius:2px;background:linear-gradient(90deg," + orange + "," + rouge + ")'></div><span style='color:" + rouge + ";font-weight:700;font-size:11px;font-family:Space Mono'>88%</span></div>"
"<div style='padding:12px'><span style='display:inline-block;padding:3px 7px;border-radius:4px;font-size:9px;font-weight:700;font-family:Space Mono;background:rgba(252,129,129,0.12);color:" + rouge + ";border:1px solid rgba(252,129,129,0.2)'>MOTIF INHABITUEL</span></div>"
"<div style='font-size:12px;color:" + txt2 + ";font-family:Space Mono;padding:12px'>New York (USA)</div>"
"<div style='padding:12px'><span style='padding:4px 10px;border-radius:5px;font-size:10px;font-weight:700;font-family:Space Mono;background:rgba(99,179,237,0.12);color:" + bleu + ";border:1px solid rgba(99,179,237,0.25)'>ENQUÊTER</span></div>"
"</div></div>",
unsafe_allow_html=True)

# ── Pied de page ─────────────────────────────────────────────
st.markdown(f"""
<div class='pied-page'>
    <span>Vigilance AI — Moteur d'Intelligence v1.0 &nbsp;•&nbsp;
          Niveau de Confidentialité : Chiffré</span>
    <div style='display:flex;gap:20px'>
        <span style='cursor:pointer'>État du Système</span>
        <span style='cursor:pointer'>Journaux de Conformité</span>
        <span style='cursor:pointer'>Support</span>
    </div>
</div>
""", unsafe_allow_html=True)