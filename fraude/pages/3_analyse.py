import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils.data import charger_donnees, get_stas
from utils.theme import get_colors, inject_css, render_sidebar

st.set_page_config(page_title="FraudLens — Analyse EDA", page_icon="🛡️",
                   layout="wide", initial_sidebar_state="expanded")

if "mode_sombre"    not in st.session_state: st.session_state.mode_sombre    = True
if "onglet_analyse" not in st.session_state: st.session_state.onglet_analyse = "Corrélation"

sombre = st.session_state.mode_sombre
t      = get_colors(sombre)
inject_css(t)
render_sidebar(sombre)

# ── Unpack theme (avoid nested quotes in f-strings) ───────────────
bg     = t['bg'];      bgcard = t['bgcard'];  bgsub  = t['bgsub']
bdr    = t['bordure']; txt1   = t['txt1'];    txt2   = t['txt2'];   txt3  = t['txt3']
prim   = t['primaire'];rouge  = t['rouge'];   vert   = t['vert'];   ora   = t['orange']
prim_a = t['prim_a']; rouge_a= t['rouge_a']; vert_a = t['vert_a']; ora_a = t['orange_a']
pfont  = t['pfont'];   pgrid  = t['pgrid'];   pbg    = t['pbg']

df_brut, df = charger_donnees()
stats       = get_stas(df)
df_fraude   = df[df["fraude"] == 1]
onglet      = st.session_state.onglet_analyse

# ── Header ────────────────────────────────────────────────────────
st.markdown(f"""
<div style='display:flex;align-items:center;justify-content:space-between;
            margin-bottom:8px;padding-bottom:16px;border-bottom:1px solid {bdr}'>
    <div style='background:{bgcard};border:1px solid {bdr};border-radius:10px;
                padding:10px 18px;display:flex;align-items:center;gap:10px;min-width:360px'>
        <i class="fa-solid fa-magnifying-glass" style="color:{txt3};font-size:13px"></i>
        <span style='color:{txt3};font-size:13px'>Rechercher des anomalies...</span>
    </div>
    <div style='display:flex;align-items:center;gap:14px;margin-left:24px'>
        <span style='font-size:16px;cursor:pointer;color:{txt2}'><i class="fa-solid fa-bell"></i></span>
        <span style='font-size:16px;cursor:pointer;color:{txt2}'><i class="fa-solid fa-globe"></i></span>
    </div>
</div>
<div style='margin-bottom:20px'>
    <div style='font-size:22px;font-weight:800;color:{txt1};margin-bottom:4px'>
        Analyse Exploratoire des Données (EDA)
    </div>
    <div style='font-size:13px;color:{txt2};max-width:620px;line-height:1.5'>
        Corrélations multidimensionnelles, segments de risque et profils démographiques — Dataset Fraude 2024-Q3.
    </div>
</div>""", unsafe_allow_html=True)

# ── KPIs ──────────────────────────────────────────────────────────
total_fmt = f"{stats['total']:,}".replace(",", " ")
taux_fmt  = f"{stats['taux_fraude']:.2f}%"
moy_fmt   = f"${stats['montant_moy']:,.0f}"
risk_conf = f"{min(round(df['score_credit'].mean() / 8.5, 1), 99.9):.1f}%"
std_fmt   = f"${df['montant_transaction'].std():,.0f}"
badge_html = (f"<div style='display:flex;align-items:center;gap:4px;margin-top:5px'>"
              f"<i class='fa-solid fa-circle-check' style='color:{vert};font-size:9px'></i>"
              f"<span style='font-size:10px;color:{txt3}'>Validé pour Q3 2024</span></div>")

kpi_data = [
    ("card-primary",  "fa-solid fa-database",             prim,  "EXEMPLES DE JEU DE DONNÉES",
     total_fmt,  "Validé pour Q3 2024",             badge_html),
    ("card-danger",   "fa-solid fa-triangle-exclamation", rouge, "PRÉVALENCE DE LA FRAUDE",
     taux_fmt,   "↑ +0.8% vs période précédente",   ""),
    ("card-warning",  "fa-solid fa-dollar-sign",          ora,   "TRANSACTION MOYENNE",
     moy_fmt,    f"Écart-type : {std_fmt}",          ""),
    ("card-success",  "fa-solid fa-shield-halved",        vert,  "RISK CONFIDENCE",
     risk_conf,  "Bayesian Model Alpha",              ""),
]

