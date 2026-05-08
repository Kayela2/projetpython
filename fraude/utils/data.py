import pandas as pd
import streamlit as st

@st.cache_data
def charger_donnees():
    """
    Charge le fichier CV et retrourne deux version:
    - df_brut : donnees originales (avec valeurs manquantes)
    -df : donnees nettoyees (sans valeurs manquantes)
    """

    chemin = "data/fraude_bancaire_synthetique_final.csv"
    df_brut = pd.read_csv(chemin)

    df = df_brut.dropna().reset_index(drop=True)
    df["fraude"] = df["fraude"].astype(int)
    df["fraude_label"] = df["fraude"].map({0: "Légitime", 1: "Fraude"})

    return df_brut, df

def get_stas(df):
    """
    Calcule les statistiques clés du dataset pour l'affichage rapide dans le dashboard
    """
    return {
        "total":       len(df),
        "nb_fraudes":  int(df["fraude"].sum()),
        "nb_legitimes": int((df["fraude"]== 0).sum()),
        "taux_fraude": round(df["fraude"].mean() * 100, 2),
        "montant_moy": round(df["montant_transaction"].mean(), 2),
        "montant_max": round(df["montant_transaction"].max(), 2),
        "score_moy":   round(df["score_credit"].mean(), 2),
        "age_moy":     round(df["age"].mean(), 1),
        "salaire_moy": round(df["salaire"].mean(), 2),
    }