![YOLO Helmet Detection]([https://github.com/Ahmad-Ali-Rafique/AI-Chatbot/blob/main/Ai-Chatbot.png](https://github.com/Ahmad-Ali-Rafique/Urdu-Voice-Chatbot/blob/main/AI%20Chatbot.png))  <!-- Replace with a relevant image link -->

# Urdu Voice Chatbot - Streamlit

Welcome to the Urdu Voice Chatbot project! This repository showcases a Streamlit application that allows users to interact with a chatbot using Urdu voice input and receive responses in Urdu.

## 🚀 **Project Overview**

The Urdu Voice Chatbot is designed to:
1. **Record Urdu Voice Input**: Users can record their voice in Urdu using the integrated audio recorder.
2. **Convert Voice to Text**: The recorded voice is transcribed into Urdu text using Google's Speech Recognition API.
3. **Generate AI Responses**: The transcribed text is processed by Gemini’s Generative AI model to generate a relevant response.
4. **Convert Text to Voice**: The generated response is then converted back into Urdu speech using Google's Text-to-Speech (TTS) API.
5. **Interactive Interface**: The Streamlit interface provides a user-friendly way to interact with the chatbot.

## 🛠️ **Technologies Used**

- **Streamlit**: For creating the interactive web interface.
- **Google Speech Recognition API**: For converting spoken Urdu into text.
- **Gemini Generative AI**: For generating intelligent responses in Urdu.
- **Google Text-to-Speech API**: For converting text responses back into speech.

## 📦 **Installation & Usage**

1. **Clone the Repository**
    ```bash
    git clone https://github.com/your-username/urdu-voice-chatbot-streamlit.git
    cd urdu-voice-chatbot-streamlit
    ```

2. **Create a Virtual Environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up Secrets**
    Create a `.streamlit/secrets.toml` file and add your API keys:
    ```toml
    [gemini]
    api_key = "YOUR_API_KEY_HERE"
    ```

5. **Run the App**
    ```bash
    streamlit run voicechatbot.py
    ```

## 📈 **Deployment**

This application is also deployed on Streamlit Cloud. You can access the live app here: [Your Streamlit App URL](https://ahmad-ali-urdu-voice-chatbot.streamlit.app/)

## 🔍 **Contributing**

Contributions are welcome! Please open an issue or submit a pull request if you have suggestions or improvements.

## 📧 **Contact**

For any inquiries or feedback, please reach out to me at [E-mail](arsbussiness786@gmail.com).

## 👤 **About Me**

I am Ahmad Ali Rafique, an AI & Machine Learning specialist with a focus on building intelligent applications. My expertise includes deep learning, natural language processing, and creating interactive applications using modern technologies. You can find more about my work on [GitHub](https://github.com/Ahmad-Ali-Rafique) and connect with me on [LinkedIn](https://www.linkedin.com/in/ahmad-ali-rafique/).
