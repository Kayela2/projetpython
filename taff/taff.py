import streamlit as st
import pandas as pd

st.title("Hello Girl") # affiche le titre de l'application
st.metric(label="wind speed", value="120ms-1",delta="-1.4ms-1") # affiche une métrique avec un delta

table = pd.DataFrame({"Column1":[1,2,3], "Column2":[9,8,7]}) # crée un DataFrame avec deux colonnes et trois lignes
st.dataframe(table) # affiche le DataFrame dans l'application
st.write(table)
#st.image("stream.jpg") # affiche une image (assurez-vous que le fichier "stream.jpg" est dans le même répertoire que ce script

state = st.checkbox('Checbox', value=True) # crée une case à cocher avec une valeur par défaut de True
if state : # si la case est cochée
    st.write("Box Checked") # affiche "Box Checked"
else : # sinon
    st.write("Box unchecked") # affiche "Box unchecked"
radio_btn = st.radio("Radio Button", ("US","UK","Canada")) # crée un bouton radio pour sélectionner une option parmi "US", "UK" et "Canada"
btn = st.button("Click Me") # crée un bouton cliquable
select = st.selectbox("select box", ("Audi","BMBW","MUSTANG")) # crée une liste déroulante pour sélectionner une marque de voiture

Multi_select = st.multiselect("Multibex", ('APPLE','SAMSUNG','HUAWEI','HONOR')) # crée une sélection multiple pour choisir plusieurs marques de téléphones

