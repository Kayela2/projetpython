import streamlit as st
import plotly.graph_objects as go
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils.data import charger_donnees, get_stas
from utils.theme import get_colors, inject_css, render_sidebar

# Hotspot nodes fixes pour la carte monde
NODES = [
    ("Paris-Bercy",      48.85,   2.35,  94, True),
    ("Lagos Hub",         6.45,   3.40,  87, True),
    ("Abidjan Signal",    5.35,  -4.00,  73, True),
    ("São Paulo Node",  -23.55, -46.63,  78, True),
    ("Shanghai Gateway", 31.22, 121.46,  71, True),
    ("Cairo Node",       30.06,  31.24,  61, True),
    ("Dubai Terminal",   25.20,  55.27,  65, True),
    ("Mumbai Relay",     19.07,  72.87,  58, False),
    ("London Nexus",     51.51,  -0.13,  52, False),
    ("New York Alpha",   40.71, -74.01,  48, False),
    ("Sydney Branch",   -33.87, 151.21,  42, False),
    ("Moscow Point",     55.75,  37.62,  38, False),
]

st.set_page_config(page_title="FraudLens — Profil des Fraudes", page_icon="🛡️",
                   layout="wide", initial_sidebar_state="expanded")

if "mode_sombre" not in st.session_state:
    st.session_state.mode_sombre = True

sombre = st.session_state.mode_sombre
t = get_colors(sombre)
inject_css(t)
render_sidebar(sombre)

df_brut, df = charger_donnees()
stats     = get_stas(df)
df_fraude = df[df["fraude"] == 1]

# ── En-tête ───────────────────────────────────────────────────
st.markdown(f"""
<div style='display:flex;align-items:center;justify-content:space-between;
            margin-bottom:20px;padding-bottom:16px;border-bottom:1px solid {t['bordure']}'>
    <div style='background:{t['bgcard']};border:1px solid {t['bordure']};border-radius:10px;
                padding:10px 18px;display:flex;align-items:center;gap:10px;min-width:320px'>
        <i class="fa-solid fa-magnifying-glass" style="color:{t['txt3']};font-size:13px"></i>
        <span style='color:{t['txt3']};font-size:13px'>Rechercher une entité ou un signal...</span>
    </div>
    <div style='display:flex;gap:8px;margin-left:auto'>
        <span style='background:{t['bgsub']};border:1px solid {t['bordure']};padding:8px 16px;
                    border-radius:8px;font-size:12px;color:{t['txt2']};cursor:pointer;display:flex;align-items:center;gap:6px'>
            <i class="fa-solid fa-sliders" style="font-size:11px"></i> Filtrer
        </span>
        <span style='background:{t['bgsub']};border:1px solid {t['bordure']};padding:8px 16px;
                    border-radius:8px;font-size:12px;color:{t['txt2']};cursor:pointer;display:flex;align-items:center;gap:6px'>
            <i class="fa-solid fa-download" style="font-size:11px"></i> Exporter le Rapport
        </span>
    </div>
</div>
<div style='margin-bottom:16px'>
    <div style='font-size:15px;font-weight:700;color:{t['txt1']}'>Analyse de Profilage de Fraude</div>
    <div style='font-size:12px;color:{t['txt2']};margin-top:2px'>Identification des archétypes de menaces et segmentation des risques réseau.</div>
</div>""", unsafe_allow_html=True)

# ── Carte + Unités actives ────────────────────────────────────
col_map, col_units = st.columns([2, 1], gap="medium")

