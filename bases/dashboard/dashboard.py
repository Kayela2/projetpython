# ===== IMPORTATIONS =====
import streamlit as st        # Framework pour créer l'interface web
import numpy as np            # Bibliothèque pour calculs numériques
import pandas as pd           # Bibliothèque pour manipulation de données
import matplotlib.pyplot as plt  # Bibliothèque pour créer des graphiques
import seaborn as sns         # Bibliothèque pour graphiques statistiques avancés

# ===== CHARGEMENT DES DONNÉES =====
# Charge le fichier CSV contenant les données bancaires
df = pd.read_csv("bases\\dashboard\\bank.csv")

# ===== CONFIGURATION DE LA PAGE =====
# Configure les paramètres de la page (titre, icône, largeur)
st.set_page_config(page_title="Real time Science Dashboard", page_icon=":bar_chart:", layout="wide")

# Affiche le titre principal
st.title("Real Time/Live DataAnalysisi")

# ===== FILTRE DES DONNÉES =====
# Crée une liste déroulante pour sélectionner un métier
# pd.unique(df["job"]) retourne les valeurs uniques de la colonne "job"
job_filter = st.selectbox("Select Job", pd.unique(df["job"]))

# Filtre le DataFrame pour ne garder que les lignes où le métier correspond à la sélection
df = df[df["job"] == job_filter]

# ===== CALCUL DES INDICATEURS (KPI) =====
# Calcule l'âge moyen
avg_age = np.mean(df["age"])

# Compte le nombre de personnes mariées
count_married = int(df[df["marital"] == "married"]["marital"].count())

# Calcule le solde moyen
balance = np.mean(df["balance"])

# ===== AFFICHAGE DES KPI =====
# Crée 3 colonnes pour afficher les indicateurs côte à côte
kpi1, kpi2, kpi3 = st.columns(3)

# Affiche l'âge moyen
kpi1.metric(label="Age", value=round(avg_age), delta=round(avg_age))

# Affiche le nombre de personnes mariées
kpi2.metric(label="Married Count", value=int(count_married), delta=round(count_married))

# Affiche le solde moyen au format monétaire
kpi3.metric(label="Balance $", value=f"${round(balance, 2)}")

# ===== GRAPHIQUES =====
# Crée 2 colonnes pour les graphiques
col1, col2 = st.columns(2)

# Premier graphique: Histogramme en barre
with col1 : 
    st.markdown("### FIRST CHART")
    fig1 = plt.figure()  # Crée une nouvelle figure
    # Graphique en barres: état civil (X) vs âge (Y)
    sns.barplot(data=df, x="marital", y="age",palette="viridis")
    st.pyplot(fig1)  # Affiche le graphique

# Deuxième graphique: Histogramme des âges
with col2 :
    st.markdown("### SECOND CHART")
    fig2 = plt.figure()  # Crée une nouvelle figure
    # Histogramme: distribution des âges
    sns.histplot(data=df,x="age")
    st.pyplot(fig2)  # Affiche le graphique

# ===== AFFICHAGE DES DONNÉES FILTRÉES =====
# Affiche le titre de la section
st.markdown("### DETAILLED DATA VIEW")

# Affiche le DataFrame sous forme de tableau interactif
st.dataframe(df)