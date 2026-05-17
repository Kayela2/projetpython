import streamlit as st


def get_colors(sombre: bool) -> dict:
    if sombre:
        return dict(
            bg       = "#060D20",
            bgcard   = "#0D1B3E",
            bgsub    = "#112252",
            sidebar  = "#080F28",
            bordure  = "rgba(59,130,246,0.12)",
            txt1     = "#F1F5F9",
            txt2     = "#94A3B8",
            txt3     = "#475569",
            primaire = "#3B82F6",
            rouge    = "#F87171",
            vert     = "#34D399",
            orange   = "#FBBF24",
            pbg      = "#0D1B3E",
            pfont    = "#94A3B8",
            pgrid    = "rgba(59,130,246,0.06)",
            prim_a   = "rgba(59,130,246,0.18)",
            rouge_a  = "rgba(248,113,113,0.18)",
            vert_a   = "rgba(52,211,153,0.18)",
            orange_a = "rgba(251,191,36,0.18)",
            shadow   = "0 4px 24px rgba(0,0,0,0.5)",
        )
    return dict(
        bg       = "#F8F9FF",
        bgcard   = "#FFFFFF",
        bgsub    = "#EEF0FF",
        sidebar  = "#FFFFFF",
        bordure  = "rgba(99,102,241,0.14)",
        txt1     = "#111827",
        txt2     = "#374151",
        txt3     = "#6B7280",
        primaire = "#6366F1",
        rouge    = "#EF4444",
        vert     = "#10B981",
        orange   = "#F59E0B",
        pbg      = "#FFFFFF",
        pfont    = "#4B5563",
        pgrid    = "rgba(99,102,241,0.07)",
        prim_a   = "rgba(99,102,241,0.08)",
        rouge_a  = "rgba(239,68,68,0.08)",
        vert_a   = "rgba(16,185,129,0.08)",
        orange_a = "rgba(245,158,11,0.08)",
        shadow   = "0 1px 3px rgba(0,0,0,0.05), 0 4px 16px rgba(99,102,241,0.07)",
    )


def _rgba(hex_c: str, alpha: float) -> str:
    h = hex_c.lstrip('#')
    return f"rgba({int(h[:2],16)},{int(h[2:4],16)},{int(h[4:6],16)},{alpha})"


def inject_css(t: dict) -> None:
    shd_prim  = _rgba(t['primaire'], 0.22)
    shd_rouge = _rgba(t['rouge'],   0.20)
    shd_vert  = _rgba(t['vert'],    0.20)
    shd_ora   = _rgba(t['orange'],  0.20)
    st.markdown(
        '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css" crossorigin="anonymous">',
        unsafe_allow_html=True,
    )
    st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Mono:wght@400;700&display=swap');