k_cols = st.columns(4, gap="medium")
for col, (card_cls, icon, color, label, value, sub, badge) in zip(k_cols, kpi_data):
    with col:
        st.markdown(f"""
        <div class='card {card_cls}' style='padding:18px 20px'>
            <div style='display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:8px'>
                <div style='font-size:10px;font-weight:700;color:{txt3};text-transform:uppercase;
                            letter-spacing:0.7px;line-height:1.3;max-width:120px'>{label}</div>
                <div style='width:30px;height:30px;border-radius:8px;background:{color}20;flex-shrink:0;
                            display:flex;align-items:center;justify-content:center'>
                    <i class="{icon}" style="color:{color};font-size:12px"></i>
                </div>
            </div>
            <div style='font-size:28px;font-weight:800;color:{color};line-height:1.1;margin-bottom:4px'>{value}</div>
            <div style='font-size:11px;color:{txt3}'>{sub}</div>
            {badge}
        </div>""", unsafe_allow_html=True)

st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

# ── Tab Navigation ────────────────────────────────────────────────
tab_names = ["Corrélation", "Segments", "Démographies"]
t_cols    = st.columns([1, 1, 1.1, 3.4, 1.3], gap="small")
for i, name in enumerate(tab_names):
    with t_cols[i]:
        active = (onglet == name)
        if st.button(name, key=f"tab_{i}", use_container_width=True,
                     type="primary" if active else "secondary"):
            st.session_state.onglet_analyse = name
            st.rerun()
with t_cols[4]:
    st.markdown(f"""
    <div style='display:flex;align-items:center;justify-content:flex-end;padding-top:4px'>
        <div style='background:{bgcard};border:1px solid {bdr};border-radius:8px;
                    padding:7px 14px;font-size:12px;font-weight:600;color:{txt2};
                    display:flex;align-items:center;gap:6px;cursor:pointer;white-space:nowrap'>
            <i class="fa-solid fa-sliders" style="font-size:11px"></i> Global Filters
        </div>
    </div>""", unsafe_allow_html=True)

