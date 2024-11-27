#Step 1: Import the necessary libraries
import streamlit as st
import speech_recognition as sr

# Step 2: Define the language and speech recognition function
def language_code(language):
    if language == "Français":
        return "fr"
    elif language == "Anglais":
        return "en"
    elif language == "Espagnol":
        return "es"
    else:
        return "en" 

def transcribe_speech(api_choice, language, pause_and_resume):
    # Initialisation de la classe de reconnaissance
    r = sr.Recognizer()

    # Lecture du microphone comme source
    try:
        with sr.Microphone() as source:
            st.info("Parlez maintenant...")

            #Si la mise en pause est activée, ne pas écouter
            if pause_and_resume:
                st.info("Enregistrement en pause..")
                return "Enregistrement en pause"
            
            # écoute la parole et la stocke dans la variable audio_text
            audio_text = r.listen(source, timeout=10, phrase_time_limit=20)
            st.info("Transcription...")

            # Utiliser l'API sélectionnée
            if api_choice == "Google":
                return r.recognize_google(audio_text, language=language_code(language))
            elif api_choice == "Sphinx":
                return r.recognize_sphinx(audio_text)
            elif api_choice == "Bing Speech (Azure)":
                st.warning("Intégration Bing/Azure Speech API à configurer")
                return "API Bing/Azure Speech non encore implémentée"
            else:
                return "API non reconnue"

    #Error handling
    except sr.UnknownValueError:
        return "Impossible de comprendre l'audio. Veuillez réessayer en parlant plus clairement."
    except sr.WaitTimeoutError:
        return "Temps d'attente dépassé. Veuillez parler après avoir cliqué sur le bouton."
    except sr.RequestError:
        return "Erreur de service. Vérifiez votre connexion Internet ou l'accès au service."
    except Exception:
        return "Erreur inattendue. Veuillez réessayer ou contacter le support."

# Step 3: Define the main function
def main():
    st.title("Speech Recognition App")
    st.write("Cliquez sur le microphone pour commencer à parler:")

    # Ajouter une option de sélection d'API
    api_choice = st.selectbox(
        "Choisissez l'API de reconnaissance vocale :",
        ("Google", "Sphinx", "Bing Speech (Azure)"))

    #ajouter une option de sélection de langue
    language = st.selectbox("Choisissez la langue :",
                            ("Français", "Anglais", "Espagnol"))
    
    #mettre en pause et de reprendre le processus de reconnaissance vocale
    pause_and_resume = st.checkbox("Mettre en pause et reprendre le processus") 

    # Ajouter un bouton pour déclencher la reconnaissance vocale
    if st.button("Start Recording"):
        text = transcribe_speech(api_choice, language, pause_and_resume)
        st.write("Transcription : ", text)

        #ajouter un bouton pour enregistrer le texte dans un fichier
        if st.button("Enregistrer la Transcription"):
            with open("Transcription.txt", "w") as file:
                file.write(text)
            st.success("Transcription enregistrée dans transcription.txt")

    #Ajouter des boutons pour mettre en pause et reprendre l'enregistrement
    if pause_and_resume:
        if st.button("Mettre en pause"):
            pause_and_resume = False
        if st.button("Reprendre"):
            pause_and_resume = True

if __name__ == "__main__":
    main()