html, body, [class*="css"] {{ font-family: 'Inter', sans-serif !important; }}
.stApp {{ background: {t['bg']} !important; }}
.block-container {{ padding: 1.5rem 2rem !important; max-width: 100% !important; }}
[data-testid="stSidebar"] {{
    background: {t['sidebar']} !important;
    min-width: 240px !important; max-width: 240px !important;
    border-right: 1px solid {t['bordure']} !important;
}}
[data-testid="stSidebar"] * {{ color: {t['txt1']} !important; }}
h1, h2, h3 {{ color: {t['txt1']} !important; font-family: 'Inter', sans-serif !important; font-weight: 700 !important; }}
.stButton > button {{
    background: {t['primaire']} !important; color: white !important;
    border: none !important; border-radius: 8px !important;
    font-weight: 600 !important; font-size: 13px !important;
    font-family: 'Inter', sans-serif !important;
}}
.card {{
    background: {t['bgcard']}; border: 1px solid {t['bordure']};
    border-radius: 12px; padding: 20px 24px; box-shadow: {t['shadow']};
    position: relative; overflow: hidden; cursor: pointer;
    transition: transform 0.25s cubic-bezier(0.34,1.56,0.64,1),
                box-shadow 0.25s ease, border-color 0.25s ease !important;
}}
.card::before {{
    content: ''; position: absolute; top: 0; left: 0; right: 0;
    height: 3px; border-radius: 12px 12px 0 0;
    opacity: 0; transform: scaleX(0.3);
    transition: opacity 0.25s ease, transform 0.3s ease;
}}
.card::after {{
    content: ''; position: absolute; top: -50%; left: -75%;
    width: 50%; height: 200%; pointer-events: none;
    background: linear-gradient(to right, transparent, rgba(255,255,255,0.06), transparent);
    transform: skewX(-20deg); transition: left 0.6s ease;
}}
.card:hover {{ transform: translateY(-5px) !important; }}
.card:hover::before {{ opacity: 1; transform: scaleX(1); }}
.card:hover::after  {{ left: 125%; }}
.card-primary:hover  {{ box-shadow: 0 16px 40px {shd_prim}  !important; border-color: {t['primaire']}66 !important; }}
.card-danger:hover   {{ box-shadow: 0 16px 40px {shd_rouge} !important; border-color: {t['rouge']}66   !important; }}
.card-warning:hover  {{ box-shadow: 0 16px 40px {shd_ora}   !important; border-color: {t['orange']}66  !important; }}
.card-success:hover  {{ box-shadow: 0 16px 40px {shd_vert}  !important; border-color: {t['vert']}66    !important; }}
.card-primary::before  {{ background: linear-gradient(90deg, {t['primaire']}, transparent); }}
.card-danger::before   {{ background: linear-gradient(90deg, {t['rouge']},    transparent); }}
.card-warning::before  {{ background: linear-gradient(90deg, {t['orange']},   transparent); }}
.card-success::before  {{ background: linear-gradient(90deg, {t['vert']},     transparent); }}
.kpi-label {{ font-size: 11px; font-weight: 600; color: {t['txt2']}; text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 8px; }}
.kpi-value {{ font-size: 30px; font-weight: 800; color: {t['txt1']}; line-height: 1.1; margin-bottom: 4px; }}
.kpi-sub   {{ font-size: 11px; color: {t['txt3']}; margin-top: 4px; }}
.section-title {{ font-size: 12px; font-weight: 700; color: {t['txt1']}; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 16px; }}
.badge {{ display: inline-block; padding: 3px 10px; border-radius: 20px; font-size: 11px; font-weight: 600; }}
.badge-s {{ background: rgba(16,185,129,0.12);  color: {t['vert']};     border: 1px solid rgba(16,185,129,0.25); }}
.badge-d {{ background: rgba(239,68,68,0.12);    color: {t['rouge']};    border: 1px solid rgba(239,68,68,0.25); }}
.badge-w {{ background: rgba(245,158,11,0.12);   color: {t['orange']};   border: 1px solid rgba(245,158,11,0.25); }}
.badge-i {{ background: {t['prim_a']};             color: {t['primaire']}; border: 1px solid rgba(99,102,241,0.25); }}
[data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"] {{
    border-radius: 8px !important; margin-bottom: 2px !important;
    font-weight: 500 !important; font-size: 13px !important;
}}
.icon-box {{
    width: 36px; height: 36px; border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
    transition: transform 0.3s cubic-bezier(0.34,1.56,0.64,1);
}}
.card:hover .icon-box {{ transform: scale(1.18) rotate(-8deg); }}
/* Border container matches card style */
div[data-testid="stVerticalBlockBorderWrapper"] {{
    background: {t['bgcard']} !important;
    border: 1px solid {t['bordure']} !important;
    border-radius: 12px !important;
    box-shadow: {t['shadow']} !important;
    padding: 4px 8px !important;
}}
/* Period radio as pill buttons */
div[data-testid="stRadio"] > div[role="radiogroup"] {{
    flex-direction: row !important;
    gap: 4px !important;
    justify-content: flex-end;
    padding-top: 8px;
}}
div[data-testid="stRadio"] > div[role="radiogroup"] > label {{
    background: {t['bgsub']};
    border: 1px solid {t['bordure']};
    border-radius: 6px;
    padding: 4px 14px !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    color: {t['txt2']} !important;
    cursor: pointer;
    margin: 0 !important;
    transition: all 0.15s;
}}
div[data-testid="stRadio"] > div[role="radiogroup"] > label:has(input:checked) {{
    background: {t['primaire']} !important;
    color: white !important;
    border-color: {t['primaire']} !important;
}}
div[data-testid="stRadio"] > div[role="radiogroup"] > label > div:first-child {{
    display: none !important;
}}
div[data-testid="stRadio"] > label {{ display: none !important; }}
/* Page link "Voir toutes" — centré, couleur primaire */
div[data-testid="stPageLink"] a {{
    color: {t['primaire']} !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    text-decoration: none !important;
    display: flex;
    justify-content: center;
    padding: 10px 0 4px;
    gap: 6px;
}}
div[data-testid="stPageLink"] a:hover {{
    text-decoration: underline !important;
}}
/* Planisphère toggle button */
div[data-testid="stButton"]:has(button[kind="secondary"]) > button {{
    background: {t['bgcard']} !important;
    color: {t['primaire']} !important;
    border: 1px solid {t['primaire']}55 !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 12px !important;
}}
div[data-testid="stButton"]:has(button[kind="secondary"]) > button:hover {{
    background: {t['prim_a']} !important;
    border-color: {t['primaire']} !important;
}}
/* Search input */
div[data-testid="stTextInput"] {{ margin-bottom: 0 !important; }}
div[data-testid="stTextInput"] > div {{
    background: {t['bgcard']} !important;
    border: 1px solid {t['bordure']} !important;
    border-radius: 10px !important;
    box-shadow: none !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}}