with col_map:
    rouge  = t['rouge'];  prim  = t['primaire']
    pfont  = t['pfont'];  txt2  = t['txt2'];  txt3 = t['txt3']

    lats   = [n[1] for n in NODES]
    lons   = [n[2] for n in NODES]
    names  = [n[0] for n in NODES]
    risks  = [n[3] for n in NODES]
    is_cr  = [n[4] for n in NODES]
    sizes  = [9 + r // 10 for r in risks]

    cr_idx = [i for i, c in enumerate(is_cr) if c]
    sf_idx = [i for i, c in enumerate(is_cr) if not c]

    land_c  = "#0D1B3E" if sombre else "#DBEAFE"
    ocean_c = "#060D20" if sombre else "#EEF2FF"
    ctry_c  = "rgba(255,255,255,0.07)" if sombre else "rgba(0,0,0,0.08)"
    coast_c = "rgba(255,255,255,0.10)" if sombre else "rgba(0,0,0,0.12)"

    fig_map = go.Figure()
    fig_map.add_trace(go.Scattergeo(
        lat=[lats[i] for i in cr_idx],
        lon=[lons[i] for i in cr_idx],
        text=[f"<b>Node: {names[i]}</b><br>{risks[i]}% Risk" for i in cr_idx],
        mode="markers",
        name="Risque Critique",
        marker=dict(
            size=[sizes[i] for i in cr_idx],
            color=rouge, opacity=0.90,
            line=dict(width=1, color="rgba(255,255,255,0.3)"),
        ),
        hovertemplate="%{text}<extra></extra>",
    ))
    fig_map.add_trace(go.Scattergeo(
        lat=[lats[i] for i in sf_idx],
        lon=[lons[i] for i in sf_idx],
        text=[f"<b>Node: {names[i]}</b><br>{risks[i]}% Risk" for i in sf_idx],
        mode="markers",
        name="Signal Faible",
        marker=dict(
            size=[sizes[i] for i in sf_idx],
            color=prim, opacity=0.75,
            line=dict(width=1, color="rgba(255,255,255,0.2)"),
        ),
        hovertemplate="%{text}<extra></extra>",
    ))
    fig_map.update_layout(
        height=380,
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False,
        font=dict(color=pfont, family="Inter"),
        geo=dict(
            projection_type="natural earth",
            bgcolor="rgba(0,0,0,0)",
            landcolor=land_c,
            oceancolor=ocean_c,
            showocean=True, showland=True,
            showcountries=True, countrycolor=ctry_c,
            showcoastlines=True, coastlinecolor=coast_c,
            showframe=False,
        ),
    )

    st.markdown(f"""
    <div class='card' style='padding-bottom:8px'>
        <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:8px'>
            <div>
                <div style='font-size:11px;font-weight:700;color:{t['txt3']};text-transform:uppercase;letter-spacing:1px;display:flex;align-items:center;gap:6px'>
                    <i class="fa-solid fa-map-location-dot" style="color:{t['primaire']}"></i>
                    CARTOGRAPHIE DES POINTS CHAUDS
                </div>
                <div style='font-size:12px;color:{t['txt2']};margin-top:2px'>Zones de haute vélocité de transaction suspecte</div>
            </div>
            <div style='display:flex;gap:12px'>
                <div style='display:flex;align-items:center;gap:4px'>
                    <div style='width:8px;height:8px;border-radius:50%;background:{t["rouge"]}'></div>
                    <span style='font-size:11px;color:{t["txt2"]}'>Risque Critique</span>
                </div>
                <div style='display:flex;align-items:center;gap:4px'>
                    <div style='width:8px;height:8px;border-radius:50%;background:{t["primaire"]}'></div>
                    <span style='font-size:11px;color:{t["txt2"]}'>Signal Faible</span>
                </div>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)
    st.plotly_chart(fig_map, use_container_width=True, config={"displayModeBar": False})

with col_units:
    region_f   = df_fraude.groupby("region").agg(
        count=("fraude", "count"),
        montant=("montant_transaction", "mean")
    ).reset_index()
    top_region = region_f.nlargest(2, "count")
    unites = [
        (t['rouge'], "URGENT", top_region.iloc[0]["region"],
         f"Fraudes massives — {top_region.iloc[0]['region']}",
         f"{top_region.iloc[0]['count']:,} cas",
         f"Montant moyen: {top_region.iloc[0]['montant']:,.0f} FCFA"),
        (t['primaire'], "ANALYSING", top_region.iloc[1]["region"],
         f"Activité suspecte — {top_region.iloc[1]['region']}",
         f"{top_region.iloc[1]['count']:,} cas",
         f"Montant moyen: {top_region.iloc[1]['montant']:,.0f} FCFA"),
    ]

    units_parts = []
    for c, badge, _, titre, sous, detail in unites:
        badge_icon = "fa-circle-exclamation" if badge == "URGENT" else "fa-circle-dot"
        units_parts.append(
            f"<div style='padding:14px;border-radius:10px;border:1px solid {c}44;"
            f"background:{c}0D;margin-bottom:10px'>"
            f"<div style='display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px'>"
            f"<span style='background:{c}22;color:{c};padding:2px 8px;border-radius:4px;"
            f"font-size:10px;font-weight:700;letter-spacing:0.5px;display:flex;align-items:center;gap:4px'>"
            f'<i class="fa-solid {badge_icon}" style="font-size:9px"></i>'
            f"{badge}"
            f"</span>"
            f"</div>"
            f"<div style='font-size:13px;font-weight:700;color:{t['txt1']};margin-bottom:4px'>{titre}</div>"
            f"<div style='font-size:12px;color:{t['txt2']};margin-bottom:8px'>{sous}</div>"
            f"<div style='font-size:11px;color:{t['txt3']};display:flex;align-items:center;gap:4px'>"
            f'<i class="fa-solid fa-coins" style="font-size:10px"></i> {detail}'
            f"</div>"
            f"</div>"
        )
    units_html = "".join(units_parts)

    st.markdown(f"""
    <div class='card' style='height:100%'>
        <div style='font-size:11px;font-weight:700;color:{t['txt3']};text-transform:uppercase;
                    letter-spacing:1px;margin-bottom:16px;display:flex;align-items:center;gap:6px'>
            <i class="fa-solid fa-shield-halved" style="color:{t['primaire']}"></i>
            UNITÉS DE FRAUDE ACTIVES
        </div>
        {units_html}
        <div style='text-align:center;margin-top:10px'>
            <span style='font-size:12px;color:{t['primaire']};font-weight:600;cursor:pointer'>
                Voir toutes les unités
                <i class="fa-solid fa-arrow-right" style="margin-left:4px;font-size:10px"></i>
            </span>
        </div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Matrice des archétypes ────────────────────────────────────
st.markdown(f"""
<div style='font-size:11px;font-weight:700;color:{t['txt3']};text-transform:uppercase;
            letter-spacing:1px;margin-bottom:12px;display:flex;align-items:center;gap:6px'>
    <i class="fa-solid fa-sitemap" style="color:{t['primaire']}"></i>
    MATRICE DE SEGMENTATION DES ARCHÉTYPES
</div>""", unsafe_allow_html=True)

# Compute archetype segments from real data
top10_montant  = df_fraude["montant_transaction"].quantile(0.90)
shadow_ghost   = df_fraude[df_fraude["montant_transaction"] >= top10_montant]
credible_sleep = df_fraude[(df_fraude["score_credit"] >= df_fraude["score_credit"].median()) &
                            (df_fraude["montant_transaction"] < top10_montant)]
synthetic_hyb  = df_fraude[~df_fraude.index.isin(shadow_ghost.index) &
                            ~df_fraude.index.isin(credible_sleep.index)]

archetypes = [
    ("fa-solid fa-eye-slash",  "Shadow Ghost",    t['rouge'], "CRITIQUE",
     f"Comptes à hauts montants (>{top10_montant:,.0f} FCFA). Profil d'attaque évanescent.",
     f"{len(shadow_ghost)}/{len(df_fraude)}",
     f"+{100*len(shadow_ghost)//max(1,len(df_fraude))}%"),
    ("fa-solid fa-moon",       "Credible Sleeper", t['orange'], "MODÉRÉE",
     "Utilisateurs avec historique légitime effectuant des micro-transactions de test.",
     f"{len(credible_sleep)}/{len(df_fraude)}",
     f"-3.5%"),
    ("fa-solid fa-shuffle",    "Synthetic Hybrid", t['primaire'], "ÉLEVÉE",
     "Profils mixtes combinant score de crédit moyen et comportements atypiques.",
     f"{len(synthetic_hyb)}/{len(df_fraude)}",
     f"+{100*len(synthetic_hyb)//max(1,len(df_fraude))}%"),
]

arch_cols = st.columns(3, gap="medium")
for col, (icn, nom, couleur, sev, desc, occ, delta) in zip(arch_cols, archetypes):
    with col:
        st.markdown(f"""
        <div class='card'>
            <div style='display:flex;align-items:center;gap:10px;margin-bottom:12px'>
                <div style='width:36px;height:36px;background:{couleur}22;border-radius:8px;
                            display:flex;align-items:center;justify-content:center'>
                    <i class="{icn}" style="color:{couleur};font-size:17px"></i>
                </div>
                <div>
                    <div style='font-size:14px;font-weight:700;color:{t['txt1']}'>{nom}</div>
                    <div style='font-size:11px;font-weight:600;color:{couleur}'>Sévérité: {sev}</div>
                </div>
            </div>
            <div style='font-size:12px;color:{t['txt2']};line-height:1.5;margin-bottom:14px'>{desc}</div>
            <div style='display:flex;gap:20px;padding-top:12px;border-top:1px solid {t['bordure']}'>
                <div>
                    <div style='font-size:10px;color:{t['txt3']};text-transform:uppercase;letter-spacing:0.5px;margin-bottom:2px'>Score de Fraude</div>
                    <div style='font-size:13px;font-weight:700;color:{t['primaire']}'>{occ}</div>
                </div>
                <div>
                    <div style='font-size:10px;color:{t['txt3']};text-transform:uppercase;letter-spacing:0.5px;margin-bottom:2px'>Occurrence</div>
                    <div style='font-size:13px;font-weight:700;color:{couleur}'>{delta}</div>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Ciblage réseaux bancaires + Recommandation ───────────────
col_rzo, col_rec = st.columns([3, 2], gap="medium")

with col_rzo:
    carte_stats = df_fraude.groupby("type_carte").agg(
        count=("fraude", "count"),
        montant=("montant_transaction", "sum")
    ).reset_index().sort_values("montant", ascending=False)
    max_m = carte_stats["montant"].max()

    rzo_rows = "".join(
        f"<div style='padding:12px 0;border-bottom:1px solid {t['bordure']}'>"
        f"<div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:6px'>"
        f"<span style='font-size:13px;font-weight:600;color:{t['txt1']};display:flex;align-items:center;gap:6px'>"
        f'<i class="fa-solid fa-credit-card" style="color:{t["primaire"]};font-size:11px"></i>'
        f"{row['type_carte']}"
        f"</span>"
        f"<span style='font-size:13px;font-weight:700;color:{t['txt2']}'>{row['montant']/1e6:.1f}M FCFA"
        f"<span style='font-size:11px;color:{t['txt3']}'>({int(row['count']/len(df_fraude)*100)}%)</span>"
        f"</span>"
        f"</div>"
        f"<div style='background:{t['bordure']};border-radius:4px;height:6px'>"
        f"<div style='width:{int(row['montant']/max_m*100)}%;height:100%;"
        f"background:{t['primaire']};border-radius:4px'></div>"
        f"</div>"
        f"</div>"
        for _, row in carte_stats.iterrows()
    )

    st.markdown(f"""
    <div class='card'>
        <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:16px'>
            <div>
                <div style='font-size:11px;font-weight:700;color:{t['txt3']};text-transform:uppercase;letter-spacing:1px;display:flex;align-items:center;gap:6px'>
                    <i class="fa-solid fa-network-wired" style="color:{t['primaire']}"></i>
                    CIBLAGE DES RÉSEAUX BANCAIRES
                </div>
                <div style='font-size:12px;color:{t['txt2']};margin-top:2px'>Volume d'attaques par type de carte</div>
            </div>
            <span style='background:{t['bgsub']};border:1px solid {t['bordure']};padding:5px 12px;
                        border-radius:6px;font-size:11px;color:{t['txt2']};cursor:pointer;display:flex;align-items:center;gap:4px'>
                <i class="fa-regular fa-calendar" style="font-size:10px"></i> 30 derniers jours
            </span>
        </div>
        {rzo_rows}
    </div>""", unsafe_allow_html=True)

with col_rec:
    top_carte = carte_stats.iloc[0]["type_carte"] if len(carte_stats) > 0 else "Premium"
    st.markdown(f"""
    <div style='background:linear-gradient(135deg,{t["primaire"]},{t["rouge"]}44);
                border-radius:14px;padding:24px;height:100%;
                border:1px solid {t["primaire"]}44'>
        <div style='margin-bottom:10px'>
            <i class="fa-solid fa-star" style="color:white;font-size:20px;opacity:0.9"></i>
        </div>
        <div style='font-size:12px;font-weight:700;color:white;text-transform:uppercase;
                    letter-spacing:1px;margin-bottom:10px;opacity:0.8'>Recommandation Stratégique</div>
        <div style='font-size:13px;color:white;line-height:1.6;margin-bottom:20px'>
            Le réseau a détecté un pivot tactique vers les cartes
            <strong>{top_carte}</strong>. Il est recommandé de renforcer les protocoles
            de vérification sur les transactions &gt; 500k FCFA immédiatement.
        </div>
        <div style='display:flex;gap:10px'>
            <span style='background:white;color:{t["primaire"]};padding:8px 16px;border-radius:8px;
                        font-size:12px;font-weight:700;cursor:pointer;display:flex;align-items:center;gap:6px'>
                <i class="fa-solid fa-bolt" style="font-size:11px"></i> Appliquer le Patch
            </span>
            <span style='background:rgba(255,255,255,0.15);color:white;padding:8px 16px;
                        border-radius:8px;font-size:12px;font-weight:600;cursor:pointer;
                        border:1px solid rgba(255,255,255,0.3);display:flex;align-items:center;gap:6px'>
                <i class="fa-solid fa-circle-info" style="font-size:11px"></i> Détails de la Menace
            </span>
        </div>
    </div>""", unsafe_allow_html=True)
