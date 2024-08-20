import streamlit as st
from audio_recorder_streamlit import audio_recorder
import speech_recognition as sr
from gtts import gTTS
import os
import base64
import tempfile
import google.generativeai as genai

# Configure the Gemini API key
GEMINI_API_KEY = st.secrets['gemini']['api_key']
genai.configure(api_key=GEMINI_API_KEY)

def main():
    st.title("🎤 :blue[Urdu Voice Chatbot] 💬🤖")
    st.subheader('اپنی آواز ریکارڈ کریں اور "اے آئی وائس باٹ" سے جواب حاصل کریں', divider='rainbow')

    st.sidebar.header("About Urdu Voice Chatbot", divider='rainbow')
    st.sidebar.write(f'''This a Urdu voice chatbot created using Streamlit. It takes in Urdu voice input and response in Urdu voice''')
    
    st.sidebar.info(f'''Development process includes these steps.  
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

    urdu_recorder = audio_recorder(text='بولیۓ', icon_size="2x", icon_name="microphone-lines", key="urdu_recorder")

    if urdu_recorder is not None:
        with st.container():
            col1, col2 = st.columns(2)

            with col2:
                # Display the audio file
                st.header('🧑')
                st.audio(urdu_recorder)

                # Create a temporary file to save the recorded audio
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_urdu_recording:
                    temp_urdu_recording.write(urdu_recorder)
                    temp_urdu_recording_path = temp_urdu_recording.name

                # Convert audio file to text
                text = Urdu_audio_to_text(temp_urdu_recording_path)
                st.success(text)

                # Remove the temporary file
                os.remove(temp_urdu_recording_path)

        # Get the response from the LLM
        response_text = llmModelResponse(text)

        with st.container():
            col1, col2 = st.columns(2)

            with col1:
                # Convert the response text to speech
                response_audio_html = response_to_urdu_audio(response_text)

                st.header('🤖')
                st.markdown(response_audio_html, unsafe_allow_html=True)

                st.info(response_text)

def Urdu_audio_to_text(temp_urdu_recording_path):
    # Speech Recognition
    recognizer = sr.Recognizer()
    with sr.AudioFile(temp_urdu_recording_path) as source:
        urdu_recoded_voice = recognizer.record(source)
        try:
            text = recognizer.recognize_google(urdu_recoded_voice, language="ur")
            return text
        except sr.UnknownValueError:
            return "آپ کی آواز واضح نہیں ہے"
        except sr.RequestError:
            return "Sorry, my speech service is down"

def response_to_urdu_audio(text, lang='ur'):
    tts = gTTS(text=text, lang=lang)
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_audio:
        tts.save(temp_audio.name)
        temp_audio_path = temp_audio.name

    # Get the base64 string of the audio file
    audio_base64 = get_audio_base64(temp_audio_path)

    # Autoplay audio using HTML and JavaScript
    audio_html = f"""
    <audio controls autoplay>
        <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
        Your browser does not support the audio element.
    </audio>
    """
    return audio_html

# Function to encode the audio file to base64
def get_audio_base64(file_path):
    with open(file_path, "rb") as audio_file:
        audio_bytes = audio_file.read()
    return base64.b64encode(audio_bytes).decode()

def llmModelResponse(text):
    prompt = f"""Kindly answer this question in Urdu langauge. 
    Dont use any other language or chaaracters from other languages.
    Use some kind Urdu words in start and ending of your answer realted to question. 
    Keep your answer short. 
    You can also ask anything related to the topic in urdu.
    if you dont know the answer or dont understand the question, 
    Respond with 'I did not get what you speak, please try again' in urdu.
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
