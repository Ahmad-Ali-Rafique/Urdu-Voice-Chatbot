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

# Main function
def main():
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(90deg, rgba(2,0,36,1) 0%, rgba(9,9,121,1) 50%, rgba(0,212,255,1) 100%);
        }
        .header-text {
            color: white;
            text-shadow: 2px 2px 4px #000000;
            text-align: center;
        }
        .avatar {
            border-radius: 50%;
            margin-right: 10px;
        }
        .chatbot-avatar {
            width: 50px;
            height: 50px;
            border-radius: 80%;
        }
        .user-text {
            background-color: #f0f0f5;
            padding: 10px;
            border-radius: 10px;
            color: black;
            margin-bottom: 10px;
        }
        .bot-text {
            background-color: #d1e7ff;
            padding: 10px;
            border-radius: 10px;
            color: black;
            margin-bottom: 10px;
        }
        .footer {
            text-align: center;
            color: white;
            padding: 20px;
            font-size: 12px;
            position: fixed;
            bottom: 0;
            width: 100%;
            animation: fadein 2s;
        }
        @keyframes fadein {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        .audio-recorder-container {
        padding: 20px;  /* Adjust padding as needed */
        border: 2px solid #ccc;  /* Add a border */
        border-radius: 10px;  /* Rounded corners */
        background-color: #f9f9f9;  /* Background color */
        display: flex;
        justify-content: center;  /* Center horizontally */
        align-items: center;  /* Center vertically */
        position: relative;  /* Ensure container is positioned */
        }
    
        .audio-recorder-container .stAudio {
        z-index: 10;  /* Bring microphone icon to the front */
        position: relative;  /* Position relative to container */
        }

        .audio-recorder-container::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: #f9f9f9;
        z-index: 1;  /* Background layer */
        border-radius: 10px;  /* Match container border-radius */
        }
        </style>
        """, 
        unsafe_allow_html=True
    )

    st.markdown("<h1 class='header-text'>🎤 Urdu Voice Chatbot</h1>", unsafe_allow_html=True)
    st.subheader('اپنی آواز ریکارڈ کریں اور "اے آئی وائس باٹ" سے جواب حاصل کریں', divider='rainbow')

    st.sidebar.image('Ahmad Ali Profile Photo.png', use_column_width=True)
    st.sidebar.header("**Ahmad Ali Rafique**")
    st.sidebar.write("AI & Machine Learning Expert")

    st.sidebar.header("About Chatbot", divider='rainbow')
    st.sidebar.write('''This is a Urdu voice chatbot created using Streamlit. It takes in Urdu voice input and responds in Urdu voice''')
    st.sidebar.info('''Development process includes these steps.  
    1️⃣ Convert Voice into text, using Google's speech recognition API.  
    2️⃣ Give text to LLM (I used Gemini), and generate a response.
    We can also fine-tune LLM for Urdu for more accurate responses.  
    3️⃣ Convert LLM-generated text into Urdu speech by using Google TTS API.  
    And boom, 🚀 ''')

    st.sidebar.header("Contact Information", divider='rainbow')
    st.sidebar.write("Feel free to reach out through the following")
    st.sidebar.write("[LinkedIn](https://www.linkedin.com/in/ahmad-ali-rafique/)")
    st.sidebar.write("[GitHub](https://github.com/Ahmad-Ali-Rafique/)")
    st.sidebar.write("[Email](arsbussiness786@gmail.com)")
    st.sidebar.write("Developed by Ahmad Ali Rafique", unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="audio-recorder-container">', unsafe_allow_html=True)
    # Audio recorder for Urdu input
    audio_data = audio_recorder(text='بولیۓ', icon_size="2x", icon_name="microphone-lines", key="urdu_recorder")
    st.markdown('</div>', unsafe_allow_html=True)

    if audio_data is not None:
        with st.container():
            col1, col2 = st.columns(2)

            with col2:
                # Display the recorded audio file
                st.markdown('<h2 class="avatar">🧑</h2>', unsafe_allow_html=True)
                st.audio(audio_data)
                
                # Save the recorded audio to a temporary file
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio_file:
                    temp_audio_file.write(audio_data)
                    temp_audio_file_path = temp_audio_file.name

                # Convert audio file to text
                text = convert_audio_to_text(temp_audio_file_path)
                st.markdown(f'<div class="user-text">{text}</div>', unsafe_allow_html=True)

                # Remove the temporary file
                os.remove(temp_audio_file_path)

        # Get response from the LLM model
        response_text = get_llm_response(text)

        with st.container():
            col1, col2 = st.columns(2)

            with col1:
                # Convert the response text to speech
                response_audio_html = convert_text_to_audio(response_text)

                st.markdown(f'<div class="bot-text">{response_text}</div>', unsafe_allow_html=True)

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

        # Directly use st.audio with the file path
        st.audio(tts_audio_path, format='audio/mp3')
    except Exception as e:
        st.error(f"Error converting text to audio: {e}")

def encode_audio_to_base64(file_path):
    with open(file_path, "rb") as audio_file:
        audio_bytes = audio_file.read()
    return base64.b64encode(audio_bytes).decode()

def get_llm_response(text, retries=3, delay=5):
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

    for attempt in range(retries):
        try:
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                generation_config=generation_config,
            )

            chat_session = model.start_chat()
            response = chat_session.send_message(prompt)

            return response.text
        except Exception as e:
            st.error(f"Error while fetching response from LLM: {e}")
            time.sleep(delay)  # Wait before retrying
            if attempt == retries - 1:
                return "Sorry, there was an error processing your request."

if __name__ == "__main__":
    main()
