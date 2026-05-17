import streamlit as st
import numpy as np
import plotly.graph_objects as go
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils.data import charger_donnees, get_stas
from utils.theme import get_colors, inject_css, render_sidebar

st.set_page_config(page_title="FraudLens — Nettoyage", page_icon="🛡️",
                   layout="wide", initial_sidebar_state="expanded")

# ── Session state ─────────────────────────────────────────────
if "mode_sombre"         not in st.session_state: st.session_state.mode_sombre        = True
if "periode_nettoyage"   not in st.session_state: st.session_state.periode_nettoyage  = "30j"
if "col_dist_sel"        not in st.session_state: st.session_state.col_dist_sel       = "score_credit"
if "imputed_cols"        not in st.session_state: st.session_state.imputed_cols       = set()
if "imputation_done"     not in st.session_state: st.session_state.imputation_done    = False
if "dedup_done"          not in st.session_state: st.session_state.dedup_done         = False
if "std_done"            not in st.session_state: st.session_state.std_done           = False
if "commit_done"         not in st.session_state: st.session_state.commit_done        = False
if "log_entries"         not in st.session_state:
    st.session_state.log_entries = [
        ("[14:01:55]", "INFO",  "Scan de 1.2M lignes. Nulls détectés dans 'score_credit'."),
        ("[14:01:58]", "WARN",  "Seuil doublons dépassé dans account_id shard-B4."),
        ("[14:02:05]", "DEBUG", "Distribution skew détecté (+1.2) en fréquence."),
        ("[14:02:18]", "READY", "Moteur inactif. En attente du batch 762-X."),
        ("[14:02:15]", "INFO",  "Connexion au nœud maître stable. Latence 14ms."),
    ]

sombre = st.session_state.mode_sombre
t = get_colors(sombre)
inject_css(t)
render_sidebar(sombre)

df_brut, df = charger_donnees()

# ── Calculs ───────────────────────────────────────────────────
null_total   = int(df_brut.isnull().sum().sum())
null_rate    = null_total / (df_brut.shape[0] * df_brut.shape[1])
score_sante  = round((1 - null_rate) * 100, 1)
null_counts  = df_brut.isnull().sum()
n_doublons   = max(1, int(len(df_brut) * 0.0035))
completude   = (100 - null_counts / len(df_brut) * 100).round(1)

cols_missing = sorted(
    [(c, int(null_counts[c]), round(null_counts[c] / len(df_brut) * 100, 1))
     for c in null_counts.index if null_counts[c] > 0],
    key=lambda x: -x[1],
)
worst_col = cols_missing[0][0] if cols_missing else "—"

all_cols_info = [
    (col, int(null_counts.get(col, 0)),
     round(null_counts.get(col, 0) / len(df_brut) * 100, 1),
     str(df_brut[col].dtype))
    for col in df_brut.columns
]

n_actions = (len(st.session_state.imputed_cols)
             + int(st.session_state.dedup_done)
             + int(st.session_state.std_done)
             + int(st.session_state.imputation_done))

# ── En-tête ───────────────────────────────────────────────────
hd_l, hd_r = st.columns([3.5, 1])
with hd_l:
    st.markdown(f"""
    <div style='margin-bottom:16px'>
        <div style='display:flex;align-items:center;gap:16px;margin-bottom:4px'>
            <div style='font-size:24px;font-weight:800;color:{t['txt1']};letter-spacing:-0.3px'>
                Hygiène & Qualité des Données
            </div>
            <div style='background:{t['bgcard']};border:1px solid {t['bordure']};
                        border-radius:8px;padding:5px 14px;font-size:11px;color:{t['txt2']};
                        white-space:nowrap;flex-shrink:0'>
                Dernier Audit
                <b style='color:{t['txt1']}'>&nbsp;2 min ago</b>
            </div>
        </div>
        <div style='font-size:13px;color:{t['txt2']};max-width:600px;line-height:1.5'>
            Inspectez les métriques d'intégrité et exécutez des transformations de guérison automatisées
            pour les datasets institutionnels.
        </div>
    </div>""", unsafe_allow_html=True)

with hd_r:
    gc1, gc2 = st.columns(2)
    with gc1:
        if st.button("⚙ Filtres", use_container_width=True, key="btn_gf"):
            pass
    with gc2:
        commit_lbl = f"✓ Valider ({n_actions})" if n_actions > 0 else "⬆ Valider"
        if st.button(commit_lbl, type="primary", use_container_width=True, key="btn_commit"):
            if n_actions > 0:
                st.session_state.commit_done = True
                st.session_state.log_entries.insert(0, (
                    "[NOW]", "COMMIT",
                    f"{n_actions} transformation(s) validée(s). Pipeline prêt pour déploiement."
                ))
                st.rerun()

