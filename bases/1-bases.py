# Importation des bibliothèques nécessaires
import streamlit as st  # Streamlit pour créer l'interface web
import pandas as pd     # Pandas pour manipuler les données

# Affiche le titre principal de l'application
st.title("STREAMLIT WEB APP")

# Affiche une métrique avec un delta (valeur actuelle et changement)
st.metric(label="wind speed", value="120ms-1",delta="-1.4ms-1")

# Crée un DataFrame (tableau) Pandas avec 2 colonnes et 3 lignes
tabel = pd.DataFrame({"Column1":[1,2,3], "Column2":[9,8,7]})

# Ligne commentée: affichage d'une image (désactivée)
# st.image("stream.jpg")

# ===== DÉMONSTRATION DES ÉLÉMENTS INTERACTIFS =====

# Checkbox (case à cocher) - Affiche un message selon l'état de la case
state = st.checkbox('Checbox', value=True)  # La case est cochée par défaut
if state :  # Si la case est cochée
    st.write("Box checked")     # Affiche ce message
else :      # Sinon
    st.write("Box unchecked")   # Affiche ce message

# Bouton radio pour sélectionner une option parmi plusieurs
radio_btn = st.radio("Radio Button", ("US","UK","Canada"))

# Bouton cliquable
btn = st.button("Click Me")

# Liste déroulante pour sélectionner une marque de voiture
select = st.selectbox("select box",("Audi","BMW","MUSTANG"))

# Sélection multiple pour choisir plusieurs marques de téléphones
multi_select = st.multiselect("Multibox", ('APPLE','SAMSUNG','HUAWEI','HONOR'))