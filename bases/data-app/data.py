# ===== IMPORTATIONS =====
import streamlit as st        # Framework pour créer l'interface web
import numpy as np            # Bibliothèque pour calculs numériques
import pandas as pd           # Bibliothèque pour manipulation de données
import matplotlib.pyplot as plt  # Bibliothèque pour créer des graphiques
import seaborn as sns         # Bibliothèque pour graphiques statistiques

# ===== TITRE DE L'APPLICATION =====
st.title("Upload file")

# ===== SECTION D'UPLOAD =====
# Affiche le titre de la section
st.subheader("Input csv")

# Crée un widget pour télécharger un fichier CSV
# L'utilisateur peut sélectionner un fichier avec l'extension .csv
uploaded_file = st.file_uploader("Choose a file", type="csv")

# ===== TRAITEMENT ET AFFICHAGE DES DONNÉES =====
# Vérifie si un fichier a été uploadé
if uploaded_file:
    # Charge le fichier CSV dans un DataFrame Pandas
    df = pd.read_csv(uploaded_file)
    
    # Affiche le titre de la section data
    st.subheader("Dataframe")
    
    # Affiche le tableau complet des données
    st.write(df)
    
    # Crée 2 colonnes pour afficher les graphiques côte à côte
    col1, col2 = st.columns(2)
    
    # Premier graphique dans la colonne 1
    with col1:
        fig1 = plt.figure()  # Crée une nouvelle figure
        # Graphique de dispersion: Salaire estimé (X) vs Âge (Y)
        # Les points sont colorés selon la colonne "Purchased" (achat ou non)
        sns.scatterplot(data=df,x='EstimatedSalary',y='Age',hue='Purchased')
        # REMARQUE: st.pyplot(fig1) est manquant ici (bug dans le code original)
    
    # Deuxième graphique dans la colonne 2
    with col2:
        fig2 = plt.figure()  # Crée une nouvelle figure
        # Affiche le titre de ce graphique
        st.subheader("Distribution of Age")
        # Histogramme: distribution des âges (nombre de personnes par tranche d'âge)
        sns.histplot(df.Age)
        # Affiche le graphique
        st.pyplot(fig2)