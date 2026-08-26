import streamlit as st
import google.generativeai as genai
from PIL import Image

# Konfigurasi Tampilan Web
st.set_page_config(page_title="SMC Chart Analyzer", page_icon="📈")
st.title("📈 SMC & Price Action Chart Analyzer")
st.write("Unggah screenshot chart kamu untuk mendapatkan analisis otomatis.")

# Input API Key dari User
api_key = st.sidebar.text_input("Masukkan Gemini API Key Kamu:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    # Upload Gambar
    uploaded_file = st.file_uploader("Pilih gambar chart (PNG, JPG, JPEG)...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Chart yang diunggah", use_column_width=True)
        
        if st.button("🔍 Analisis Chart Sekarang"):
            with st.spinner("AI sedang membedah struktur SMC & Price Action..."):
                prompt = """
                Bertindaklah sebagai pakar analisis teknikal Smart Money Concepts (SMC) dan Price Action. 
                Analisis gambar chart ini secara ringkas, to the point, dan terstruktur meliputi:
                1. Tren & Struktur Pasar Utama (BOS, CHoCH/MSS)
                2. Zona Penting (Order Block/OB, FVG/Imbalance, Liquidity BSL/SSL)
                3. Trade Setup (Opsi BUY/SELL, perkiraan Entry, SL, dan TP)
                4. Konfirmasi/Validasi sebelum eksekusi
                Gunakan format bullet points yang mudah dibaca saat trading.
                """
                response = model.generate_content([prompt, image])
                st.markdown("---")
                st.subheader("📊 Hasil Analisis SMC:")
                st.write(response.text)
else:
    st.warning("Silakan masukkan Gemini API Key kamu di sidebar sebelah kiri untuk memulai.")
