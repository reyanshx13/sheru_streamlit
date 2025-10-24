import streamlit as st
import webbrowser as wb
import datetime
import requests
import pyjokes
from gtts import gTTS
import os

# -------------------------
# 🔑 API Key
# -------------------------
API_KEY = "4e4927e1d6a9d4e8f9f7a3313badd7a1"

# -------------------------
# 🧠 Speak Function (gTTS)
# -------------------------
def speak(text):
    st.write(f"🟢 **Sheru:** {text}")
    tts = gTTS(text)
    tts.save("response.mp3")
    st.audio("response.mp3", autoplay=True)

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
        return "Stopping now. Have a good day!"
    else:
        return "Sorry, I didn’t understand that."

# -------------------------
# 🖥️ Streamlit UI
# -------------------------
st.set_page_config(page_title="Sheru - Voice Assistant", page_icon="🎤", layout="centered")
st.title("⚡️ Sheru - Your Smart Voice Assistant")

# Background Style
st.markdown(
    """
    <style>
    body { background-color: #0E1117; color: white; }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------
# 🎤 User Input
# -------------------------
command = st.text_input("Type your command here and press Enter:")

if command:
    response = handle_command(command)
    speak(response)

