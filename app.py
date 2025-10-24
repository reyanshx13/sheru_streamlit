import streamlit as st
import webbrowser as wb
import datetime
import requests
import pyjokes
from gtts import gTTS
from io import BytesIO

# WebRTC
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import queue
import numpy as np
import speech_recognition as sr
import av

# -------------------------
# 🔑 API Key
# -------------------------
API_KEY = "4e4927e1d6a9d4e8f9f7a3313badd7a1"

# -------------------------
# 🧠 Speak Function
# -------------------------
def speak(text):
    st.write(f"🟢 **Sheru:** {text}")
    tts = gTTS(text)
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    st.audio(fp, format="audio/mp3", autoplay=True)

# -------------------------
# 🌤️ Weather Function
# -------------------------
def get_weather(city):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()
        if data["cod"] == 200:
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"]
            return f"The temperature in {city} is {temp}°C with {desc}."
        else:
            return "Sorry, I couldn’t find that city."
    except:
        return "There was an error fetching the weather."

# -------------------------
# 🎯 Command Handler
# -------------------------
def handle_command(command):
    command = command.lower()
    if "youtube" in command:
        wb.open("https://youtube.com")
        return "Opening YouTube."
    elif "weather" in command:
        city = "Prayagraj"
        if "in" in command:
            city = command.split("in")[-1].strip()
        return get_weather(city)
    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        return f"The time is {current_time}."
    elif "date" in command:
        today = datetime.date.today()
        return f"Today's date is {today}."
    elif "search" in command:
        query = command.replace("search", "").strip()
        wb.open(f"https://www.google.com/search?q={query}")
        return f"Searching for {query}."
    elif "joke" in command:
        return pyjokes.get_joke()
    elif "hello" in command:
        return "Hello! How can I help you?"
    elif "your name" in command:
        return "My name is Sheru, your virtual assistant!"
    elif "stop" in command or "quit" in command:
        st.session_state.listening = False
        return "Stopping now. Have a good day!"
    else:
        return "Sorry, I didn’t understand that."

# -------------------------
# 🖥️ Streamlit UI
# -------------------------
st.set_page_config(page_title="Sheru - Voice Assistant", page_icon="🎤", layout="centered")
st.title("⚡️ Sheru - Your Smart Voice Assistant")

st.markdown(
    """
    <style>
    body { background-color: #0E1117; color: white; }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------
# 🎧 Voice Input Using Browser
# -------------------------
if "listening" not in st.session_state:
    st.session_state.listening = False

col1, col2 = st.columns(2)
with col1:
    if st.button("🎙️ Start Listening"):
        st.session_state.listening = True
with col2:
    if st.button("🛑 Stop Listening"):
        st.session_state.listening = False
        speak("Listening stopped.")

audio_queue = queue.Queue()

def audio_callback(frame: av.AudioFrame):
    audio = frame.to_ndarray()
    audio_queue.put(audio)
    return frame

if st.session_state.listening:
    st.info("🎧 Sheru is listening... Speak now!")

    # WebRTC with STUN server for better connectivity
    webrtc_ctx = webrtc_streamer(
        key="speech-recorder",
        mode=WebRtcMode.RECVONLY,
        media_stream_constraints={"audio": True, "video": False},
        audio_frame_callback=audio_callback,
        async_processing=True,
        rtc_configuration={
            "iceServers": [
                {"urls": ["stun:stun.l.google.com:19302"]},  # public STUN server
            ]
        }
    )

    if not audio_queue.empty():
        recognizer = sr.Recognizer()
        try:
            audio_data = audio_queue.get()
            # Convert NumPy array to AudioData
            audio_data = sr.AudioData(audio_data.tobytes(), 16000, 2)
            command = recognizer.recognize_google(audio_data)
            st.write(f"🗣️ You said: **{command}**")
            response = handle_command(command)
            speak(response)
        except sr.UnknownValueError:
            st.warning("⚠️ Sorry, I didn’t catch that.")
        except Exception as e:
            st.error(f"Error: {e}")


