import streamlit as st
import httpx
import asyncio
import os
from dotenv import load_dotenv

# 1. Load Secrets from .env (Security for GitHub)
load_dotenv()
AUTH_TOKEN = os.getenv("AUTH_TOKEN")

# 2. Page Config
st.set_page_config(page_title="SkyPulse Pro", page_icon="🌐", layout="wide")

# 3. Advanced Neon CSS
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at center, #010101 0%, #000000 70%, #040d1c 100%); overflow: hidden; }
    
    @keyframes particle-motion {
        0% { transform: translateY(0) translateX(0) rotate(0deg); opacity: 0; }
        50% { opacity: 0.6; }
        100% { transform: translateY(-1000px) translateX(300px) rotate(360deg); opacity: 0; }
    }
    .particles {
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background-image: radial-gradient(#0ff 1px, transparent 1.5px), radial-gradient(#f0f 1px, transparent 1.5px);
        background-size: 400px 400px, 250px 250px;
        animation: particle-motion 30s linear infinite;
        z-index: 0;
    }

    @keyframes ticker-scroll { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    .ticker-wrap {
        width: 100%; overflow: hidden; background: rgba(0, 255, 255, 0.05);
        border: 1px solid #0ff; border-radius: 10px; padding: 10px 0; 
        margin-bottom: 25px; box-shadow: 0 0 15px rgba(0, 255, 255, 0.2);
    }
    .ticker-text {
        display: inline-block; white-space: nowrap; font-size: 0.95rem; color: #0ff;
        animation: ticker-scroll 20s linear infinite; text-shadow: 0 0 5px #0ff;
    }

    .input-section {
        background: rgba(4, 13, 28, 0.4); backdrop-filter: blur(15px);
        border-radius: 20px; padding: 30px; border: 1px solid rgba(0, 255, 255, 0.1);
        z-index: 10;
    }
    h1 { text-align: center; color: white !important; text-shadow: 0 0 15px #0ff; }
    .neon-emoji { font-size: 50px; text-shadow: 0 0 20px #0ff; vertical-align: middle; }
    </style>
    <div class="particles"></div>
    """, unsafe_allow_html=True)

# 4. Header Icons (Fixed NameErrors)
col_l, col_m, col_r = st.columns([1, 1, 1.2]) 
with col_l: st.image("https://img.icons8.com/color/144/null/partly-cloudy-day--v1.png", width=110)
with col_m: st.image("https://img.icons8.com/color/144/null/summer--v1.png", width=120) 
with col_r: 
    st.markdown("""
        <div style='display: flex; align-items: center;'>
            <img src='https://img.icons8.com/color/144/null/cloud-lighting.png' width='110'>
            <span class='neon-emoji'>☁️⚡</span>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<h1>SKY PULSE ATMOSPHERE PRO</h1>", unsafe_allow_html=True)

# 5. Moving Bar
st.markdown('<div class="ticker-wrap"><div class="ticker-text">📡 SATELLITE LINK ACTIVE... | 🛰️ SCANNING GLOBAL NODES... | 🌡️ FETCHING LIVE ATMOSPHERIC DATA... | 🚨 Developed by Faizan DEV...</div></div>', unsafe_allow_html=True)

# 6. Input Section
with st.container():
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    pak_cities = ["Faisalabad", "Lahore", "Karachi", "Islamabad", "Multan", "Peshawar", "Other"]
    
    c_in, c_unit = st.columns([3, 1])
    with c_in:
        selected = st.selectbox("📍 Select City", pak_cities)
        city = st.text_input("Or Type Manually", placeholder="e.g. London, Dubai") if selected == "Other" else selected
    with c_unit:
        unit = st.radio("Unit", ["Celsius", "Fahrenheit"], horizontal=True)
    
    search_btn = st.button("Check Weather")
    st.markdown('</div>', unsafe_allow_html=True)

# 7. API Logic (Secure with AUTH_TOKEN)
async def fetch_weather(city_name):
    async with httpx.AsyncClient() as client:
        try:
            # AUTH_TOKEN ab seedha .env se aa raha hai
            headers = {"x-auth-token": AUTH_TOKEN}
            r = await client.get(f"http://127.0.0.1:8000/weather/{city_name}", headers=headers)
            return r.json()
        except: return None

if search_btn and city:
    data = asyncio.run(fetch_weather(city))
    if data and "detail" not in data:
        st.write("---")
        temp = data['temperature'] if unit == "Celsius" else round((data['temperature'] * 9/5) + 32, 1)
        m1, m2, m3 = st.columns(3)
        m1.metric("🌡️ Temperature", f"{temp}° {unit[0]}")
        m2.metric("🌬️ Air Quality (AQI)", data['aqi'])
        m3.metric("💨 Wind Speed", f"{data['wind_speed']} km/h")
    elif data: st.error(data['detail'])
    else: st.error("⚠️ Backend Offline! Please run 'uvicorn main:app'.")