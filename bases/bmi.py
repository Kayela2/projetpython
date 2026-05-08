# Importation de Streamlit pour créer l'interface
import streamlit as st

# Affiche le titre de l'application
st.title(" BMI CALCULATOR")

# ===== ENTRÉES DE L'UTILISATEUR =====
# Champ numérique pour entrer le poids en kilogrammes
weight = st.number_input("Entrer votre poids (kg)")

# Bouton radio pour choisir l'unité de mesure de la taille
statut = st.radio("Selectionner le format de la taille",("cm","metres","pieds"))

# ===== CALCUL DE L'IMC (BMI) =====
# Bloc try-except pour gérer les erreurs potentielles (comme division par zéro)
try :
    # Si l'utilisateur a sélectionné les centimètres
    if statut == "cm":
        height = st.number_input('Centimetres')
        # Formule de l'IMC: poids / (taille en mètres)^2
        # Convertit les cm en mètres en divisant par 100
        bmi = weight/((height/100)**2)
        bmi = round(bmi)  # Arrondit le résultat
    
    # Si l'utilisateur a sélectionné les mètres
    elif statut == "metres":
        height = st.number_input('Metres')
        # Calcul direct avec la taille en mètres
        bmi = weight/(height**2)
        bmi = round(bmi)
    
    # Si l'utilisateur a sélectionné les pieds
    elif statut== "pieds":
        height = st.number_input('Pieds')
        # Convertit les pieds en mètres (1 pied = 0.305 mètres, donc 1 m = 3.28 pieds)
        bmi = weight/((height/3.28)**2)
        bmi = round(bmi)
    
# Gère les exceptions (erreurs) qui pourraient survenir
except Exception as e:
    print(" Erreur division 0")  # Affiche un message en cas d'erreur

# ===== BOUTON DE CALCUL ET AFFICHAGE DES RÉSULTATS =====
# Vérifie si le bouton a été cliqué
if(st.button('Calcule BMI')) :
    # Affiche l'IMC calculé avec 2 décimales
    st.write(f"Ton BMI est de {bmi:.2f}")

    # Analyse l'IMC et affiche un message approprié
    if bmi < 18.5 :
        # IMC < 18.5: sous-poids (message d'erreur en rouge)
        st.error("Tu es en sous-poids")
    elif bmi > 18.5 and bmi < 25 :
        # IMC entre 18.5 et 25: poids normal (message informatif en bleu)
        st.info("Tu es en bonne sante")
    elif bmi > 25:
        # IMC > 25: surpoids (message d'avertissement en jaune)
        st.warning("Va a la salle de sport bro")
    else:
        # Cas exceptionnel (ne devrait pas arriver)
        st.error("Tu es un alien")