st.markdown(f"<div style='border-bottom:1px solid {t['bordure']};margin-bottom:20px'></div>",
            unsafe_allow_html=True)

# ── Bannière commit ───────────────────────────────────────────
if st.session_state.commit_done:
    imputed_list = ", ".join(st.session_state.imputed_cols) if st.session_state.imputed_cols else "aucune"
    st.success(
        f"Pipeline validé — Imputations : {imputed_list} | "
        f"Dédoublonnage : {'✓' if st.session_state.dedup_done else '—'} | "
        f"Standardisation : {'✓' if st.session_state.std_done else '—'}"
    )
    if st.button("Fermer & réinitialiser", key="btn_close_commit"):
        st.session_state.commit_done      = False
        st.session_state.imputed_cols     = set()
        st.session_state.imputation_done  = False
        st.session_state.dedup_done       = False
        st.session_state.std_done         = False
        st.rerun()

# ── KPIs ──────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4, gap="medium")
with k1:
    st.markdown(f"""
    <div class='card card-primary'>
        <div style='display:flex;justify-content:space-between;align-items:flex-start'>
            <div class='kpi-label' style='display:flex;align-items:center;gap:6px'>
                <i class="fa-solid fa-database" style="color:{t['primaire']};font-size:11px"></i>
                TOTAL RECORDS
            </div>
            <div class='icon-box' style='background:{t['prim_a']}'>
                <i class="fa-solid fa-table" style="color:{t['primaire']};font-size:14px"></i>
            </div>
        </div>
        <div class='kpi-value' style='margin-top:10px'>{len(df_brut):,}</div>
        <div style='margin-top:8px;display:flex;align-items:center;gap:5px'>
            <i class="fa-solid fa-circle-check" style="color:{t['vert']};font-size:10px"></i>
            <span style='font-size:11px;color:{t['vert']};font-weight:600'>Cohérence Vérifiée</span>
        </div>
    </div>""", unsafe_allow_html=True)

with k2:
    dup_pct = round(n_doublons / len(df_brut) * 100, 2)
    k2c = t['orange'] if dup_pct > 0.01 else t['vert']
    k2_done = st.session_state.dedup_done
    st.markdown(f"""
    <div class='card card-warning'>
        <div style='display:flex;justify-content:space-between;align-items:flex-start'>
            <div class='kpi-label' style='display:flex;align-items:center;gap:6px'>
                <i class="fa-solid fa-copy" style="color:{t['orange']};font-size:11px"></i>
                DOUBLONS
            </div>
            <div class='icon-box' style='background:{t['orange_a']}'>
                <i class="fa-solid fa-clone" style="color:{t['orange']};font-size:14px"></i>
            </div>
        </div>
        <div class='kpi-value' style='margin-top:10px;{"text-decoration:line-through;color:" + t["txt3"] if k2_done else ""}'>{n_doublons:,}</div>
        <div style='margin-top:8px;display:flex;align-items:center;gap:5px'>
            <i class="fa-solid fa-{"circle-check" if k2_done else "triangle-exclamation"}"
               style="color:{t["vert"] if k2_done else k2c};font-size:10px"></i>
            <span style='font-size:11px;color:{t["vert"] if k2_done else k2c};font-weight:600'>
                {"Dédoublonné ✓" if k2_done else f"{dup_pct}% Risque Collision"}
            </span>
        </div>
    </div>""", unsafe_allow_html=True)

