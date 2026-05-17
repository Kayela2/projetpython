import streamlit as st
import numpy as np
import plotly.graph_objects as go
import sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils.data import charger_donnees, get_stas
from utils.theme import get_colors, inject_css, render_sidebar

st.set_page_config(
    page_title="FraudLens — Tableau de Bord",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "mode_sombre" not in st.session_state:
    st.session_state.mode_sombre = True
if "periode_vel" not in st.session_state:
    st.session_state.periode_vel = "24h"
if "show_map" not in st.session_state:
    st.session_state.show_map = False
if "langue" not in st.session_state:
    st.session_state.langue = "FR"

sombre = st.session_state.mode_sombre
t = get_colors(sombre)
inject_css(t)
render_sidebar(sombre)

df_brut, df = charger_donnees()
stats     = get_stas(df)
df_fraude = df[df["fraude"] == 1]

_T = {
    "FR": dict(
        search="Rechercher : région, carte, montant, 'fraude'…",
        admin="Administrateur",
        total_tx="Total Transactions",   total_sub="Enregistrements analysés",
        taux="Taux de Fraude",           taux_sub="Prévalence détectée",
        cas="Cas de Fraude",             cas_sub="Alertes confirmées",
        risque="Index de Risque",
        vel_titre="Vélocité des Transactions", vel_sub="Analyse du flux temps réel",
        ano24="⊙ ANOMALIE DÉTECTÉE", ano7j="⊙ PIC ANORMAL — JEU", ano30="⊙ ANOMALIE — J13",
        regions="Alertes par Région",    incidents="incidents",
        planisphere="🌍  Voir le Planisphère", masquer="🗺️  Masquer le Planisphère",
        alertes="Alertes Critiques Récentes",
        export="⬇  Export",             enqueter="Enquêter",
        voir="Voir toutes les alertes critiques",
        res_titre="Résultats de recherche",
        res_aucun="Aucun résultat pour",
        res_autres="autres résultats",
        col_region="Région", col_carte="Type carte", col_genre="Genre",
        col_montant="Montant", col_fraude="Statut",
        fraude_lbl="Fraude", legitime="Légitime",
    ),
    "EN": dict(
        search="Search: region, card type, amount, 'fraud'…",
        admin="Administrator",
        total_tx="Total Transactions",   total_sub="Records analyzed",
        taux="Fraud Rate",               taux_sub="Detected prevalence",
        cas="Fraud Cases",               cas_sub="Confirmed alerts",
        risque="Risk Index",
        vel_titre="Transaction Velocity", vel_sub="Real-time flow analysis",
        ano24="⊙ ANOMALY DETECTED", ano7j="⊙ ABNORMAL PEAK — THU", ano30="⊙ ANOMALY — D13",
        regions="Alerts by Region",      incidents="incidents",
        planisphere="🌍  View Planisphere", masquer="🗺️  Hide Planisphere",
        alertes="Recent Critical Alerts",
        export="⬇  Export",             enqueter="Investigate",
        voir="View all critical alerts",
        res_titre="Search results",
        res_aucun="No results for",
        res_autres="more results",
        col_region="Region", col_carte="Card type", col_genre="Gender",
        col_montant="Amount", col_fraude="Status",
        fraude_lbl="Fraud", legitime="Legitimate",
    ),
}
langue = st.session_state.langue
L = _T[langue]

# ── Barre du haut ────────────────────────────────────────────
bar_l, bar_mid, bar_r = st.columns([3, 0.7, 2.5], gap="small")

with bar_l:
    requete = st.text_input("", placeholder=L['search'],
                            key="search_q", label_visibility="collapsed")

with bar_mid:
    lc1, lc2 = st.columns(2)
    with lc1:
        if st.button("FR", key="btn_fr",
                     type="primary" if langue == "FR" else "secondary",
                     use_container_width=True):
            st.session_state.langue = "FR"
            st.rerun()
    with lc2:
        if st.button("EN", key="btn_en",
                     type="primary" if langue == "EN" else "secondary",
                     use_container_width=True):
            st.session_state.langue = "EN"
            st.rerun()

with bar_r:
    st.markdown(f"""
    <div style='display:flex;align-items:center;gap:14px;justify-content:flex-end;padding-top:6px'>
        <span style='font-size:16px;cursor:pointer;color:{t["txt2"]}'><i class="fa-solid fa-bell"></i></span>
        <span style='font-size:16px;cursor:pointer;color:{t["txt2"]}'><i class="fa-solid fa-globe"></i></span>
    </div>""", unsafe_allow_html=True)

st.markdown(f"<div style='border-bottom:1px solid {t['bordure']};margin-bottom:20px;margin-top:8px'></div>",
            unsafe_allow_html=True)

# ── Résultats de recherche ───────────────────────────────────
if requete and len(requete.strip()) >= 2:
    q = requete.strip().lower()

    mask = (
        df['region'].str.lower().str.contains(q, na=False) |
        df['type_carte'].str.lower().str.contains(q, na=False) |
        df['genre'].str.lower().str.contains(q, na=False)
    )
    if any(kw in q for kw in ('fraude', 'fraud', 'frauduleux')):
        mask = mask | (df['fraude'] == 1)
    try:
        val = float(q.replace(',', '.').replace(' ', ''))
        mask = mask | df['montant_transaction'].between(val * 0.85, val * 1.15)
    except ValueError:
        pass

    nb       = int(mask.sum())
    resultats = df[mask].head(8)

    if nb > 0:
        rows_s = "".join(
            (
                f"<div style='display:grid;grid-template-columns:1.4fr 1fr 0.5fr 1.3fr 0.8fr;"
                f"padding:10px 0;border-bottom:1px solid {t['bordure']};align-items:center;gap:8px'>"
                f"<div style='font-size:12px;font-weight:600;color:{t['txt1']}'>"
                f'<i class="fa-solid fa-location-dot" style="color:{t["txt3"]};margin-right:5px;font-size:10px"></i>'
                f"{row['region']}</div>"
                f"<div style='font-size:12px;color:{t['txt2']}'>{row['type_carte']}</div>"
                f"<div style='font-size:12px;color:{t['txt2']}'>{row['genre']}</div>"
                f"<div style='font-size:12px;font-weight:700;color:{t['txt1']}'>{row['montant_transaction']:,.0f} <span style='font-size:10px;color:{t['txt3']}'>FCFA</span></div>"
                + (
                    f"<span class='badge badge-d'>{L['fraude_lbl']}</span>"
                    if row['fraude'] == 1
                    else f"<span class='badge badge-s'>{L['legitime']}</span>"
                )
                + "</div>"
            )
            for _, row in resultats.iterrows()
        )
        hdr_s = "".join(
            f"<div style='font-size:10px;font-weight:700;color:{t['txt3']};"
            f"text-transform:uppercase;letter-spacing:0.8px'>{col}</div>"
            for col in [L['col_region'], L['col_carte'], L['col_genre'],
                        L['col_montant'], L['col_fraude']]
        )
        plus_html = (
            f"<div style='font-size:11px;color:{t['txt3']};text-align:center;"
            f"padding-top:10px;font-style:italic'>... {nb - 8} {L['res_autres']}</div>"
        ) if nb > 8 else ""

        st.markdown(f"""
        <div class='card card-primary' style='margin-bottom:20px'>
            <div style='display:flex;align-items:center;justify-content:space-between;margin-bottom:14px'>
                <div style='display:flex;align-items:center;gap:8px'>
                    <i class="fa-solid fa-magnifying-glass" style="color:{t['primaire']};font-size:12px"></i>
                    <span style='font-size:14px;font-weight:700;color:{t['txt1']}'>{L['res_titre']}</span>
                    <span style='font-size:11px;background:{t['prim_a']};color:{t['primaire']};
                                 padding:2px 10px;border-radius:20px;font-weight:700'>{nb}</span>
                </div>
                <span style='font-size:11px;color:{t['txt3']};font-style:italic'>"{requete}"</span>
            </div>
            <div style='display:grid;grid-template-columns:1.4fr 1fr 0.5fr 1.3fr 0.8fr;
                        padding:8px 0;border-bottom:2px solid {t['bordure']};gap:8px'>
                {hdr_s}
            </div>
            {rows_s}
            {plus_html}
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style='background:{t['bgsub']};border:1px solid {t['bordure']};border-radius:10px;
                    padding:14px 20px;margin-bottom:20px;display:flex;align-items:center;gap:10px'>
            <i class="fa-solid fa-circle-xmark" style="color:{t['txt3']};font-size:14px"></i>
            <span style='font-size:13px;color:{t['txt2']}'>{L['res_aucun']}
                <b style='color:{t['txt1']}'> "{requete}"</b>
            </span>
        </div>""", unsafe_allow_html=True)
else:
    st.markdown("<div style='margin-bottom:8px'></div>", unsafe_allow_html=True)

# ── KPIs ─────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4, gap="medium")

with c1:
    st.markdown(f"""
    <div class='card card-primary'>
        <div style='display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:14px'>
            <div class='icon-box' style='background:{t['prim_a']}'>
                <i class="fa-solid fa-arrow-trend-up" style="color:{t['primaire']};font-size:15px"></i>
            </div>
            <span class='badge badge-s'>+12%</span>
        </div>
        <div class='kpi-label'>{L['total_tx']}</div>
        <div class='kpi-value'>{len(df):,}</div>
        <div class='kpi-sub'>{L['total_sub']}</div>
    </div>""", unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class='card card-danger'>
        <div style='display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:14px'>
            <div class='icon-box' style='background:{t['rouge_a']}'>
                <i class="fa-solid fa-triangle-exclamation" style="color:{t['rouge']};font-size:15px"></i>
            </div>
            <span class='badge badge-d'>+0.5%</span>
        </div>
        <div class='kpi-label'>{L['taux']}</div>
        <div class='kpi-value' style='color:{t['rouge']}'>{stats['taux_fraude']}%</div>
        <div class='kpi-sub'>{L['taux_sub']}</div>
    </div>""", unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class='card card-warning'>
        <div style='display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:14px'>
            <div class='icon-box' style='background:{t['orange_a']}'>
                <i class="fa-solid fa-bell" style="color:{t['orange']};font-size:15px"></i>
            </div>
            <span class='badge badge-w'>Actif</span>
        </div>
        <div class='kpi-label'>{L['cas']}</div>
        <div class='kpi-value'>{stats['nb_fraudes']:,}</div>
        <div class='kpi-sub'>{L['cas_sub']}</div>
    </div>""", unsafe_allow_html=True)

with c4:
    risk_pct   = min(99, int(stats['taux_fraude'] * 12))
    risk_label = "Critique" if risk_pct > 70 else "Modéré" if risk_pct > 40 else "Faible"
    risk_color = t['rouge'] if risk_pct > 70 else t['orange'] if risk_pct > 40 else t['vert']
    st.markdown(f"""
    <div class='card card-success'>
        <div style='display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:14px'>
            <div class='icon-box' style='background:{t['vert_a']}'>
                <i class="fa-solid fa-shield-halved" style="color:{t['vert']};font-size:15px"></i>
            </div>
        </div>
        <div class='kpi-label'>{L['risque']}</div>
        <div class='kpi-value' style='color:{risk_color}'>{risk_label}</div>
        <div style='margin-top:10px;background:{t['bordure']};border-radius:4px;height:6px;overflow:hidden'>
            <div style='width:{risk_pct}%;height:100%;
                        background:linear-gradient(90deg,{t['vert']},{t['orange']},{t['rouge']});
                        border-radius:4px'></div>
        </div>
        <div style='font-size:11px;color:{t['txt3']};margin-top:4px;text-align:right'>{risk_pct}%</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Graphique vélocité + Alertes par région ──────────────────
col_chart, col_region = st.columns([2.2, 1], gap="medium")

with col_chart:
    with st.container(border=True):
        hd_l, hd_r = st.columns([2.5, 1.5])

        with hd_l:
            st.markdown(f"""
            <div style='font-size:15px;font-weight:700;color:{t["txt1"]};
                        display:flex;align-items:center;gap:8px;padding-top:4px'>
                <i class="fa-solid fa-chart-line" style="color:{t["primaire"]};font-size:13px"></i>
                {L['vel_titre']}
            </div>
            <div style='font-size:12px;color:{t["txt2"]};margin-top:2px;margin-left:21px;margin-bottom:4px'>
                {L['vel_sub']}
            </div>""", unsafe_allow_html=True)

        with hd_r:
            periode = st.radio("", ["24h", "7j", "30j"], horizontal=True,
                               label_visibility="collapsed", key="periode_vel")

        rng    = np.random.default_rng(42)
        fill_c = "rgba(59,130,246,0.12)" if sombre else "rgba(99,102,241,0.08)"

        if periode == "24h":
            x_d     = np.linspace(0, 24, 288)
            y_d     = np.maximum(
                3200
                + 5800 * np.exp(-((x_d - 8.5) ** 2) / 22)
                + 2400 * np.exp(-((x_d - 21.5) ** 2) / 10)
                + rng.normal(0, 180, 288),
                200,
            )
            ai      = int(12 / 24 * 288)
            y_d[ai:ai + 8] *= 1.35
            tv      = [0, 4, 8, 12, 16, 20, 24]
            tt      = [f"{v:02d}:00" for v in tv]
            ax0, ax1 = x_d[ai - 3], x_d[ai + 11]
            vline_x = 12.0
            ann     = L['ano24']
        elif periode == "7j":
            x_d     = list(range(7))
            y_d     = np.array([48200, 53400, 61800, 93500, 55600, 37800, 29400], dtype=float)
            y_d    += rng.normal(0, 1500, 7)
            tv      = list(range(7))
            tt      = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]
            ax0, ax1 = 2.6, 3.4
            vline_x = 3.0
            ann     = L['ano7j']
        else:
            x_d     = list(range(30))
            trend   = np.linspace(42000, 60000, 30)
            y_d     = trend + rng.normal(0, 4000, 30)
            y_d[12] *= 1.65
            tv      = [0, 7, 14, 21, 29]
            tt      = ["J1", "J7", "J14", "J21", "J30"]
            ax0, ax1 = 11.5, 12.5
            vline_x = 12.0
            ann     = L['ano30']

        fig_v = go.Figure(go.Scatter(
            x=x_d, y=y_d, mode="lines", fill="tozeroy",
            fillcolor=fill_c,
            line=dict(color=t['primaire'], width=3, shape="spline"),
            hovertemplate="%{y:,.0f} transactions<extra></extra>",
        ))
        fig_v.add_vrect(x0=ax0, x1=ax1, fillcolor="rgba(239,68,68,0.08)", line_width=0)
        fig_v.add_vline(x=vline_x, line_dash="dash", line_color=t['rouge'], line_width=1.5)
        fig_v.add_annotation(
            x=vline_x, y=1.0, xref="x", yref="paper",
            text=ann, showarrow=False, yanchor="bottom",
            font=dict(color="white", size=10, family="Inter"),
            bgcolor=t['rouge'], borderwidth=0, borderpad=6,
        )
        fig_v.update_layout(
            height=300,
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color=t['pfont'], family="Inter"),
            margin=dict(l=0, r=0, t=36, b=0),
            showlegend=False,
            xaxis=dict(showgrid=False, zeroline=False,
                       tickvals=tv, ticktext=tt,
                       tickfont=dict(size=10, color=t['txt3'])),
            yaxis=dict(showgrid=True, gridcolor=t['pgrid'], zeroline=False,
                       tickfont=dict(size=10, color=t['txt3'])),
        )
        st.plotly_chart(fig_v, use_container_width=True, config={"displayModeBar": False})

with col_region:
    fraudes_r  = df_fraude.groupby("region").size().sort_values(ascending=False)
    couleurs_r = [t['rouge'], t['orange'], t['vert'], t['primaire']]
    region_rows = ""
    for i, (reg, cnt) in enumerate(fraudes_r.items()):
        c_r = couleurs_r[i % len(couleurs_r)]
        region_rows += (
            f"<div style='display:flex;align-items:center;gap:12px;padding:10px;margin-bottom:6px;"
            f"background:{t['bgsub']};border-radius:8px;border:1px solid {t['bordure']}'>"
            f"<div style='width:30px;height:30px;background:{c_r}22;border-radius:7px;"
            f"display:flex;align-items:center;justify-content:center'>"
            f'<i class="fa-solid fa-location-dot" style="color:{c_r};font-size:13px"></i>'
            f"</div><div style='flex:1'>"
            f"<div style='font-size:13px;font-weight:600;color:{t['txt1']}'>{reg}</div>"
            f"<div style='font-size:11px;color:{t['txt2']}'>{cnt:,} {L['incidents']}</div>"
            f"</div><div style='width:8px;height:8px;border-radius:50%;background:{c_r}'></div>"
            f"</div>"
        )

    st.markdown(f"""
    <div class='card' style='padding-bottom:12px'>
        <div class='section-title'>
            <i class="fa-solid fa-map-location-dot" style="margin-right:6px;color:{t['primaire']}"></i>
            {L['regions']}
        </div>
        {region_rows}
    </div>""", unsafe_allow_html=True)

    lbl_map = L['masquer'] if st.session_state.show_map else L['planisphere']
    if st.button(lbl_map, use_container_width=True, key="btn_planisphere"):
        st.session_state.show_map = not st.session_state.show_map
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# ── Planisphère (conditionnel) ────────────────────────────────
if st.session_state.show_map:
    with st.container(border=True):
        st.markdown(f"""
        <div style='display:flex;align-items:center;gap:8px;margin-bottom:16px'>
            <i class="fa-solid fa-earth-africa" style="color:{t['primaire']};font-size:15px"></i>
            <div>
                <div style='font-size:15px;font-weight:700;color:{t['txt1']}'>Planisphère des Fraudes</div>
                <div style='font-size:11px;color:{t['txt2']};margin-top:2px'>Distribution régionale du volume d'incidents détectés</div>
            </div>
        </div>""", unsafe_allow_html=True)

        fraudes_r_all = df_fraude.groupby("region").agg(
            incidents=("fraude", "count"),
            montant=("montant_transaction", "sum"),
        ).sort_values("incidents", ascending=True).reset_index()

        bar_colors = [
            t['rouge'] if v == fraudes_r_all["incidents"].max() else
            t['orange'] if v >= fraudes_r_all["incidents"].quantile(0.66) else
            t['primaire']
            for v in fraudes_r_all["incidents"]
        ]

        fig_geo = go.Figure()
        fig_geo.add_trace(go.Bar(
            x=fraudes_r_all["incidents"], y=fraudes_r_all["region"],
            orientation="h", marker_color=bar_colors, marker_line_width=0,
            text=[f"{v:,} incidents" for v in fraudes_r_all["incidents"]],
            textposition="outside",
            textfont=dict(size=11, color=t['txt2'], family="Inter"),
            hovertemplate="%{y}: <b>%{x:,}</b> incidents<extra></extra>",
        ))
        fig_geo.add_trace(go.Bar(
            x=fraudes_r_all["montant"] / 1e6,
            y=fraudes_r_all["region"],
            orientation="h",
            marker_color=[
                f"rgba({int(c[1:3],16)},{int(c[3:5],16)},{int(c[5:7],16)},0.33)"
                for c in bar_colors
            ],
            marker_line_width=0,
            name="Montant (M FCFA)",
            visible=False,
        ))
        fig_geo.update_layout(
            height=max(260, len(fraudes_r_all) * 52),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color=t['pfont'], family="Inter"),
            margin=dict(l=10, r=80, t=0, b=20),
            showlegend=False,
            xaxis=dict(showgrid=True, gridcolor=t['pgrid'], zeroline=False,
                       tickfont=dict(size=10, color=t['txt3'])),
            yaxis=dict(showgrid=False, tickfont=dict(size=12, color=t['txt1'])),
        )

        map_c1, map_c2, map_c3 = st.columns(3, gap="medium")
        max_reg = fraudes_r_all.loc[fraudes_r_all["incidents"].idxmax(), "region"]
        max_inc = fraudes_r_all["incidents"].max()
        total_m = fraudes_r_all["montant"].sum() / 1e6
        with map_c1:
            st.markdown(f"""
            <div style='background:{t['rouge_a']};border:1px solid {t['rouge']}44;border-radius:10px;padding:14px'>
                <div style='font-size:10px;font-weight:700;color:{t['rouge']};text-transform:uppercase;letter-spacing:1px'>Zone Critique</div>
                <div style='font-size:20px;font-weight:800;color:{t['txt1']};margin:6px 0 2px'>{max_reg}</div>
                <div style='font-size:12px;color:{t['txt2']}'>{max_inc:,} incidents détectés</div>
            </div>""", unsafe_allow_html=True)
        with map_c2:
            st.markdown(f"""
            <div style='background:{t['prim_a']};border:1px solid {t['primaire']}44;border-radius:10px;padding:14px'>
                <div style='font-size:10px;font-weight:700;color:{t['primaire']};text-transform:uppercase;letter-spacing:1px'>Régions Surveillées</div>
                <div style='font-size:20px;font-weight:800;color:{t['txt1']};margin:6px 0 2px'>{len(fraudes_r_all)}</div>
                <div style='font-size:12px;color:{t['txt2']}'>zones géographiques actives</div>
            </div>""", unsafe_allow_html=True)
        with map_c3:
            st.markdown(f"""
            <div style='background:{t['orange_a']};border:1px solid {t['orange']}44;border-radius:10px;padding:14px'>
                <div style='font-size:10px;font-weight:700;color:{t['orange']};text-transform:uppercase;letter-spacing:1px'>Exposition Financière</div>
                <div style='font-size:20px;font-weight:800;color:{t['txt1']};margin:6px 0 2px'>{total_m:,.1f}M</div>
                <div style='font-size:12px;color:{t['txt2']}'>FCFA de transactions frauduleuses</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.plotly_chart(fig_geo, use_container_width=True, config={"displayModeBar": False})

    st.markdown("<br>", unsafe_allow_html=True)

# ── Alertes Critiques Récentes ────────────────────────────────
types_a    = ["Dépôt Inhabituel", "Vitesse IP", "Carte Blacklistée", "Connexion Suspecte", "Transfert Anormal"]
icones_a   = ["fa-money-bill-wave", "fa-bolt", "fa-credit-card", "fa-user-secret", "fa-right-left"]
couleurs_a = [t['orange'], t['rouge'], t['rouge'], t['primaire'], t['orange']]
sample_f   = df_fraude.sample(min(5, len(df_fraude)), random_state=42)

entetes = ["ENTITÉ / UTILISATEUR", "TYPE D'ALERTE", "SCORE DE RISQUE", "VALEUR", "DATE & HEURE", "ACTION"]
header_html = "".join(
    f"<div style='font-size:10px;font-weight:700;color:{t['txt3']};letter-spacing:0.8px;text-transform:uppercase'>{h}</div>"
    for h in entetes
)

rows_html = ""
for i, (idx, row) in enumerate(sample_f.iterrows()):
    score   = min(99, int(70 + (row['montant_transaction'] / df['montant_transaction'].max()) * 28))
    a_type  = types_a[i % len(types_a)]
    a_icon  = icones_a[i % len(icones_a)]
    a_color = couleurs_a[i % len(couleurs_a)]
    initials = f"{row['genre'][0].upper()}{i + 1}"
    score_c  = t['rouge'] if score > 80 else t['orange']
    rows_html += (
        f"<div style='display:grid;grid-template-columns:2fr 1.5fr 1.5fr 1.2fr 1.2fr 0.8fr;"
        f"padding:12px 0;border-bottom:1px solid {t['bordure']};align-items:center'>"
        f"<div style='display:flex;align-items:center;gap:10px'>"
        f"<div style='width:32px;height:32px;border-radius:50%;background:{t['prim_a']};"
        f"display:flex;align-items:center;justify-content:center;"
        f"font-size:11px;font-weight:700;color:{t['primaire']}'>{initials}</div>"
        f"<div><div style='font-size:13px;font-weight:600;color:{t['txt1']}'>Client {idx}</div>"
        f"<div style='font-size:11px;color:{t['txt3']}'>ID: {str(idx).zfill(4)}-{row['type_carte'][:2].upper()}</div>"
        f"</div></div>"
        f"<div><span style='background:{a_color}22;color:{a_color};border:1px solid {a_color}44;"
        f"padding:3px 8px;border-radius:6px;font-size:11px;font-weight:600;"
        f"display:inline-flex;align-items:center;gap:4px'>"
        f'<i class="fa-solid {a_icon}" style="font-size:10px"></i> {a_type}'
        f"</span></div>"
        f"<div style='display:flex;align-items:center;gap:8px'>"
        f"<div style='flex:1;height:4px;background:{t['bordure']};border-radius:2px'>"
        f"<div style='width:{score}%;height:100%;background:{score_c};border-radius:2px'></div>"
        f"</div><span style='font-size:13px;font-weight:700;color:{score_c}'>{score}</span></div>"
        f"<div style='font-size:13px;color:{t['txt1']};font-weight:500'>{row['montant_transaction']:,.0f} FCFA</div>"
        f"<div style='font-size:12px;color:{t['txt2']}'>"
        f'<i class="fa-regular fa-clock" style="margin-right:4px;font-size:11px"></i>'
        f" Aujourd'hui, 14:{20 + i:02d}</div>"
        f"<div><span style='background:{t['primaire']};color:white;padding:5px 12px;"
        f"border-radius:7px;font-size:11px;font-weight:600;cursor:pointer'>{L['enqueter']}</span></div>"
        f"</div>"
    )

with st.container(border=True):
    # ── En-tête avec bouton téléchargement ──────────────────────
    hd_l, hd_r = st.columns([5, 1])
    with hd_l:
        st.markdown(f"""
        <div style='font-size:15px;font-weight:700;color:{t["txt1"]};
                    display:flex;align-items:center;gap:8px;margin-bottom:16px'>
            <i class="fa-solid fa-circle-exclamation" style="color:{t["rouge"]};font-size:13px"></i>
            {L['alertes']}
        </div>""", unsafe_allow_html=True)
    with hd_r:
        csv_export = df_fraude[["age", "salaire", "score_credit", "montant_transaction",
                                "anciennete_compte", "type_carte", "region", "genre", "fraude"]
                               ].to_csv(index=False).encode("utf-8")
        st.download_button(
            label=L['export'],
            data=csv_export,
            file_name="alertes_fraudes.csv",
            mime="text/csv",
            key="dl_fraudes",
            use_container_width=True,
        )

    # ── Tableau ─────────────────────────────────────────────────
    st.markdown(f"""
    <div style='border-top:1px solid {t["bordure"]};padding-top:4px'>
        <div style='display:grid;grid-template-columns:2fr 1.5fr 1.5fr 1.2fr 1.2fr 0.8fr;
                    padding:8px 0;border-bottom:2px solid {t["bordure"]}'>
            {header_html}
        </div>
        {rows_html}
    </div>""", unsafe_allow_html=True)

    # ── Lien "Voir toutes" ───────────────────────────────────────
    st.markdown("<div style='margin-top:8px'>", unsafe_allow_html=True)
    st.page_link(
        "pages/1_exploration.py",
        label=f"{L['voir']} ({stats['nb_fraudes']:,})  →",
        icon=":material/open_in_new:",
    )
    st.markdown("</div>", unsafe_allow_html=True)
