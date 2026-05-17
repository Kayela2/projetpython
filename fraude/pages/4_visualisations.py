import streamlit as st
import numpy as np
import plotly.graph_objects as go
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils.data import charger_donnees, get_stas
from utils.theme import get_colors, inject_css, render_sidebar

st.set_page_config(page_title="FraudLens — Visualisations", page_icon="🛡️",
                   layout="wide", initial_sidebar_state="expanded")

if "mode_sombre"      not in st.session_state: st.session_state.mode_sombre      = True
if "onglet_visu"      not in st.session_state: st.session_state.onglet_visu      = "Vue Globale"

sombre = st.session_state.mode_sombre
t = get_colors(sombre)
inject_css(t)
render_sidebar(sombre)

df_brut, df = charger_donnees()
stats     = get_stas(df)
df_fraude = df[df["fraude"] == 1]

# Pre-extract theme vars
bg     = t['bg'];      bgcard = t['bgcard'];  bgsub  = t['bgsub']
bdr    = t['bordure']; txt1   = t['txt1'];    txt2   = t['txt2'];  txt3 = t['txt3']
prim   = t['primaire'];rouge  = t['rouge'];   vert   = t['vert'];  ora  = t['orange']
prim_a = t['prim_a']; rouge_a= t['rouge_a']; vert_a = t['vert_a']; ora_a = t['orange_a']
pfont  = t['pfont'];   pgrid  = t['pgrid']

df_leg  = df[df["fraude"] == 0]
df_frau = df[df["fraude"] == 1]
onglet  = st.session_state.onglet_visu

# ── En-tête ───────────────────────────────────────────────────
st.markdown(f"""
<div style='display:flex;align-items:center;justify-content:space-between;
            margin-bottom:20px;padding-bottom:16px;border-bottom:1px solid {bdr}'>
    <div style='background:{bgcard};border:1px solid {bdr};border-radius:10px;
                padding:10px 18px;display:flex;align-items:center;gap:10px;min-width:360px'>
        <i class="fa-solid fa-magnifying-glass" style="color:{txt3};font-size:13px"></i>
        <span style='color:{txt3};font-size:13px'>Rechercher des patterns...</span>
    </div>
    <div style='display:flex;align-items:center;gap:14px;margin-left:24px'>
        <span style='font-size:16px;cursor:pointer;color:{txt2}'><i class="fa-solid fa-bell"></i></span>
        <span style='font-size:16px;cursor:pointer;color:{txt2}'><i class="fa-solid fa-globe"></i></span>
    </div>
</div>
<div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:16px'>
    <div>
        <div style='font-size:16px;font-weight:700;color:{txt1}'>Visualisations Interactives Premium</div>
        <div style='font-size:12px;color:{txt2};margin-top:2px'>Exploration forensique des anomalies de transaction à haute résolution.</div>
    </div>
    <div style='display:flex;gap:8px'>
        <span style='background:{bgsub};border:1px solid {bdr};padding:8px 16px;border-radius:8px;
                     font-size:12px;color:{txt2};cursor:pointer;display:flex;align-items:center;gap:6px'>
            <i class="fa-regular fa-calendar-days" style="font-size:11px"></i> Derniers 30 Jours
        </span>
        <span style='background:{prim};color:white;padding:8px 16px;border-radius:8px;
                     font-size:12px;font-weight:600;cursor:pointer;display:flex;align-items:center;gap:6px'>
            <i class="fa-solid fa-arrow-up-right-from-square" style="font-size:11px"></i> Exporter Rapport
        </span>
    </div>
</div>""", unsafe_allow_html=True)

# ── Navigation onglets ─────────────────────────────────────────
tab_names = ["Vue Globale", "Démographies", "Distributions"]
t_cols    = st.columns([1, 1, 1.2, 3.8], gap="small")
for i, name in enumerate(tab_names):
    with t_cols[i]:
        active = (onglet == name)
        if st.button(name, key=f"vtab_{i}", use_container_width=True,
                     type="primary" if active else "secondary"):
            st.session_state.onglet_visu = name
            st.rerun()

