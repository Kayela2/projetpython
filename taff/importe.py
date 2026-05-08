import streamlit as st

st.title('upload file') # affiche le titre de l'application

image = st.file_uploader("*  please upload an image", type=["jpg", "jpeg", "png"]) # crée un champ de téléchargement de fichier pour les images avec des types de fichiers spécifiques
 
if image:
  st.image(image) # affiche l'image téléchargée dans l'application

video = image = st.file_uploader("** Please upload a video", type=["mp4", "avi", "mov"])
if video : 
  st.video(video) # affiche la vidéo téléchargée dans l'application

st.slider("*** This is a lider ***", min_value=10, max_value=50, value=1, step=5)

st.text_area("Courte description")