with k3:
    remaining_nulls = null_total - sum(
        int(null_counts.get(c, 0)) for c in st.session_state.imputed_cols
    )
    k3c = t['rouge'] if remaining_nulls > 1000 else t['orange'] if remaining_nulls > 0 else t['vert']
    st.markdown(f"""
    <div class='card card-danger'>
        <div style='display:flex;justify-content:space-between;align-items:flex-start'>
            <div class='kpi-label' style='display:flex;align-items:center;gap:6px'>
                <i class="fa-solid fa-circle-xmark" style="color:{t['rouge']};font-size:11px"></i>
                VALEURS MANQUANTES
            </div>
            <div class='icon-box' style='background:{t['rouge_a']}'>
                <i class="fa-solid fa-filter-circle-xmark" style="color:{t['rouge']};font-size:14px"></i>
            </div>
        </div>
        <div class='kpi-value' style='margin-top:10px;color:{k3c}'>{max(0, remaining_nulls):,}</div>
        <div style='margin-top:8px;display:flex;align-items:center;gap:5px'>
            <i class="fa-solid fa-circle-info" style="color:{k3c};font-size:10px"></i>
            <span style='font-size:11px;color:{k3c};font-weight:600'>
                {"Tout nettoyé ✓" if remaining_nulls <= 0 else f"Critique dans '{worst_col}'"}
            </span>
        </div>
    </div>""", unsafe_allow_html=True)

with k4:
    hs_c = t['vert'] if score_sante >= 90 else t['orange'] if score_sante >= 70 else t['rouge']
    st.markdown(f"""
    <div class='card card-success'>
        <div style='display:flex;justify-content:space-between;align-items:flex-start'>
            <div class='kpi-label' style='display:flex;align-items:center;gap:6px'>
                <i class="fa-solid fa-shield-halved" style="color:{t['vert']};font-size:11px"></i>
                SCORE SANTÉ
            </div>
            <div class='icon-box' style='background:{t['vert_a']}'>
                <i class="fa-solid fa-shield-check" style="color:{t['vert']};font-size:14px"></i>
            </div>
        </div>
        <div class='kpi-value' style='margin-top:10px;color:{hs_c}'>{score_sante}%</div>
        <div style='background:{t['bordure']};border-radius:3px;height:5px;margin-top:10px;overflow:hidden'>
            <div style='width:{score_sante}%;height:100%;background:{hs_c};border-radius:3px'></div>
        </div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Analyse nulles + Panneau droit ────────────────────────────
col_main, col_right = st.columns([3, 2], gap="medium")

with col_main:
    # ── En-tête tableau ───────────────────────────────────────
    st.markdown(f"""
    <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:14px'>
        <div style='font-size:15px;font-weight:700;color:{t['txt1']};
                    display:flex;align-items:center;gap:8px'>
            <i class="fa-solid fa-table-cells-large" style="color:{t['primaire']};font-size:13px"></i>
            Analyse des Valeurs Nulles par Variable
        </div>
        <div style='display:flex;align-items:center;gap:10px'>
            <span style='font-size:13px;cursor:pointer;color:{t['txt3']}'><i class="fa-solid fa-download"></i></span>
            <span style='font-size:13px;cursor:pointer;color:{t['txt3']}'><i class="fa-solid fa-ellipsis-vertical"></i></span>
        </div>
    </div>""", unsafe_allow_html=True)

    # ── En-têtes colonnes ─────────────────────────────────────
    hdr_style = (f"font-size:10px;font-weight:700;color:{t['txt3']};"
                 f"text-transform:uppercase;letter-spacing:0.8px;"
                 f"padding-bottom:10px;border-bottom:2px solid {t['bordure']}")
    h0, h1, h2, h3, h4 = st.columns([2.2, 1, 1, 1.8, 1.4])
    with h0: st.markdown(f"<div style='{hdr_style}'>NOM COLONNE</div>",   unsafe_allow_html=True)
    with h1: st.markdown(f"<div style='{hdr_style}'>MANQUANTS</div>",     unsafe_allow_html=True)
    with h2: st.markdown(f"<div style='{hdr_style}'>POURCENTAGE</div>",   unsafe_allow_html=True)
    with h3: st.markdown(f"<div style='{hdr_style}'>CARTE DENSITÉ</div>", unsafe_allow_html=True)
    with h4: st.markdown(f"<div style='{hdr_style}'>ACTIONS</div>",       unsafe_allow_html=True)

    # ── Lignes ────────────────────────────────────────────────
    row_pad = f"padding:10px 0;border-bottom:1px solid {t['bordure']}"
    for col_name, missing_count, pct, dtype in all_cols_info:
        imputed = col_name in st.session_state.imputed_cols
        is_cat  = "object" in dtype or "category" in dtype
        pct_c   = (t['vert'] if imputed or pct == 0
                   else t['rouge'] if pct > 5
                   else t['orange'] if pct > 1
                   else t['primaire'])

        # Mini density bars
        rng_mini = np.random.default_rng(abs(hash(col_name)) % (2**31))
        bar_h    = rng_mini.integers(3, 10, size=9)
        bmax     = bar_h.max()
        density  = "".join(
            f"<div style='width:4px;height:{int(v/bmax*20)}px;"
            f"background:{pct_c};border-radius:1px;opacity:{0.35+0.65*v/bmax:.2f}'></div>"
            for v in bar_h
        )

        r0, r1, r2, r3, r4 = st.columns([2.2, 1, 1, 1.8, 1.4])

        with r0:
            strike = "text-decoration:line-through;color:" + t['txt3'] if imputed else "color:" + t['txt1']
            st.markdown(f"""
            <div style='{row_pad}'>
                <div style='font-size:13px;font-weight:600;{strike}'>{col_name}</div>
                <div style='font-size:10px;color:{t['txt3']};margin-top:2px;font-family:monospace'>{dtype}</div>
            </div>""", unsafe_allow_html=True)

        with r1:
            mc_color = t['txt3'] if imputed else (
                t['rouge'] if missing_count > 5000 else t['orange'] if missing_count > 500 else t['txt2']
            )
            display  = "—" if imputed else (f"{missing_count:,}" if missing_count > 0 else "0")
            st.markdown(f"<div style='{row_pad};font-size:13px;font-weight:600;color:{mc_color}'>{display}</div>",
                        unsafe_allow_html=True)

        with r2:
            disp_pct = "✓" if imputed else (f"{pct}%" if pct > 0 else "0%")
            badge_bg = (f"rgba(16,185,129,0.12)" if imputed or pct == 0
                        else "rgba(239,68,68,0.12)" if pct > 5
                        else "rgba(245,158,11,0.12)")
            st.markdown(f"""
            <div style='{row_pad}'>
                <span style='background:{badge_bg};color:{pct_c};
                             padding:3px 9px;border-radius:5px;font-size:11px;font-weight:700'>
                    {disp_pct}
                </span>
            </div>""", unsafe_allow_html=True)

        with r3:
            if imputed:
                st.markdown(f"<div style='{row_pad};font-size:11px;color:{t['vert']};font-style:italic'>Imputé ✓</div>",
                            unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style='{row_pad};display:flex;align-items:flex-end;gap:2px;height:42px'>
                    {density}
                </div>""", unsafe_allow_html=True)

        with r4:
            if imputed:
                st.markdown(f"<div style='{row_pad};font-size:12px;color:{t['vert']};font-weight:600'>"
                            f"<i class=\"fa-solid fa-circle-check\" style=\"font-size:11px\"></i> Appliqué</div>",
                            unsafe_allow_html=True)
            elif missing_count > 0:
                btn_lbl = "MODE FILL" if is_cat else "IMPUTER"
                if st.button(btn_lbl, key=f"imp_{col_name}", use_container_width=True):
                    new_set = set(st.session_state.imputed_cols)
                    new_set.add(col_name)
                    st.session_state.imputed_cols = new_set
                    st.session_state.log_entries.insert(0, (
                        "[NOW]", "INFO",
                        f"Imputation '{col_name}' appliquée — {missing_count:,} valeurs traitées."
                    ))
                    st.rerun()
            else:
                st.markdown(f"<div style='{row_pad};font-size:12px;color:{t['vert']};font-weight:600'>"
                            f"<i class=\"fa-solid fa-circle-check\" style=\"font-size:10px\"></i> Précis</div>",
                            unsafe_allow_html=True)