st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# Onglet 1 — Vue Globale
# ══════════════════════════════════════════════════════════════
if onglet == "Vue Globale":
    col_pulse, col_gauge = st.columns([2, 1], gap="medium")

    with col_pulse:
        rng    = np.random.default_rng(2024)
        heures = [f"{h:02d}:00" for h in range(0, 24, 2)]
        reel   = np.abs(rng.normal(60, 20, 12)).clip(10, 100).round(0)
        predit = np.abs(reel + rng.normal(0, 10, 12)).clip(10, 100).round(0)

        fig_pulse = go.Figure()
        fig_pulse.add_trace(go.Bar(x=heures, y=reel,   name="Réel",
                                   marker_color=prim,    marker_line_width=0, opacity=0.9))
        fig_pulse.add_trace(go.Bar(x=heures, y=predit,  name="Prédit",
                                   marker_color=rouge_a, marker_line_width=0, opacity=0.7))
        fig_pulse.update_layout(
            barmode="overlay", height=260,
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color=pfont, family="Inter"), margin=dict(l=0, r=0, t=0, b=0),
            showlegend=True,
            legend=dict(font=dict(size=10, color=pfont), bgcolor="rgba(0,0,0,0)",
                        orientation="h", y=1.12, x=1, xanchor="right"),
            xaxis=dict(showgrid=False, zeroline=False, tickfont=dict(size=9, color=txt3)),
            yaxis=dict(showgrid=True, gridcolor=pgrid, zeroline=False,
                       tickfont=dict(size=9, color=txt3)),
        )
        st.markdown(f"""
        <div class='card' style='padding-bottom:8px'>
            <div style='font-size:14px;font-weight:700;color:{txt1};margin-bottom:4px;
                        display:flex;align-items:center;gap:8px'>
                <i class="fa-solid fa-signal" style="color:{prim};font-size:13px"></i>
                Pulse de Risque Réseau
            </div>
        </div>""", unsafe_allow_html=True)
        st.plotly_chart(fig_pulse, use_container_width=True, config={"displayModeBar": False})

    with col_gauge:
        precision = 93.0
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number", value=precision,
            number={"suffix": "%", "font": {"size": 28, "color": prim, "family": "Inter"}},
            gauge={
                "axis": {"range": [0, 100], "tickfont": {"color": pfont, "size": 9}},
                "bar":  {"color": prim, "thickness": 0.25},
                "bgcolor": "rgba(0,0,0,0)", "borderwidth": 0,
                "steps": [
                    {"range": [0, 60],   "color": rouge_a},
                    {"range": [60, 80],  "color": ora_a},
                    {"range": [80, 100], "color": vert_a},
                ],
                "threshold": {"line": {"color": vert, "width": 3},
                              "thickness": 0.75, "value": precision},
            },
        ))
        fig_gauge.update_layout(
            height=220, paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color=pfont, family="Inter"), margin=dict(l=20, r=20, t=20, b=10),
        )
        st.markdown(f"""
        <div class='card'>
            <div style='font-size:14px;font-weight:700;color:{txt1};margin-bottom:4px;
                        display:flex;align-items:center;gap:8px'>
                <i class="fa-solid fa-brain" style="color:{prim};font-size:13px"></i>
                Confiance du Modèle ML
            </div>
        </div>""", unsafe_allow_html=True)
        st.plotly_chart(fig_gauge, use_container_width=True, config={"displayModeBar": False})
        st.markdown(f"""
        <div style='font-size:11px;color:{txt2};text-align:center;margin-top:-8px;line-height:1.5'>
            Modèle XGBoost v4.2 optimisé pour la détection<br>de transactions frauduleuses transfrontalières.
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Heatmap temporelle
    st.markdown(f"""
    <div class='card' style='padding-bottom:8px'>
        <div style='font-size:14px;font-weight:700;color:{txt1};margin-bottom:4px;
                    display:flex;align-items:center;gap:8px'>
            <i class="fa-solid fa-calendar-week" style="color:{prim};font-size:13px"></i>
            Temporal Risk Heatmap (24/7)
        </div>
    </div>""", unsafe_allow_html=True)

    rng2  = np.random.default_rng(77)
    jours = ["LUN", "MAR", "MER", "JEU", "VEN", "SAM", "DIM"]
    base  = np.array([0.9, 1.3, 1.6, 1.7, 1.4, 1.1, 0.7, 0.5, 0.4, 0.3, 0.3, 0.4,
                      0.5, 0.5, 0.6, 0.7, 0.8, 0.9, 0.9, 1.0, 1.1, 1.2, 1.3, 1.1])
    hmap  = np.outer(rng2.uniform(0.8, 1.2, 7), base)
    hmap  = (hmap / hmap.max() * 100).round(0)

    fig_hmap = go.Figure(go.Heatmap(
        z=hmap, x=[f"{h:02d}h" for h in range(24)], y=jours,
        colorscale=[[0.0, prim_a], [0.5, prim], [0.75, ora], [1.0, rouge]],
        showscale=True,
        colorbar=dict(
            title=dict(text="Risque Faible → Critique", font=dict(size=10, color=pfont)),
            tickfont=dict(size=9, color=pfont), len=0.8,
        ),
        hovertemplate="%{y} %{x}: %{z:.0f}% risque<extra></extra>",
    ))
    fig_hmap.update_layout(
        height=280,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=pfont, family="Inter"), margin=dict(l=40, r=60, t=10, b=40),
        xaxis=dict(showgrid=False, tickfont=dict(size=9, color=txt3)),
        yaxis=dict(showgrid=False, tickfont=dict(size=10, color=txt3)),
    )
    st.plotly_chart(fig_hmap, use_container_width=True, config={"displayModeBar": False})

# ══════════════════════════════════════════════════════════════
# Onglet 2 — Démographies
# ══════════════════════════════════════════════════════════════
elif onglet == "Démographies":
    col_demo, col_var = st.columns(2, gap="medium")

    with col_demo:
        fig_demo = go.Figure()
        fig_demo.add_trace(go.Histogram(
            x=df_leg["age"], name="Légitime",
            nbinsx=10, marker_color=prim_a, opacity=0.85,
        ))
        fig_demo.add_trace(go.Histogram(
            x=df_frau["age"], name="Fraude",
            nbinsx=10, marker_color=rouge, opacity=0.85,
        ))
        fig_demo.update_layout(
            barmode="overlay", height=320,
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color=pfont, family="Inter"), margin=dict(l=0, r=0, t=0, b=0),
            showlegend=True,
            legend=dict(font=dict(size=10, color=pfont), bgcolor="rgba(0,0,0,0)"),
            xaxis=dict(showgrid=False, zeroline=False,
                       tickvals=[18, 25, 35, 45, 55],
                       ticktext=["18–25", "26–35", "36–45", "46–55", "55+"],
                       tickfont=dict(size=9, color=txt3)),
            yaxis=dict(showgrid=True, gridcolor=pgrid, zeroline=False,
                       tickfont=dict(size=9, color=txt3)),
        )
        st.markdown(f"""
        <div class='card' style='padding-bottom:8px'>
            <div style='font-size:14px;font-weight:700;color:{txt1};margin-bottom:4px;
                        display:flex;align-items:center;gap:8px'>
                <i class="fa-solid fa-users" style="color:{prim};font-size:13px"></i>
                Densité Démographique des Anomalies
            </div>
        </div>""", unsafe_allow_html=True)
        st.plotly_chart(fig_demo, use_container_width=True, config={"displayModeBar": False})

    with col_var:
        region_stats = df.groupby("region")["montant_transaction"].agg(["mean", "std"]).reset_index()
        region_stats.columns = ["region", "moy", "std"]
        region_stats = region_stats.sort_values("moy", ascending=False)
        max_moy = region_stats["moy"].max()

        var_rows = "".join(
            f"<div style='display:flex;align-items:center;gap:10px;padding:10px 0;border-bottom:1px solid {bdr}'>"
            f"<span style='font-size:12px;font-weight:600;color:{txt2};width:80px;flex-shrink:0'>{row['region']}</span>"
            f"<div style='flex:1;background:{bdr};border-radius:3px;height:6px'>"
            f"<div style='width:{int(row['moy']/max_moy*100)}%;height:100%;background:{prim};border-radius:3px'></div>"
            f"</div>"
            f"<i class='fa-solid fa-circle' style='color:{rouge};font-size:8px;width:16px;text-align:center'></i>"
            f"</div>"
            for _, row in region_stats.iterrows()
        )

        sample_top = df_fraude.nlargest(3, "montant_transaction")
        statuts = [
            f"<span style='background:{rouge_a};color:{rouge};padding:2px 8px;border-radius:4px;font-size:10px;font-weight:700'>CRITIQUE</span>",
            f"<span style='background:{prim_a};color:{prim};padding:2px 8px;border-radius:4px;font-size:10px;font-weight:700'>INVESTIGATION</span>",
            f"<span style='background:{ora_a};color:{ora};padding:2px 8px;border-radius:4px;font-size:10px;font-weight:700'>BLOQUÉ</span>",
        ]
        alerte_rows = ""
        for i, (_, row) in enumerate(sample_top.iterrows()):
            score = min(99, int(85 + row["montant_transaction"] / df["montant_transaction"].max() * 14))
            alerte_rows += (
                f"<div style='display:grid;grid-template-columns:1fr 1.2fr 0.8fr 1fr;align-items:center;"
                f"padding:8px 0;border-bottom:1px solid {bdr}'>"
                f"<div style='font-size:11px;color:{txt2};font-family:Space Mono,monospace'>"
                f"<i class='fa-regular fa-clock' style='margin-right:4px;font-size:10px'></i>"
                f"14:{20+i*5:02d}:{i*7:02d}</div>"
                f"<div style='font-size:11px;font-weight:600;color:{txt1}'>Node_{i+1}_LX</div>"
                f"<div style='font-size:11px;font-weight:700;color:{rouge}'>{score}.{i}</div>"
                + statuts[i % len(statuts)]
                + "</div>"
            )

        alerte_header = "".join(
            f"<div style='font-size:10px;font-weight:700;color:{txt3};text-transform:uppercase;letter-spacing:0.6px'>{h}</div>"
            for h in ["Horodatage", "Entité", "Score", "Statut"]
        )

        st.markdown(f"""
        <div class='card'>
            <div style='font-size:14px;font-weight:700;color:{txt1};margin-bottom:4px;
                        display:flex;align-items:center;gap:8px'>
                <i class="fa-solid fa-chart-area" style="color:{prim};font-size:13px"></i>
                Variance du Volume de Transaction
            </div>
            <div style='font-size:11px;color:{txt2};margin-bottom:12px;margin-left:21px'>Par région — montant moyen</div>
            {var_rows}
            <div style='margin-top:16px'>
                <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:8px'>
                    <span style='font-size:12px;font-weight:700;color:{txt1};display:flex;align-items:center;gap:6px'>
                        <i class="fa-solid fa-fire" style="color:{rouge};font-size:11px"></i>
                        Alertes de Haute Priorité
                    </span>
                    <span style='font-size:11px;color:{prim};font-weight:600;cursor:pointer'>Voir tout le journal</span>
                </div>
                <div style='display:grid;grid-template-columns:1fr 1.2fr 0.8fr 1fr;padding:6px 0;
                            border-bottom:2px solid {bdr}'>
                    {alerte_header}
                </div>
                {alerte_rows}
            </div>
        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# Onglet 3 — Distributions
# ══════════════════════════════════════════════════════════════
elif onglet == "Distributions":
    col_dist, col_box = st.columns(2, gap="medium")

    with col_dist:
        fig_dist = go.Figure()
        fig_dist.add_trace(go.Histogram(
            x=df_leg["montant_transaction"], name="Légitime",
            nbinsx=50, marker_color=prim, opacity=0.75,
        ))
        fig_dist.add_trace(go.Histogram(
            x=df_frau["montant_transaction"], name="Fraude",
            nbinsx=50, marker_color=rouge, opacity=0.75,
        ))
        fig_dist.update_layout(
            barmode="overlay", height=340,
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color=pfont, family="Inter"), margin=dict(l=10, r=10, t=10, b=40),
            showlegend=True,
            legend=dict(font=dict(size=10, color=pfont), bgcolor="rgba(0,0,0,0)",
                        orientation="v", x=1, xanchor="right", y=1),
            xaxis=dict(title=dict(text="Montant (FCFA)", font=dict(size=10, color=txt3)),
                       showgrid=False, zeroline=False, tickfont=dict(size=9, color=txt3)),
            yaxis=dict(showgrid=True, gridcolor=pgrid, zeroline=False,
                       tickfont=dict(size=9, color=txt3)),
        )
        with st.container(border=True):
            st.markdown(
                f"<div style='font-size:11px;font-weight:700;color:{txt1};text-transform:uppercase;"
                f"letter-spacing:0.8px;margin-bottom:6px;display:flex;align-items:center;gap:7px'>"
                f"<i class='fa-solid fa-chart-bar' style='color:{prim};font-size:11px'></i>"
                f"Distribution des Montants</div>",
                unsafe_allow_html=True,
            )
            st.plotly_chart(fig_dist, use_container_width=True, config={"displayModeBar": False})

    with col_box:
        fig_box = go.Figure()
        fig_box.add_trace(go.Box(
            y=df_leg["score_credit"], name="Légitime",
            marker_color=prim, line_color=prim, fillcolor=prim_a, boxpoints=False,
        ))
        fig_box.add_trace(go.Box(
            y=df_frau["score_credit"], name="Fraude",
            marker_color=rouge, line_color=rouge, fillcolor=rouge_a, boxpoints=False,
        ))
        fig_box.update_layout(
            height=340,
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color=pfont, family="Inter"), margin=dict(l=10, r=10, t=10, b=40),
            showlegend=True,
            legend=dict(font=dict(size=10, color=pfont), bgcolor="rgba(0,0,0,0)",
                        orientation="v", x=1, xanchor="right", y=1),
            xaxis=dict(showgrid=False, zeroline=False, tickfont=dict(size=9, color=txt3)),
            yaxis=dict(showgrid=True, gridcolor=pgrid, zeroline=False,
                       tickfont=dict(size=9, color=txt3)),
        )
        with st.container(border=True):
            st.markdown(
                f"<div style='font-size:11px;font-weight:700;color:{txt1};text-transform:uppercase;"
                f"letter-spacing:0.8px;margin-bottom:6px;display:flex;align-items:center;gap:7px'>"
                f"<i class='fa-solid fa-credit-card' style='color:{prim};font-size:11px'></i>"
                f"Score de Crédit par Statut</div>",
                unsafe_allow_html=True,
            )
            st.plotly_chart(fig_box, use_container_width=True, config={"displayModeBar": False})

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    col_sc1, col_sc2 = st.columns(2, gap="medium")
    sleg  = df_leg.sample(min(500, len(df_leg)),   random_state=42)
    sfrau = df_frau.sample(min(100, len(df_frau)), random_state=42)

    with col_sc1:
        fig_sc1 = go.Figure()
        fig_sc1.add_trace(go.Scatter(
            x=sleg["age"], y=sleg["montant_transaction"],
            mode="markers", name="Légitime",
            marker=dict(color=prim, size=5, opacity=0.5, symbol="circle"),
        ))
        fig_sc1.add_trace(go.Scatter(
            x=sfrau["age"], y=sfrau["montant_transaction"],
            mode="markers", name="Fraude",
            marker=dict(color=rouge, size=7, opacity=0.85, symbol="x"),
        ))
        fig_sc1.update_layout(
            height=340,
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color=pfont, family="Inter"), margin=dict(l=10, r=10, t=10, b=40),
            showlegend=True,
            legend=dict(font=dict(size=10, color=pfont), bgcolor="rgba(0,0,0,0)",
                        orientation="v", x=1, xanchor="right", y=1),
            xaxis=dict(title=dict(text="Âge", font=dict(size=10, color=txt3)),
                       showgrid=False, zeroline=False, tickfont=dict(size=9, color=txt3)),
            yaxis=dict(title=dict(text="Montant (FCFA)", font=dict(size=10, color=txt3)),
                       showgrid=True, gridcolor=pgrid, zeroline=False,
                       tickfont=dict(size=9, color=txt3)),
        )
        with st.container(border=True):
            st.markdown(
                f"<div style='font-size:11px;font-weight:700;color:{txt1};text-transform:uppercase;"
                f"letter-spacing:0.8px;margin-bottom:6px;display:flex;align-items:center;gap:7px'>"
                f"<i class='fa-solid fa-person' style='color:{prim};font-size:11px'></i>"
                f"Âge vs Montant</div>",
                unsafe_allow_html=True,
            )
            st.plotly_chart(fig_sc1, use_container_width=True, config={"displayModeBar": False})

    with col_sc2:
        fig_sc2 = go.Figure()
        fig_sc2.add_trace(go.Scatter(
            x=sleg["salaire"], y=sleg["score_credit"],
            mode="markers", name="Légitime",
            marker=dict(color=prim, size=5, opacity=0.5, symbol="circle"),
        ))
        fig_sc2.add_trace(go.Scatter(
            x=sfrau["salaire"], y=sfrau["score_credit"],
            mode="markers", name="Fraude",
            marker=dict(color=rouge, size=7, opacity=0.85, symbol="x"),
        ))
        fig_sc2.update_layout(
            height=340,
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color=pfont, family="Inter"), margin=dict(l=10, r=10, t=10, b=40),
            showlegend=True,
            legend=dict(font=dict(size=10, color=pfont), bgcolor="rgba(0,0,0,0)",
                        orientation="v", x=1, xanchor="right", y=1),
            xaxis=dict(title=dict(text="Salaire (FCFA)", font=dict(size=10, color=txt3)),
                       showgrid=False, zeroline=False, tickfont=dict(size=9, color=txt3)),
            yaxis=dict(title=dict(text="Score de Crédit", font=dict(size=10, color=txt3)),
                       showgrid=True, gridcolor=pgrid, zeroline=False,
                       tickfont=dict(size=9, color=txt3)),
        )
        with st.container(border=True):
            st.markdown(
                f"<div style='font-size:11px;font-weight:700;color:{txt1};text-transform:uppercase;"
                f"letter-spacing:0.8px;margin-bottom:6px;display:flex;align-items:center;gap:7px'>"
                f"<i class='fa-solid fa-coins' style='color:{prim};font-size:11px'></i>"
                f"Salaire vs Score de Crédit</div>",
                unsafe_allow_html=True,
            )
            st.plotly_chart(fig_sc2, use_container_width=True, config={"displayModeBar": False})
