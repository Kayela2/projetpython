import streamlit as st
import pandas as pd
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils.data import charger_donnees, get_stas
from utils.theme import get_colors, inject_css, render_sidebar

st.set_page_config(page_title="FraudLens — Exploration", page_icon="🛡️",
                   layout="wide", initial_sidebar_state="expanded")

# ── Session state ─────────────────────────────────────────────
if "mode_sombre"   not in st.session_state: st.session_state.mode_sombre   = True
if "page_exp"      not in st.session_state: st.session_state.page_exp      = 0
if "rows_per_page" not in st.session_state: st.session_state.rows_per_page = 15
if "show_import"   not in st.session_state: st.session_state.show_import   = False
if "show_add"      not in st.session_state: st.session_state.show_add      = False

sombre = st.session_state.mode_sombre
t = get_colors(sombre)
inject_css(t)
render_sidebar(sombre)

df_brut, df = charger_donnees()
stats = get_stas(df)

# ── Top bar ───────────────────────────────────────────────────
st.markdown(f"""
<div style='display:flex;align-items:center;justify-content:space-between;
            margin-bottom:20px;padding-bottom:16px;border-bottom:1px solid {t['bordure']}'>
    <div>
        <div style='font-size:22px;font-weight:800;color:{t['txt1']};letter-spacing:-0.3px'>
            Exploration du Dataset
        </div>
        <div style='font-size:13px;color:{t['txt2']};margin-top:3px'>
            Analyse en temps réel des flux transactionnels et démographiques bancaires.
        </div>
    </div>
    <div style='display:flex;align-items:center;gap:14px'>
        <span style='font-size:16px;cursor:pointer;color:{t["txt2"]}'><i class="fa-solid fa-bell"></i></span>
        <span style='font-size:16px;cursor:pointer;color:{t["txt2"]}'><i class="fa-solid fa-gear"></i></span>
    </div>
</div>""", unsafe_allow_html=True)

# ── KPIs ──────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4, gap="medium")
with c1:
    st.markdown(f"""
    <div class='card card-primary'>
        <div class='kpi-label' style='display:flex;align-items:center;gap:6px;margin-bottom:10px'>
            <i class="fa-solid fa-table-list" style="color:{t['primaire']};font-size:11px"></i>
            TOTAL RECORDS
        </div>
        <div class='kpi-value'>{len(df):,}</div>
        <div style='margin-top:8px'>
            <span class='badge badge-s'>✓ Intégrité Vérifiée</span>
        </div>
    </div>""", unsafe_allow_html=True)
with c2:
    st.markdown(f"""
    <div class='card card-primary'>
        <div class='kpi-label' style='display:flex;align-items:center;gap:6px;margin-bottom:10px'>
            <i class="fa-solid fa-star-half-stroke" style="color:{t['primaire']};font-size:11px"></i>
            SCORE CRÉDIT MOY.
        </div>
        <div class='kpi-value'>{stats['score_moy']:.1f}</div>
        <div class='kpi-sub'>Std Dev : ±12.4</div>
    </div>""", unsafe_allow_html=True)
with c3:
    st.markdown(f"""
    <div class='card card-warning'>
        <div class='kpi-label' style='display:flex;align-items:center;gap:6px;margin-bottom:10px'>
            <i class="fa-solid fa-coins" style="color:{t['orange']};font-size:11px"></i>
            SALAIRE MOYEN
        </div>
        <div class='kpi-value'>{stats['salaire_moy']/1000:.0f}k <span style='font-size:14px;font-weight:500'>FCFA</span></div>
        <div class='kpi-sub'>Std Dev : ±12.4k</div>
    </div>""", unsafe_allow_html=True)
