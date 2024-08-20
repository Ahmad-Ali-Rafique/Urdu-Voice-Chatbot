import streamlit as st
from audio_recorder_streamlit import audio_recorder
import speech_recognition as sr
from gtts import gTTS
import os
import base64
import tempfile
import google.generativeai as genai

# Retrieve API key from Streamlit secrets
GEMINI_API_KEY = st.secrets['gemini']['api_key']
genai.configure(api_key=GEMINI_API_KEY)

def main():
    st.title("🎤 :blue[Urdu Voice Chatbot] 💬🤖")
    st.subheader('اپنی آواز ریکارڈ کریں اور "اے آئی وائس باٹ" سے جواب حاصل کریں', divider='rainbow')

    st.sidebar.header("About Urdu Voice Chatbot", divider='rainbow')
    st.sidebar.write('''This a Urdu voice chatbot created using Streamlit. It takes in Urdu voice input and responds in Urdu voice''')
    
    st.sidebar.info('''Development process includes these steps.  
    1️⃣ Convert Voice into text, using Google's speech recognition API.  
    2️⃣ Give text to LLM (I used Gemini), and generate a response.
    we can also fine-tune LLM for URDU for more accurate responses).  
    3️⃣ Convert LLM-generated text into URDU speech by using Google TTS API.  
    And boom, 🚀 ''')

    st.sidebar.write("")  # Adds one line of space
    st.sidebar.write("")  # Adds one line of space
    st.sidebar.write("")  # Adds one line of space
    st.sidebar.write("")  # Adds one line of space
    
    st.sidebar.write("Developed by [Mubeen F.] (https://mubeenf.com)")

    # Audio recorder for Urdu input
    audio_data = audio_recorder(text='بولیۓ', icon_size="2x", icon_name="microphone-lines", key="urdu_recorder")

    if audio_data is not None:
        with st.container():
            col1, col2 = st.columns(2)

            with col2:
                # Display the recorded audio file
                st.header('🧑')                                                                                                                                                                                                                                                                                                                                                                                                                                                          
                st.audio(audio_data)

                # Save the recorded audio to a temporary file
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio_file:
                    temp_audio_file.write(audio_data)
                    temp_audio_file_path = temp_audio_file.name
                
                # Convert audio file to text
                text = convert_audio_to_text(temp_audio_file_path)
                st.success(text)

                # Remove the temporary file
                os.remove(temp_audio_file_path)

        # Get response from the LLM model
        response_text = get_llm_response(text)

        with st.container():
            col1, col2 = st.columns(2)

            with col1:
                # Convert the response text to speech
                response_audio_html = convert_text_to_audio(response_text)
                st.header('🤖')
                st.markdown(response_audio_html, unsafe_allow_html=True)

                st.info(response_text)

def convert_audio_to_text(audio_file_path):
    # Convert Urdu audio to text using speech recognition
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file_path) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language="ur")
            return text
        except sr.UnknownValueError:
            return "آپ کی آواز واضح نہیں ہے"
        except sr.RequestError:
            return "Sorry, my speech service is down"

def convert_text_to_audio(text, lang='ur'):
    try:
        tts = gTTS(text=text, lang=lang)
        tts_audio_path = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False).name
        tts.save(tts_audio_path)

        # Encode the audio file to base64
        audio_base64 = encode_audio_to_base64(tts_audio_path)

        # Create HTML for autoplaying audio
        audio_html = f"""
        <audio controls autoplay>
            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
            Your browser does not support the audio element.
        </audio>
        """
        return audio_html
    except Exception as e:
        st.error(f"Error converting text to audio: {e}")
        return ""

def encode_audio_to_base64(file_path):
    with open(file_path, "rb") as audio_file:
        audio_bytes = audio_file.read()
    return base64.b64encode(audio_bytes).decode()

def get_llm_response(text):
    prompt = f"""Kindly answer this question in Urdu language. 
    Don't use any other language or characters from other languages.
    Use some Urdu words at the beginning and end of your answer related to the question. 
    Keep your answer short. 
    You can also ask anything related to the topic in Urdu.
    If you don't know the answer or don't understand the question, 
    Respond with 'I did not get what you speak, please try again' in Urdu.
    Question: {text}"""

    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

    chat_session = model.start_chat()
    response = chat_session.send_message(prompt)

    return response.text

if __name__ == "__main__":
    main()