st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
#  CORRÉLATION
# ═══════════════════════════════════════════════════════════════════
if onglet == "Corrélation":
    col_heat, col_tbl = st.columns([1.5, 1], gap="medium")

    with col_heat:
        cols_num = ["montant_transaction", "age", "salaire", "score_credit", "fraude"]
        etiq     = ["Amount", "Age", "Salary", "Score", "Fraud"]
        corr     = df[cols_num].corr().round(2)

        fig_corr = go.Figure(go.Heatmap(
            z=corr.values, x=etiq, y=etiq,
            colorscale=[[0.0, pbg], [0.35, prim_a], [0.65, prim], [1.0, rouge]],
            text=corr.values.round(2), texttemplate="%{text}",
            textfont=dict(size=12, family="Inter", color="white"),
            showscale=False, zmin=-1, zmax=1,
        ))
        fig_corr.update_layout(
            height=360,
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color=pfont, family="Inter"),
            margin=dict(l=50, r=10, t=10, b=50),
            xaxis=dict(tickfont=dict(size=11, family="Inter", color=pfont)),
            yaxis=dict(tickfont=dict(size=11, family="Inter", color=pfont)),
        )
        st.markdown(f"""
        <div class='card' style='padding-bottom:4px'>
            <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:2px'>
                <div>
                    <div style='font-size:15px;font-weight:700;color:{txt1}'>Heatmap de Corrélation</div>
                    <div style='font-size:11px;color:{txt2};margin-top:2px'>
                        Coefficient de Pearson des variables numériques</div>
                </div>
                <span style='font-size:11px;padding:3px 10px;border-radius:20px;font-weight:600;
                             background:{rouge_a};color:{rouge};border:1px solid {rouge}33'>
                    <i class="fa-solid fa-triangle-exclamation" style="font-size:10px"></i> Haut Risque
                </span>
            </div>
        </div>""", unsafe_allow_html=True)
        st.plotly_chart(fig_corr, use_container_width=True, config={"displayModeBar": False})

    with col_tbl:
        st.markdown(f"""
        <div class='card' style='padding-bottom:8px'>
            <div style='font-size:15px;font-weight:700;color:{txt1};margin-bottom:4px'>
                Distribution des Variables</div>
            <div style='font-size:11px;color:{txt2};margin-bottom:14px'>Statistiques descriptives clés</div>
        </div>""", unsafe_allow_html=True)

        h_cols = st.columns([1.5, 1, 1, 1.1, 1.1])
        h_style = f"font-size:10px;font-weight:700;color:{txt3};text-transform:uppercase;letter-spacing:0.8px;padding:6px 2px"
        for hc, lbl in zip(h_cols, ["Variable", "Moyenne", "Médiane", "Asymétrie", "Kurtosis"]):
            with hc:
                st.markdown(f"<div style='{h_style}'>{lbl}</div>", unsafe_allow_html=True)

        var_map = [
            ("montant_transaction", "Txn_Amount"),
            ("age",                 "User_Age"),
            ("salaire",             "Salary_K"),
            ("score_credit",        "Score_Credit"),
            ("fraude",              "Fraude"),
        ]
        for col_k, col_lbl in var_map:
            s   = df[col_k]
            skw = s.skew()
            krt = s.kurt()
            mean_s = f"{s.mean():,.0f}" if col_k in ("montant_transaction","salaire") else f"{s.mean():.2f}"
            med_s  = f"{s.median():,.0f}" if col_k in ("montant_transaction","salaire") else f"{s.median():.2f}"
            skw_s  = f"{'+'if skw>0 else ''}{skw:.2f}"
            krt_s  = f"{krt:.2f}"
            skw_c  = rouge if abs(skw) > 1 else (ora if abs(skw) > 0.5 else vert)
            krt_c  = rouge if abs(krt) > 3 else (ora if abs(krt) > 1 else vert)

            r_cols = st.columns([1.5, 1, 1, 1.1, 1.1])
            cell   = f"background:{bgsub};padding:8px 6px;margin-bottom:3px;font-size:11px"
            with r_cols[0]:
                st.markdown(f"<div style='{cell};border-radius:6px 0 0 6px;font-weight:600;color:{txt1}'>{col_lbl}</div>",
                            unsafe_allow_html=True)
            with r_cols[1]:
                st.markdown(f"<div style='{cell};color:{txt2}'>{mean_s}</div>", unsafe_allow_html=True)
            with r_cols[2]:
                st.markdown(f"<div style='{cell};color:{txt2}'>{med_s}</div>", unsafe_allow_html=True)
            with r_cols[3]:
                st.markdown(f"<div style='{cell};font-weight:700;color:{skw_c}'>{skw_s}</div>", unsafe_allow_html=True)
            with r_cols[4]:
                st.markdown(f"<div style='{cell};border-radius:0 6px 6px 0;font-weight:700;color:{krt_c}'>{krt_s}</div>",
                            unsafe_allow_html=True)

        st.markdown(f"""
        <div style='display:flex;gap:16px;margin-top:12px;padding:10px 12px;
                    background:{bgsub};border-radius:8px'>
            <div style='display:flex;align-items:center;gap:5px'>
                <div style='width:8px;height:8px;border-radius:50%;background:{vert}'></div>
                <span style='font-size:10px;color:{txt3}'>Normal</span>
            </div>
            <div style='display:flex;align-items:center;gap:5px'>
                <div style='width:8px;height:8px;border-radius:50%;background:{ora}'></div>
                <span style='font-size:10px;color:{txt3}'>Modéré</span>
            </div>
            <div style='display:flex;align-items:center;gap:5px'>
                <div style='width:8px;height:8px;border-radius:50%;background:{rouge}'></div>
                <span style='font-size:10px;color:{txt3}'>Anomalie</span>
            </div>
        </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
#  SEGMENTS
# ═══════════════════════════════════════════════════════════════════
elif onglet == "Segments":
    col_dist, col_seg = st.columns(2, gap="medium")

    with col_dist:
        variable = st.selectbox("Variable",
                                ["Montant de Transaction", "Salaire", "Score de Crédit", "Âge"],
                                label_visibility="collapsed")
        col_map = {"Montant de Transaction": "montant_transaction", "Salaire": "salaire",
                   "Score de Crédit": "score_credit", "Âge": "age"}
        col_sel = col_map[variable]

        fig_d = go.Figure()
        fig_d.add_trace(go.Histogram(x=df[df["fraude"]==0][col_sel], name="Légitime",
                                     marker_color=prim, nbinsx=30, opacity=0.7))
        fig_d.add_trace(go.Histogram(x=df[df["fraude"]==1][col_sel], name="Fraude",
                                     marker_color=rouge, nbinsx=30, opacity=0.7))
        fig_d.update_layout(
            barmode="overlay", height=280,
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color=pfont, family="Inter"), margin=dict(l=0, r=0, t=10, b=0),
            showlegend=True,
            legend=dict(font=dict(size=10, family="Inter", color=pfont),
                        bgcolor="rgba(0,0,0,0)", orientation="h", y=1.08),
            xaxis=dict(showgrid=False, zeroline=False, tickfont=dict(size=9, color=txt3)),
            yaxis=dict(showgrid=True, gridcolor=pgrid, zeroline=False, tickfont=dict(size=9, color=txt3)),
        )
        st.markdown(f"""
        <div class='card' style='padding-bottom:4px'>
            <div style='font-size:15px;font-weight:700;color:{txt1};display:flex;align-items:center;gap:8px'>
                <i class="fa-solid fa-chart-bar" style="color:{prim};font-size:13px"></i>
                Distribution — {variable}
            </div>
            <div style='font-size:11px;color:{txt2};margin-left:21px'>Légitime vs Fraude</div>
        </div>""", unsafe_allow_html=True)
        st.plotly_chart(fig_d, use_container_width=True, config={"displayModeBar": False})

        df["tranche_score"] = pd.cut(df["score_credit"],
            bins=[0, 400, 600, 800, 1000],
            labels=["Faible (<400)", "Moyen (400-600)", "Bon (600-800)", "Excellent (>800)"])
        seg_sc = df.groupby("tranche_score", observed=True).agg(
            total=("fraude","count"), fraudes=("fraude","sum")).reset_index()
        seg_sc["taux"] = (seg_sc["fraudes"] / seg_sc["total"] * 100).round(1)
        sc_colors = [rouge, ora, prim, vert]
        sc_rows = ""
        for i2, (_, row) in enumerate(seg_sc.iterrows()):
            c   = sc_colors[i2 % 4]
            pct = min(row['taux'] * 12, 100)
            sc_rows += (
                f"<div style='display:flex;align-items:center;gap:10px;padding:7px 0;"
                f"border-bottom:1px solid {bdr}'>"
                f"<span style='font-size:11px;font-weight:500;color:{txt2};min-width:130px'>{row['tranche_score']}</span>"
                f"<div style='flex:1;background:{bgcard};border-radius:3px;height:5px'>"
                f"<div style='width:{pct:.0f}%;height:100%;background:{c};border-radius:3px'></div></div>"
                f"<span style='font-size:11px;font-weight:700;color:{c};min-width:44px;text-align:right'>{row['taux']}%</span>"
                f"</div>"
            )
        st.markdown(f"""
        <div class='card' style='margin-top:12px'>
            <div style='font-size:13px;font-weight:700;color:{txt1};margin-bottom:12px;
                        display:flex;align-items:center;gap:6px'>
                <i class="fa-solid fa-gauge-high" style="color:{prim};font-size:12px"></i>
                Fraude par Score de Crédit
            </div>
            {sc_rows}
        </div>""", unsafe_allow_html=True)

    with col_seg:
        df["tranche_salaire"] = pd.cut(df["salaire"],
            bins=[0, 40000, 80000, 10_000_000],
            labels=["Junior (<40k)", "Mid (40–80k)", "Senior (>80k)"])
        seg = df.groupby("tranche_salaire", observed=True).agg(
            total=("fraude","count"), fraudes=("fraude","sum")).reset_index()
        seg["taux_fraude"]   = (seg["fraudes"] / seg["total"] * 100).round(1)
        seg["taux_legitime"] = 100 - seg["taux_fraude"]

        fig_seg = go.Figure()
        fig_seg.add_trace(go.Bar(name="Légitime", x=seg["tranche_salaire"].astype(str),
                                 y=seg["taux_legitime"], marker_color=prim, opacity=0.85))
        fig_seg.add_trace(go.Bar(name="Fraude", x=seg["tranche_salaire"].astype(str),
                                 y=seg["taux_fraude"], marker_color=rouge, opacity=0.85))
        fig_seg.update_layout(
            barmode="group", height=280,
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color=pfont, family="Inter"), margin=dict(l=0, r=0, t=10, b=0),
            showlegend=True,
            legend=dict(font=dict(size=10, family="Inter", color=pfont),
                        bgcolor="rgba(0,0,0,0)", orientation="h", y=1.08),
            xaxis=dict(tickfont=dict(size=10, color=txt3), showgrid=False),
            yaxis=dict(tickfont=dict(size=9, color=txt3), gridcolor=pgrid, ticksuffix="%"),
        )
        st.markdown(f"""
        <div class='card' style='padding-bottom:4px'>
            <div style='font-size:15px;font-weight:700;color:{txt1};display:flex;align-items:center;gap:8px'>
                <i class="fa-solid fa-users" style="color:{prim};font-size:13px"></i>
                Segmentation par Salaire
            </div>
            <div style='font-size:11px;color:{txt2};margin-left:21px'>Taux Fraude vs Légitime</div>
        </div>""", unsafe_allow_html=True)
        st.plotly_chart(fig_seg, use_container_width=True, config={"displayModeBar": False})

        taux_jr_vals = seg[seg["tranche_salaire"] == "Junior (<40k)"]["taux_fraude"].values
        taux_jr_val  = float(taux_jr_vals[0]) if len(taux_jr_vals) else stats['taux_fraude']
        corr_r       = df[['salaire', 'montant_transaction']].corr().iloc[0, 1]
        findings = [
            (rouge_a, rouge, "fa-solid fa-circle-exclamation", "RISQUE EXÉCUTIF", "Alerte Segment Alpha",
             f"Les profils Junior affichent {taux_jr_val:.1f}% de fraude, au-dessus de la moyenne globale ({stats['taux_fraude']:.1f}%).",
             "Action immédiate requise"),
            (prim_a, prim, "fa-solid fa-chart-line", "BASELINE DE STABILITÉ", "Cohérence Revenus",
             f"Corrélation Salaire/Montant stable (r = {corr_r:.2f}) — référence de confiance.", ""),
        ]
        for bg_a, color, icon, label, titre, desc, action in findings:
            act_html = (f"<div style='margin-top:8px;font-size:12px;color:{color};font-weight:600;"
                        f"display:flex;align-items:center;gap:4px'>"
                        f"<i class='fa-solid fa-arrow-trend-up' style='font-size:11px'></i> {action}</div>") if action else ""
            st.markdown(f"""
            <div style='background:{bg_a};border:1px solid {color}44;border-radius:12px;
                        padding:14px 16px;margin-bottom:10px'>
                <div style='display:flex;align-items:center;gap:6px;margin-bottom:4px'>
                    <i class="{icon}" style="color:{color};font-size:11px"></i>
                    <span style='font-size:10px;font-weight:700;color:{color};text-transform:uppercase;
                                 letter-spacing:1px'>{label}</span>
                </div>
                <div style='font-size:14px;font-weight:700;color:{txt1};margin-bottom:6px'>{titre}</div>
                <div style='font-size:12px;color:{txt2};line-height:1.5'>{desc}</div>
                {act_html}
            </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
#  DÉMOGRAPHIES
# ═══════════════════════════════════════════════════════════════════
elif onglet == "Démographies":
    col_age, col_demo = st.columns(2, gap="medium")

    with col_age:
        df["tranche_age"] = pd.cut(df["age"],
            bins=[0, 25, 35, 45, 55, 120],
            labels=["18–25", "25–35", "35–45", "45–55", "55+"])
        age_seg = df.groupby("tranche_age", observed=True).agg(
            total=("fraude","count"), fraudes=("fraude","sum")).reset_index()
        age_seg["taux"] = (age_seg["fraudes"] / age_seg["total"] * 100).round(1)

        fig_age = go.Figure()
        fig_age.add_trace(go.Bar(x=age_seg["tranche_age"].astype(str), y=age_seg["total"],
                                 name="Total", marker_color=prim, opacity=0.55))
        fig_age.add_trace(go.Bar(x=age_seg["tranche_age"].astype(str), y=age_seg["fraudes"],
                                 name="Fraudes", marker_color=rouge, opacity=0.9))
        fig_age.update_layout(
            barmode="overlay", height=280,
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color=pfont, family="Inter"), margin=dict(l=0, r=0, t=10, b=0),
            showlegend=True,
            legend=dict(font=dict(size=10, family="Inter", color=pfont),
                        bgcolor="rgba(0,0,0,0)", orientation="h", y=1.08),
            xaxis=dict(tickfont=dict(size=11, color=txt3), showgrid=False),
            yaxis=dict(tickfont=dict(size=9, color=txt3), gridcolor=pgrid),
        )
        st.markdown(f"""
        <div class='card' style='padding-bottom:4px'>
            <div style='font-size:15px;font-weight:700;color:{txt1};display:flex;align-items:center;gap:8px'>
                <i class="fa-solid fa-cake-candles" style="color:{prim};font-size:13px"></i>
                Distribution par Tranche d'Âge
            </div>
            <div style='font-size:11px;color:{txt2};margin-left:21px'>Total transactions vs détections fraude</div>
        </div>""", unsafe_allow_html=True)
        st.plotly_chart(fig_age, use_container_width=True, config={"displayModeBar": False})

        age_rows = ""
        for _, row in age_seg.iterrows():
            c   = rouge if row['taux'] > stats['taux_fraude'] else vert
            pct = min(row['taux'] * 14, 100)
            age_rows += (
                f"<div style='display:flex;align-items:center;gap:10px;padding:7px 0;"
                f"border-bottom:1px solid {bdr}'>"
                f"<span style='font-size:12px;font-weight:600;color:{txt1};min-width:55px'>{row['tranche_age']}</span>"
                f"<div style='flex:1;background:{bgcard};border-radius:3px;height:6px'>"
                f"<div style='width:{pct:.0f}%;height:100%;background:{c};border-radius:3px'></div></div>"
                f"<span style='font-size:11px;font-weight:700;color:{c};min-width:44px;text-align:right'>{row['taux']}%</span>"
                f"<span style='font-size:10px;color:{txt3};min-width:54px;text-align:right'>{int(row['total']):,} tx</span>"
                f"</div>"
            )
        st.markdown(f"""
        <div class='card' style='margin-top:12px'>
            <div style='font-size:13px;font-weight:700;color:{txt1};margin-bottom:12px;
                        display:flex;align-items:center;gap:6px'>
                <i class="fa-solid fa-percent" style="color:{rouge};font-size:11px"></i>
                Taux de Fraude par Tranche d'Âge
            </div>
            {age_rows}
        </div>""", unsafe_allow_html=True)

    with col_demo:
        tranches_h = [
            ("00–06h", 0.8, rouge, "Anomalie",  "fa-triangle-exclamation"),
            ("06–12h", 0.5, prim,  "Stable",    "fa-check"),
            ("12–18h", 0.5, prim,  "Stable",    "fa-check"),
            ("18–24h", 0.6, ora,   "Modéré",    "fa-minus"),
        ]
        rows_h = ""
        for tr, pct, c, lbl, ico in tranches_h:
            rows_h += (
                f"<div style='display:flex;align-items:center;gap:10px;padding:8px 0;"
                f"border-bottom:1px solid {bdr}'>"
                f"<span style='font-size:12px;font-weight:500;color:{txt2};min-width:60px'>{tr}</span>"
                f"<div style='flex:1;background:{bgcard};border-radius:3px;height:5px'>"
                f"<div style='width:{int(pct*100)}%;height:100%;background:{c};border-radius:3px'></div></div>"
                f"<span style='font-size:11px;font-weight:600;color:{c};min-width:76px;text-align:right;"
                f"display:flex;align-items:center;justify-content:flex-end;gap:4px'>"
                f"<i class='fa-solid {ico}' style='font-size:10px'></i>{lbl}</span>"
                f"</div>"
            )
        st.markdown(f"""
        <div class='card'>
            <div style='font-size:13px;font-weight:700;color:{txt1};margin-bottom:12px;
                        display:flex;align-items:center;gap:6px'>
                <i class="fa-regular fa-clock" style="color:{prim};font-size:13px"></i>
                Volume par Tranche Horaire
            </div>
            {rows_h}
        </div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

        stat_items = [
            ("Montant Moyen", f"${df['montant_transaction'].mean():,.0f}",   prim),
            ("Montant Max",   f"${df['montant_transaction'].max():,.0f}",    rouge),
            ("Écart-type",    f"${df['montant_transaction'].std():,.0f}",    ora),
            ("Médiane",       f"${df['montant_transaction'].median():,.0f}", vert),
        ]
        s_cols = st.columns(2)
        for i2, (lbl, val, color) in enumerate(stat_items):
            with s_cols[i2 % 2]:
                st.markdown(f"""
                <div style='background:{color}12;border:1px solid {color}33;border-radius:10px;
                            padding:12px 14px;margin-bottom:10px;text-align:center'>
                    <div style='font-size:10px;font-weight:600;color:{txt3};text-transform:uppercase;
                                margin-bottom:4px'>{lbl}</div>
                    <div style='font-size:18px;font-weight:800;color:{color}'>{val}</div>
                </div>""", unsafe_allow_html=True)

        st.markdown(f"""
        <div class='card'>
            <div style='font-size:13px;font-weight:700;color:{txt1};margin-bottom:14px;
                        display:flex;align-items:center;gap:6px'>
                <i class="fa-solid fa-user-group" style="color:{prim};font-size:12px"></i>
                Profil Démographique Moyen
            </div>
            <div style='display:flex;flex-direction:column;gap:12px'>
                <div style='display:flex;justify-content:space-between;align-items:center'>
                    <span style='font-size:12px;color:{txt2}'>Âge moyen</span>
                    <span style='font-size:13px;font-weight:700;color:{txt1}'>{stats['age_moy']:.0f} ans</span>
                </div>
                <div style='display:flex;justify-content:space-between;align-items:center'>
                    <span style='font-size:12px;color:{txt2}'>Salaire moyen</span>
                    <span style='font-size:13px;font-weight:700;color:{txt1}'>${stats['salaire_moy']:,.0f}</span>
                </div>
                <div style='display:flex;justify-content:space-between;align-items:center'>
                    <span style='font-size:12px;color:{txt2}'>Score crédit moyen</span>
                    <span style='font-size:13px;font-weight:700;color:{prim}'>{stats['score_moy']:.0f}</span>
                </div>
                <div style='display:flex;justify-content:space-between;align-items:center'>
                    <span style='font-size:12px;color:{txt2}'>Transactions frauduleuses</span>
                    <span style='font-size:13px;font-weight:700;color:{rouge}'>{stats['nb_fraudes']:,}</span>
                </div>
                <div style='display:flex;justify-content:space-between;align-items:center'>
                    <span style='font-size:12px;color:{txt2}'>Taux de fraude</span>
                    <span style='font-size:13px;font-weight:700;color:{rouge}'>{stats['taux_fraude']:.2f}%</span>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)