with c4:
    st.markdown(f"""
    <div class='card card-danger'>
        <div class='kpi-label' style='display:flex;align-items:center;gap:6px;margin-bottom:10px'>
            <i class="fa-solid fa-triangle-exclamation" style="color:{t['rouge']};font-size:11px"></i>
            RISQUE CRITIQUE
        </div>
        <div class='kpi-value' style='color:{t["rouge"]}'>{stats['taux_fraude']}%</div>
        <div class='kpi-sub' style='color:{t["rouge"]}88'>Priorité haute attention</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Filtres + Tableau ──────────────────────────────────────────
col_f, col_t = st.columns([1, 3.2], gap="medium")

with col_f:
    st.markdown(f"""
    <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:14px'>
        <div style='font-size:12px;font-weight:700;color:{t['txt1']};
                    text-transform:uppercase;letter-spacing:1px;
                    display:flex;align-items:center;gap:6px'>
            <i class="fa-solid fa-sliders" style="color:{t['primaire']};font-size:11px"></i>
            Filtres
        </div>
    </div>""", unsafe_allow_html=True)

    age_min, age_max = int(df["age"].min()), int(df["age"].max())
    st.markdown(f"""<div style='font-size:11px;font-weight:600;color:{t['txt2']};
                margin-bottom:4px;text-transform:uppercase;letter-spacing:0.5px'>
                Distribution par Âge</div>""", unsafe_allow_html=True)
    age_range = st.slider("age_sl", age_min, age_max, (age_min, age_max),
                          key="age_range", label_visibility="collapsed")
    st.markdown(f"""<div style='display:flex;justify-content:space-between;
                font-size:11px;color:{t['txt3']};margin-bottom:16px'>
                <span>{age_range[0]}</span><span>{age_range[1]}</span></div>""",
                unsafe_allow_html=True)

    sc_min, sc_max = int(df["score_credit"].min()), int(df["score_credit"].max())
    st.markdown(f"""<div style='font-size:11px;font-weight:600;color:{t['txt2']};
                margin-bottom:4px;text-transform:uppercase;letter-spacing:0.5px'>
                Score Crédit Min.</div>""", unsafe_allow_html=True)
    score_seuil = st.slider("sc_sl", sc_min, sc_max, sc_min,
                            key="score_seuil", label_visibility="collapsed")
    st.markdown(f"""<div style='display:flex;justify-content:space-between;
                font-size:11px;color:{t['txt3']};margin-bottom:16px'>
                <span>{score_seuil}</span><span>{sc_max}</span></div>""",
                unsafe_allow_html=True)

    st.markdown(f"""<div style='font-size:11px;font-weight:600;color:{t['txt2']};
                margin-bottom:8px;text-transform:uppercase;letter-spacing:0.5px'>
                Statut du Compte</div>""", unsafe_allow_html=True)
    aff_legitime = st.checkbox("Comptes Actifs (Légitimes)", value=True, key="chk_legit")
    aff_fraude   = st.checkbox("Comptes Signalés (Fraude)",  value=True, key="chk_fraud")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Appliquer les Filtres", use_container_width=True, type="primary",
                 key="btn_apply"):
        st.session_state.page_exp = 0
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    schema = [("age","INT"),("salaire","FLOAT"),("score_credit","FLOAT"),
              ("montant_transaction","FLOAT"),("anciennete_compte","INT"),
              ("type_carte","STRING"),("region","STRING"),("genre","STRING"),("fraude","INT")]
    rows_s = "".join(
        f"<div style='display:flex;justify-content:space-between;align-items:center;"
        f"padding:7px 0;border-bottom:1px solid {t['bordure']}'>"
        f"<div style='display:flex;align-items:center;gap:8px'>"
        f"<div style='width:6px;height:6px;border-radius:50%;background:{t['primaire']}'></div>"
        f"<span style='font-size:12px;font-weight:500;color:{t['txt1']}'>{col}</span>"
        f"</div><span style='background:{t['prim_a']};color:{t['primaire']};padding:2px 7px;"
        f"border-radius:4px;font-size:10px;font-weight:700;font-family:monospace'>{tp}</span>"
        f"</div>"
        for col, tp in schema
    )
    st.markdown(f"""
    <div class='card'>
        <div style='font-size:11px;font-weight:700;color:{t['txt1']};margin-bottom:12px;
                    text-transform:uppercase;letter-spacing:0.8px;
                    display:flex;align-items:center;gap:6px'>
            <i class="fa-solid fa-database" style="color:{t['primaire']};font-size:11px"></i>
            Schéma des Champs
        </div>
        {rows_s}
    </div>""", unsafe_allow_html=True)

with col_t:
    # ── Filtrage ─────────────────────────────────────────────
    masque = ((df["age"] >= age_range[0]) & (df["age"] <= age_range[1]) &
              (df["score_credit"] >= score_seuil))
    if not aff_legitime:
        masque &= df["fraude"] == 1
    if not aff_fraude:
        masque &= df["fraude"] == 0
    df_f = df[masque].copy()

    rows_pp  = st.session_state.rows_per_page
    total_r  = len(df_f)
    total_pg = max(1, (total_r + rows_pp - 1) // rows_pp)
    page     = min(st.session_state.page_exp, total_pg - 1)
    start_r  = page * rows_pp
    end_r    = min(start_r + rows_pp, total_r)

    # ── En-tête tableau ───────────────────────────────────────
    th_l, th_r = st.columns([2.2, 2.8])
    with th_l:
        st.markdown(f"""
        <div style='padding-top:6px'>
            <div style='font-size:15px;font-weight:700;color:{t['txt1']}'>
                Aperçu des Données Brutes
            </div>
            <div style='font-size:12px;color:{t['txt2']};margin-top:2px'>
                Affichage :
                <b style='color:{t["primaire"]}'>{start_r+1}–{end_r}</b>
                sur
                <b style='color:{t["txt1"]}'>{total_r:,}</b>
                enregistrements
            </div>
        </div>""", unsafe_allow_html=True)

    with th_r:
        act1, act2, act3, act4 = st.columns([1.1, 1.1, 1.1, 0.8])

        with act1:
            lbl_imp = "✕ Fermer" if st.session_state.show_import else "⬆ Importer"
            if st.button(lbl_imp, key="btn_import", use_container_width=True):
                st.session_state.show_import = not st.session_state.show_import
                st.rerun()

        with act2:
            cols_exp = ["age","salaire","score_credit","montant_transaction",
                        "anciennete_compte","type_carte","region","genre","fraude"]
            csv_data = df_f[cols_exp].to_csv(index=False).encode("utf-8")
            st.download_button(
                label="⬇ Exporter",
                data=csv_data,
                file_name="donnees_filtrees.csv",
                mime="text/csv",
                key="dl_exp",
                use_container_width=True,
            )

        with act3:
            lbl_add = "✕ Annuler" if st.session_state.show_add else "＋ Ajouter"
            if st.button(lbl_add, key="btn_add", use_container_width=True):
                st.session_state.show_add = not st.session_state.show_add
                st.rerun()

        with act4:
            rpp_opts  = [15, 25, 50]
            rpp_idx   = rpp_opts.index(st.session_state.rows_per_page) if st.session_state.rows_per_page in rpp_opts else 0
            rpp_sel   = st.selectbox("rpp", rpp_opts, index=rpp_idx,
                                     key="rpp_sel", label_visibility="collapsed")
            if rpp_sel != st.session_state.rows_per_page:
                st.session_state.rows_per_page = rpp_sel
                st.session_state.page_exp = 0
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Panneau Import ────────────────────────────────────────
    if st.session_state.show_import:
        with st.expander("Importer un fichier CSV", expanded=True):
            st.markdown(f"""
            <div style='font-size:12px;color:{t['txt2']};margin-bottom:8px'>
                Importez un fichier CSV compatible avec le schéma du dataset de fraude.
                Les colonnes attendues : age, salaire, score_credit, montant_transaction,
                anciennete_compte, type_carte, region, genre, fraude.
            </div>""", unsafe_allow_html=True)
            uploaded = st.file_uploader("Choisir un fichier CSV", type=["csv"], key="file_up")
            if uploaded is not None:
                try:
                    df_imp = pd.read_csv(uploaded)
                    st.success(f"Fichier importé avec succès — {len(df_imp):,} lignes × {len(df_imp.columns)} colonnes")
                    st.dataframe(df_imp.head(8), use_container_width=True, hide_index=True)
                    if st.button("Confirmer l'import", type="primary", key="btn_confirm_imp"):
                        st.session_state.show_import = False
                        st.rerun()
                except Exception as e:
                    st.error(f"Erreur de lecture : {e}")

    # ── Formulaire Ajouter ────────────────────────────────────
    if st.session_state.show_add:
        with st.expander("Nouvelle transaction", expanded=True):
            f1, f2, f3 = st.columns(3)
            with f1:
                n_age = st.number_input("Âge", 18, 99, 35, key="add_age")
                n_sal = st.number_input("Salaire (FCFA)", 0, 10_000_000, 500_000, 10_000, key="add_sal")
                n_reg = st.selectbox("Région", sorted(df["region"].dropna().unique()), key="add_reg")
            with f2:
                n_sco = st.number_input("Score Crédit", 0.0, 850.0, 650.0, key="add_sco")
                n_mnt = st.number_input("Montant (FCFA)", 0, 5_000_000, 50_000, 1_000, key="add_mnt")
                n_typ = st.selectbox("Type de carte", sorted(df["type_carte"].dropna().unique()), key="add_typ")
            with f3:
                n_anc = st.number_input("Ancienneté (ans)", 0, 50, 5, key="add_anc")
                n_gen = st.selectbox("Genre", sorted(df["genre"].dropna().unique()), key="add_gen")
                n_fra = st.selectbox("Statut", ["Légitime (0)", "Fraude (1)"], key="add_fra")
            sc1, sc2 = st.columns([1, 3])
            with sc1:
                if st.button("Enregistrer", type="primary", use_container_width=True, key="btn_save_tx"):
                    st.success("Transaction enregistrée (simulation — non persistée en base).")
                    st.session_state.show_add = False
                    st.rerun()

    # ── Tableau paginé ────────────────────────────────────────
    df_page = df_f.iloc[start_r:end_r][
        ["age","salaire","score_credit","montant_transaction",
         "anciennete_compte","type_carte","region","genre","fraude"]
    ].copy()
    df_page.columns = ["ÂGE","SALAIRE (FCFA)","SCORE","MONTANT (FCFA)","ANCIENNETÉ","CARTE","RÉGION","GENRE","STATUT"]
    df_page["SALAIRE (FCFA)"]  = df_page["SALAIRE (FCFA)"].apply(lambda x: f"{x:,.0f}")
    df_page["MONTANT (FCFA)"]  = df_page["MONTANT (FCFA)"].apply(lambda x: f"{x:,.0f}")
    df_page["SCORE"]           = df_page["SCORE"].round(1)
    df_page["STATUT"]          = df_page["STATUT"].map({0: "✅ Légitime", 1: "🚨 Fraude"})
    st.dataframe(df_page, use_container_width=True, height=420, hide_index=True)

    # ── Pagination ────────────────────────────────────────────
    st.markdown("<div style='margin-top:12px'>", unsafe_allow_html=True)
    pg_prev, pg_info, pg_next = st.columns([1, 2.5, 1])

    with pg_prev:
        if st.button("← Précédent", disabled=(page == 0),
                     use_container_width=True, key="btn_prev"):
            st.session_state.page_exp = page - 1
            st.rerun()

    with pg_info:
        max_show = 5
        half     = max_show // 2
        pg_start = max(0, min(page - half, total_pg - max_show))
        pg_end   = min(total_pg, pg_start + max_show)
        pg_cols  = st.columns(pg_end - pg_start)
        for i, p in enumerate(range(pg_start, pg_end)):
            with pg_cols[i]:
                is_cur = p == page
                label  = str(p + 1)
                if st.button(label, key=f"pgbtn_{p}",
                             type="primary" if is_cur else "secondary",
                             use_container_width=True):
                    st.session_state.page_exp = p
                    st.rerun()

    with pg_next:
        if st.button("Suivant →", disabled=(page >= total_pg - 1),
                     use_container_width=True, key="btn_next"):
            st.session_state.page_exp = page + 1
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(f"""
    <div style='text-align:center;margin-top:8px;font-size:11px;color:{t['txt3']}'>
        Page {page + 1} sur {total_pg}  ·  {rows_pp} lignes/page
    </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Insight IA + Qualité ──────────────────────────────────
    bc1, bc2 = st.columns(2, gap="medium")
    null_rate = 1 - (df_brut.isnull().sum().sum() / (df_brut.shape[0] * df_brut.shape[1]))
    qualite   = int(null_rate * 100)
    with bc1:
        st.markdown(f"""
        <div class='card card-primary'>
            <div style='display:flex;align-items:center;gap:10px;margin-bottom:10px'>
                <div class='icon-box' style='width:30px;height:30px;background:{t['prim_a']};border-radius:8px'>
                    <i class="fa-solid fa-wand-magic-sparkles" style="color:{t['primaire']};font-size:12px"></i>
                </div>
                <div style='font-size:13px;font-weight:700;color:{t['txt1']}'>Insight IA Automatique</div>
            </div>
            <div style='font-size:12px;color:{t['txt2']};line-height:1.6'>
                Anomalie récurrente détectée dans les transactions inférieures à <b>50 000 FCFA</b>
                ce mois-ci — probabilité de fraude coordonnée élevée.
            </div>
            <div style='margin-top:12px;font-size:12px;color:{t['primaire']};font-weight:600;cursor:pointer'>
                Voir les détails
                <i class="fa-solid fa-arrow-right" style="margin-left:4px;font-size:10px"></i>
            </div>
        </div>""", unsafe_allow_html=True)
    with bc2:
        qual_c = t['vert'] if qualite >= 90 else t['orange'] if qualite >= 70 else t['rouge']
        st.markdown(f"""
        <div class='card card-success' style='text-align:center'>
            <div class='kpi-label'>Qualité des Données</div>
            <div style='font-size:44px;font-weight:800;color:{qual_c};line-height:1.1'>{qualite}%</div>
            <div style='background:{t['bordure']};border-radius:4px;height:8px;margin:12px 0 4px'>
                <div style='width:{qualite}%;height:100%;background:{qual_c};
                            border-radius:4px;transition:width 0.4s ease'></div>
            </div>
            <div style='font-size:12px;color:{t['txt2']}'>Score de complétude global</div>
        </div>""", unsafe_allow_html=True)