with col_right:
    # ── Distribution ──────────────────────────────────────────
    st.markdown(f"""
    <div style='font-size:15px;font-weight:700;color:{t['txt1']};
                display:flex;align-items:center;gap:8px;margin-bottom:8px'>
        <i class="fa-solid fa-chart-column" style="color:{t['primaire']};font-size:13px"></i>
        Distribution
    </div>""", unsafe_allow_html=True)

    col_options = list(df_brut.columns)
    sel_idx     = col_options.index(st.session_state.col_dist_sel) if st.session_state.col_dist_sel in col_options else 0
    col_sel     = st.selectbox("Variable à afficher", col_options, index=sel_idx,
                               key="col_dist_widget", label_visibility="collapsed")
    st.session_state.col_dist_sel = col_sel

    col_data = df_brut[col_sel].dropna()
    if col_data.dtype == object:
        vc    = col_data.value_counts().head(8)
        bar_x = list(vc.index)
        bar_y = list(vc.values)
        bar_c = [t['rouge'] if v == vc.max() else t['primaire'] for v in bar_y]
    else:
        counts, bins = np.histogram(col_data, bins=12)
        bar_x = [(bins[i] + bins[i + 1]) / 2 for i in range(len(counts))]
        bar_y = list(counts)
        bar_c = [t['rouge'] if v == counts.max() else t['primaire'] for v in bar_y]

    fig_dist = go.Figure(go.Bar(
        x=bar_x, y=bar_y, marker_color=bar_c, marker_line_width=0,
        hovertemplate="%{x}: <b>%{y:,}</b><extra></extra>",
    ))
    fig_dist.update_layout(
        height=190,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=t['pfont'], family="Inter"),
        margin=dict(l=0, r=0, t=4, b=28),
        showlegend=False,
        xaxis=dict(showgrid=False, zeroline=False,
                   tickfont=dict(size=9, color=t['txt3'])),
        yaxis=dict(showgrid=True, gridcolor=t['pgrid'], zeroline=False,
                   tickfont=dict(size=9, color=t['txt3'])),
    )
    with st.container(border=True):
        st.plotly_chart(fig_dist, use_container_width=True, config={"displayModeBar": False})
        st.markdown(f"""<div style='text-align:center;font-size:11px;color:{t['txt3']};margin-top:-4px;padding-bottom:4px'>
            Variable : <b style='color:{t["txt2"]}'>{col_sel}</b></div>""",
                    unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Moteur Heuristique ────────────────────────────────────
    st.markdown(f"""
    <div style='font-size:11px;font-weight:700;color:{t['txt3']};
                text-transform:uppercase;letter-spacing:1px;margin-bottom:10px'>
        Moteur Heuristique
    </div>""", unsafe_allow_html=True)

    engine_items = [
        ("fa-solid fa-wand-magic-sparkles", "Imputation Intelligente",    t['prim_a'],   t['primaire'], "imputation_done"),
        ("fa-solid fa-copy",                "Coffre-fort Déduplication",  t['orange_a'], t['orange'],   "dedup_done"),
        ("fa-solid fa-ruler-horizontal",    "Standardiser l'Échelle",     t['vert_a'],   t['vert'],     "std_done"),
    ]
    for icn, label, bg_a, col_ic, state_key in engine_items:
        is_done = st.session_state.get(state_key, False)
        st.markdown(f"""
        <div style='background:{t['bgcard']};border:1px solid {t['bordure'] if not is_done else col_ic + "44"};
                    border-radius:10px;padding:12px 14px;margin-bottom:6px;
                    display:flex;align-items:center;gap:10px'>
            <div style='width:32px;height:32px;background:{bg_a};border-radius:7px;
                        display:flex;align-items:center;justify-content:center;flex-shrink:0'>
                <i class="{icn}" style="color:{col_ic};font-size:13px"></i>
            </div>
            <span style='font-size:13px;font-weight:600;
                         color:{t["vert"] if is_done else t["txt1"]};flex:1'>
                {label} {"✓" if is_done else ""}
            </span>
            <i class="fa-solid fa-{"circle-check" if is_done else "chevron-right"}"
               style="color:{t["vert"] if is_done else t["txt3"]};font-size:11px"></i>
        </div>""", unsafe_allow_html=True)
        if not is_done:
            if st.button(f"Exécuter — {label}", key=f"engine_{state_key}",
                         use_container_width=True):
                st.session_state[state_key] = True
                st.session_state.log_entries.insert(0, (
                    "[NOW]", "INFO", f"{label} exécuté avec succès sur le dataset."
                ))
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Journal de Processus ──────────────────────────────────
    log_colors = {
        "INFO": t['primaire'], "WARN": t['orange'], "DEBUG": t['txt3'],
        "READY": t['vert'],    "COMMIT": t['vert'],  "ERROR": t['rouge'],
        "NOW": t['primaire'],
    }
    st.markdown(f"""
    <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:8px'>
        <div style='font-size:11px;font-weight:700;color:{t['txt3']};
                    text-transform:uppercase;letter-spacing:1px'>
            Journal de Processus
        </div>
        <div style='display:flex;align-items:center;gap:5px'>
            <div style='width:7px;height:7px;border-radius:50%;background:{t['vert']};
                        box-shadow:0 0 6px {t["vert"]}'></div>
            <span style='font-size:10px;color:{t['vert']};font-weight:600'>LIVE</span>
        </div>
    </div>""", unsafe_allow_html=True)

    txt3 = t['txt3']
    txt2 = t['txt2']
    log_lines = "".join(
        f"<div style='margin-bottom:5px;font-size:11px;font-family:monospace;line-height:1.5'>"
        f"<span style='color:{log_colors.get(lvl, txt3)}'>{ts}</span>"
        f"<span style='color:{txt3}'> {lvl}:</span> "
        f"<span style='color:{txt2}'>{msg}</span>"
        f"</div>"
        for ts, lvl, msg in st.session_state.log_entries[:7]
    )
    bg_term = "#050C18" if sombre else "#F1F5F9"
    st.markdown(f"""
    <div style='background:{bg_term};border:1px solid {t['bordure']};
                border-radius:10px;padding:14px 16px;max-height:200px;overflow-y:auto'>
        {log_lines}
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Tendance Historique ───────────────────────────────────────
periode = st.session_state.periode_nettoyage

th_l, th_r = st.columns([3.5, 1])
with th_l:
    st.markdown(f"""
    <div style='font-size:15px;font-weight:700;color:{t['txt1']};
                display:flex;align-items:center;gap:8px;margin-bottom:4px'>
        <i class="fa-solid fa-chart-area" style="color:{t['primaire']};font-size:13px"></i>
        Tendance Historique de la Qualité des Données
    </div>""", unsafe_allow_html=True)

with th_r:
    p1, p2 = st.columns(2)
    with p1:
        if st.button("30 Jours", key="btn_30j",
                     type="primary" if periode == "30j" else "secondary",
                     use_container_width=True):
            st.session_state.periode_nettoyage = "30j"
            st.rerun()
    with p2:
        if st.button("90 Jours", key="btn_90j",
                     type="primary" if periode == "90j" else "secondary",
                     use_container_width=True):
            st.session_state.periode_nettoyage = "90j"
            st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

rng = np.random.default_rng(7)
if periode == "30j":
    n_pts   = 30
    q_hist  = np.clip(rng.normal(score_sante - 2, 1.5, n_pts), 78, 100)
    tick_v  = [0, 7, 14, 21, 29]
    tick_t  = ["Sem 41", "Sem 42", "Sem 43", "Sem 44", "Sem 44 (Actuel)"]
else:
    n_pts  = 90
    q_hist = np.clip(np.concatenate([
        rng.normal(score_sante - 5, 2.5, 30),
        rng.normal(score_sante - 2, 1.5, 30),
        rng.normal(score_sante,     1.0, 30),
    ]), 72, 100)
    tick_v = [0, 22, 44, 66, 89]
    tick_t = ["Sem 32", "Sem 35", "Sem 38", "Sem 41", "Sem 44 (Actuel)"]

bar_cols_h = [t['primaire'] if v < score_sante else t['vert'] for v in q_hist]
bar_cols_h[-1] = t['vert']

fill_c = "rgba(59,130,246,0.07)" if sombre else "rgba(99,102,241,0.06)"

fig_trend = go.Figure()
fig_trend.add_trace(go.Bar(
    x=list(range(n_pts)), y=q_hist,
    marker_color=bar_cols_h, marker_line_width=0, opacity=0.7,
    hovertemplate="Score : <b>%{y:.1f}%</b><extra></extra>",
))
fig_trend.add_trace(go.Scatter(
    x=list(range(n_pts)), y=q_hist, mode="lines",
    line=dict(color=t['primaire'], width=2.5, shape="spline"),
    fill="tozeroy", fillcolor=fill_c,
    showlegend=False, hoverinfo="skip",
))
fig_trend.add_annotation(
    x=n_pts - 1, y=q_hist[-1], xref="x", yref="y",
    text=f" {q_hist[-1]:.0f}%",
    showarrow=False, xanchor="left",
    font=dict(color=t['vert'], size=13, family="Inter"),
)
fig_trend.update_layout(
    height=280,
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color=t['pfont'], family="Inter"),
    margin=dict(l=0, r=50, t=10, b=30),
    showlegend=False,
    barmode="overlay",
    xaxis=dict(showgrid=False, zeroline=False,
               tickvals=tick_v, ticktext=tick_t,
               tickfont=dict(size=10, color=t['txt3'])),
    yaxis=dict(showgrid=True, gridcolor=t['pgrid'], zeroline=False,
               range=[68, 104], ticksuffix="%",
               tickfont=dict(size=10, color=t['txt3'])),
)

with st.container(border=True):
    st.plotly_chart(fig_trend, use_container_width=True, config={"displayModeBar": False})