div[data-testid="stTextInput"] > div:focus-within {{
    border-color: {t['primaire']} !important;
    box-shadow: 0 0 0 3px {t['prim_a']} !important;
}}
div[data-testid="stTextInput"] input {{
    background: transparent !important;
    border: none !important;
    padding: 8px 14px !important;
    font-size: 13px !important;
    color: {t['txt1']} !important;
    font-family: 'Inter', sans-serif !important;
    box-shadow: none !important;
}}
div[data-testid="stTextInput"] input::placeholder {{ color: {t['txt3']} !important; }}
div[data-testid="stTextInput"] > label {{ display: none !important; }}
/* Disabled buttons — muted, not clickable */
div[data-testid="stButton"] > button:disabled {{
    opacity: 0.38 !important;
    cursor: not-allowed !important;
}}
/* Download button — matches secondary action buttons */
div[data-testid="stDownloadButton"] > button {{
    background: {t['bgcard']} !important;
    color: {t['primaire']} !important;
    border: 1px solid {t['primaire']}55 !important;
    border-radius: 8px !important;
    font-size: 12px !important;
    font-weight: 600 !important;
}}
div[data-testid="stDownloadButton"] > button:hover {{
    background: {t['prim_a']} !important;
    border-color: {t['primaire']} !important;
}}
/* Selectbox — match card style */
div[data-testid="stSelectbox"] > div > div {{
    background: {t['bgcard']} !important;
    border: 1px solid {t['bordure']} !important;
    border-radius: 8px !important;
    font-size: 12px !important;
    color: {t['txt1']} !important;
}}
div[data-testid="stSelectbox"] > label {{ display: none !important; }}
</style>
""", unsafe_allow_html=True)


def render_sidebar(sombre: bool) -> None:
    t = get_colors(sombre)
    with st.sidebar:
        st.markdown(f"""
        <div style='padding:20px 16px 16px;border-bottom:1px solid {t['bordure']};margin-bottom:12px'>
            <div style='display:flex;align-items:center;gap:10px'>
                <div style='width:34px;height:34px;background:{t["primaire"]};border-radius:9px;
                            display:flex;align-items:center;justify-content:center;flex-shrink:0'>
                    <i class="fa-solid fa-shield-halved" style="color:white;font-size:15px"></i>
                </div>
                <div>
                    <div style='font-size:15px;font-weight:800;color:{t["txt1"]};letter-spacing:0.5px;line-height:1.1'>FraudLens</div>
                    <div style='font-size:10px;color:{t["txt2"]};margin-top:1px'>Analyse Bancaire</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.page_link("app.py",                    label="Tableau de Bord",      icon=":material/dashboard:")
        st.page_link("pages/1_exploration.py",    label="Exploration",           icon=":material/database:")
        st.page_link("pages/2_nettoyage.py",      label="Nettoyage",             icon=":material/cleaning_services:")
        st.page_link("pages/3_analyse.py",        label="Analyse Exploratoire",  icon=":material/analytics:")
        st.page_link("pages/4_visualisations.py", label="Visualisations",        icon=":material/monitoring:")
        st.page_link("pages/5_faudes.py",         label="Profil des Fraudes",    icon=":material/security:")

        st.markdown("<br><br><br>", unsafe_allow_html=True)

        if st.button("＋  Nouvelle Analyse", use_container_width=True):
            pass

        label_theme = "☀️  Mode Clair" if sombre else "🌙  Mode Sombre"
        if st.button(label_theme, use_container_width=True):
            st.session_state.mode_sombre = not sombre
            st.rerun()

        st.markdown(f"""
        <div style='margin-top:12px;padding-top:12px;border-top:1px solid {t['bordure']}'>
            <div style='display:flex;align-items:center;gap:8px;font-size:13px;color:{t["txt2"]};padding:8px 4px;cursor:pointer'>
                <i class="fa-solid fa-gear" style="font-size:12px;width:14px"></i> Paramètres
            </div>
            <div style='display:flex;align-items:center;gap:8px;font-size:13px;color:{t["rouge"]};padding:8px 4px;cursor:pointer'>
                <i class="fa-solid fa-right-from-bracket" style="font-size:12px;width:14px"></i> Déconnexion
            </div>
        </div>
        """, unsafe_allow_html=True)
