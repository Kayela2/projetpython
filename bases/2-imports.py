# Importation de Streamlit pour créer l'interface web
import streamlit as st

# Affiche le titre de la page
st.title('Uploading file')

# ===== SECTION UPLOAD D'IMAGES =====
# Permet à l'utilisateur d'uploader une image (formats .png ou .jpg)
image = st.file_uploader("** PLEASE UPLOAD AN IMAGE", type=['png','jpg'])

# Si un fichier image a été uploadé
if image:
    # Affiche l'image dans l'application
    st.image(image)

# ===== SECTION UPLOAD DE VIDÉOS =====
# Permet à l'utilisateur d'uploader une vidéo (formats .mp4 ou .avi)
video = image = st.file_uploader("** PLEASE UPLOAD A VIDEO", type=['mp4','avi'])

# Si un fichier vidéo a été uploadé
if video :
    # Affiche la vidéo dans l'application
    st.video(video)

# ===== SECTION CONTRÔLES =====
# Curseur: l'utilisateur peut sélectionner une valeur entre 10 et 250 (par pas de 5)
st.slider("** This is a lider**", min_value=10, max_value=250, value=1, step=5)

# Champ de texte multiligne pour qu'une description courte soit entrée
st.text_area("Courte description")

# Sélecteur de date pour que l'utilisateur entre une date
st.date_input("Entrer une date")