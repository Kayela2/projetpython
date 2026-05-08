# Importation de Streamlit
import streamlit as st

# Affiche un titre centré en HTML personnalisé
st.markdown("<h1 style='text-align: center;'> USER REGISTRATION </h1>", unsafe_allow_html=True)

# ===== FORMULAIRE D'INSCRIPTION =====
# Crée un formulaire qui envoie les données au clic du bouton
with st.form("Formulaire"):
    # Crée 2 colonnes côte à côte
    col1, col2 = st.columns(2)
    
    # Champ Prénom dans la 1ère colonne
    f_name = col1.text_input("First Name")
    
    # Champ Nom dans la 2ème colonne
    l_name = col2.text_input("Last Name")
    
    # Champ Email (largeur complète)
    email = st.text_input("Email")
    
    # Champ Mot de passe (le texte est masqué)
    password = st.text_input("Password", type="password")
    
    # Champ Confirmation du mot de passe (le texte est masqué)
    coonfirm_password = st.text_input("Confirm Password", type="password")
    
    # Crée 3 colonnes pour la date
    day,month,year = st.columns(3)
    
    # Champs pour Jour, Mois, Année
    day.text_input("Day")
    month.text_input("Month")
    year.text_input("Year")

    # Bouton pour soumettre le formulaire
    st_state = st.form_submit_button("Submit")
    
    # Vérifie si le formulaire a été soumis
    if st_state :
        # Vérifie si le prénom ET le nom sont vides
        if f_name == "" and l_name == "":
            # Affiche un message d'avertissement
            st.warning("Please fill above fields")
        else:
            # Affiche un message de succès avec les noms entrés
            st.success(f"Welcome {f_name} {l_name}")
            # Affiche des pilules (boutons non cliquables)
            st.pills("LABEL", options=("1 ","2 ","3 "))

# ===== BARRE DE NAVIGATION LATÉRALE =====
# Crée une navigation dans la barre latérale (côté droit)
p = st.sidebar.radio("Navigation", options=("Home","About","Contact"))