import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="SMC Chart Analyzer", layout="centered")

st.title("📈 SMC & Price Action Chart Analyzer")
st.write("Unggah screenshot chart kamu untuk mendapatkan analisis otomatis.")

# Sidebar untuk API Key
st.sidebar.header("Pengaturan")
api_key = st.sidebar.text_input("Masukkan Gemini API Key:", type="password")

# Upload Gambar
uploaded_file = st.file_uploader("Pilih gambar chart (PNG, JPG, JPEG)...", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Chart yang diunggah")
    
    if st.button("🔍 Analisis Chart Sekarang"):
        if not api_key:
            st.error("Silakan masukkan Gemini API Key di sidebar terlebih dahulu!")
        else:
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = """
                Kamu adalah seorang analis pasar teknikal profesional spesialis Smart Money Concepts (SMC) dan Price Action. 
                Analisis gambar chart trading ini dan berikan respons terstruktur:
                1. **Tren Utama & Struktur Pasar:** (Bullish/Bearish/Side, Higher High/Low, Break of Structure).
                2. **Area Kunci SMC:** (Order Block, Fair Value Gap/FVG, Liquidity Sweep, Support/Resistance).
                3. **Rekomendasi Rencana Trading:** (Saran Entry, Area Stop Loss, dan Target Take Profit dengan alasannya).
                4. **Peringatan Risiko:** (Risiko utama atau kondisi konfirmasi yang perlu ditunggu).
                Gunakan bahasa Indonesia yang jelas, tegas, dan mudah dipahami.
                """
                
                with st.spinner("Sedang menganalisis chart... Mohon tunggu..."):
                    response = model.generate_content([prompt, image])
                    st.success("Analisis Selesai!")
                    st.markdown("### Hasil Analisis Chart:")
                    st.write(response.text)
                    
            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")
