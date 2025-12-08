import streamlit as st
import google.generativeai as genai

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="MedSim Alpha", page_icon="🩺", layout="wide")

# --- CSS İLE GÖRSEL DÜZENLEMELER (MOBİL DÜZELTMELERİ DAHİL) ---
st.markdown("""
<style>
    /* --- 1. MOBİL İÇİN YAN MENÜ BUTONU AYARLARI --- */
    /* Sol üstteki menü açma butonunu (ok/hamburger) belirginleştirir */
    [data-testid="stSidebarCollapsedControl"] {
        background-color: #E3F2FD !important; /* Açık mavi arka plan */
        color: #1565C0 !important; /* Koyu mavi ikon */
        border: 2px solid #1565C0 !important; /* Çerçeve */
        border-radius: 50% !important; /* Yuvarlak buton */
        width: 2.5rem !important;
        height: 2.5rem !important;
        z-index: 1000001 !important; /* Her şeyin üstünde kalsın */
    }
    
    /* Butonun üzerine gelince */
    [data-testid="stSidebarCollapsedControl"]:hover {
        background-color: #1565C0 !important;
        color: white !important;
    }

    /* --- 2. MOBİLDE CHAT PENCERESİ GÖRÜNÜRLÜĞÜ --- */
    /* Ana içerik alanının altına ekstra boşluk bırakır. 
       Böylece son mesaj, alttaki yazı yazma kutusunun arkasında kalmaz. */
    .main .block-container {
        padding-bottom: 160px !important; 
    }

    /* Chat Input (Yazı Yazma) Alanı */
    div[data-testid="stChatInput"] {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        padding: 1rem;
        background-color: #F8F8F8; /* Arkasındaki yazıların karışmaması için opak arka plan */
        z-index: 1000;
    }

    /* --- 3. GENEL GÖRSEL AYARLAR --- */
    .stChatMessage { border-radius: 10px; padding: 10px; }
    .stButton button { width: 100%; border-radius: 5px; font-weight: bold; }
    h1 { color: #2c3e50; }
    .stAlert { border-radius: 5px; }
    
    /* Mobil uyumluluk için metin boyutları */
    @media only screen and (max-width: 600px) {
        h1 { font-size: 1.8rem; }
        .stButton button { padding: 15px 10px; } /* Mobilde butonlara daha kolay basılsın */
    }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE (Hafıza) ---
if "history" not in st.session_state:
    st.session_state.history = []
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None
if "sys_instruct" not in st.session_state:
    st.session_state.sys_instruct = ""
# API Key başlangıçta boş
if "api_key" not in st.session_state:
    st.session_state.api_key = ""

# --- YAN MENÜ (SIDEBAR) ---
with st.sidebar:
    st.title("MedSim")
    
    st.markdown("⚠️ *Sistemi kullanmak için API Key gereklidir.*")
    
    api_key_input = st.text_input(
        "Google API Key:", 
        type="password", 
        placeholder="AIzaSy...", 
        value=st.session_state.api_key,
        help="Google AI Studio'dan aldığınız anahtarı buraya yapıştırın."
    )
    
    if api_key_input:
        st.session_state.api_key = api_key_input

    st.divider()

    # YENİ VAKA BUTONU
    if st.button("🎲 YENİ VAKA OLUŞTUR", type="primary"):
        if not st.session_state.api_key:
            st.error("Lütfen önce yukarıdaki kutuya geçerli bir API Key girin!")
        else:
            st.session_state.history = []
            st.session_state.chat_session = None
            
            try:
                genai.configure(api_key=st.session_state.api_key)
                model = genai.GenerativeModel("gemini-2.5-flash") # Model
                
                with st.spinner("Vaka hazırlanıyor..."):
                    prompt = """
                    Tıp eğitimi için bir vaka oluştur. Vakalar her türlü branştan gelebilir.
                    
                    SİSTEM TALİMATI (System Instruction):
                    1. ROLÜN: [Hasta. İsim, Yaş, Cinsiyet, Meslek].
                    2. ŞİKAYET: [Tek cümlelik, net giriş şikayeti].
                    3. GERÇEK TANI: [Gizli].
                    4. TARZIN: Tamamen hasta rolündesin. "Yapay zekayım" deme. Yapay zekanın bilgilendirici fonksiyonlarını asla kullanma. Tam bir hasta profili olarak davran.
                       - Konuşman "motomot", kısa ve net olsun. Duygusallık yok.
                       - Sadece sorulan soruya cevap ver.
                       - Örnek: "Ağrın nerede?" -> "Göğsümde." (Hikaye anlatma).
                    5. TIBBİ VERİLER (Doktor özel olarak isterse parantez içinde teknik dille ver):
                       - İstenmeyen veriyi asla verme.
                    6. ORDER/TEDAVİ: Doktor order girdiğinde (İlaç, doz), uygunluğunu teknik dille değerlendir.
                    """
                    
                    res = model.generate_content(prompt)
                    st.session_state.sys_instruct = res.text
                    
                    st.session_state.chat_session = model.start_chat(history=[
                        {"role": "user", "parts": ["Senaryoyu başlat. Kendini tanıt ve şikayetini tek cümleyle söyle:\n" + st.session_state.sys_instruct]}
                    ])
                    
                    first_msg = st.session_state.chat_session.send_message("Başla")
                    st.session_state.history.append({"role": "model", "parts": [first_msg.text]})
                    st.rerun()
                    
            except Exception as e:
                st.error(f"API Hatası: Anahtarınızı kontrol edin. Hata detayı: {e}")

    st.divider()

    # --- FONKSİYONLAR ---

    # 1. VİTALLER
    with st.expander("💓 VİTALLER"):
        vitals_list = st.multiselect("Ölçüm Seçin:", 
            ["Tansiyon", "Nabız", "Ateş", "Solunum Sayısı", "SpO2", "Kan Şekeri"])
        if st.button("Vitalleri Ölç"):
            if st.session_state.chat_session and vitals_list:
                msg = f"(Doktor şu vitalleri ölçtü: {', '.join(vitals_list)}. Sonuçları teknik formatta ver.)"
                response = st.session_state.chat_session.send_message(msg)
                st.session_state.history.append({"role": "user", "parts": [f"{', '.join(vitals_list)} ölçülüyor..."]})
                st.session_state.history.append({"role": "model", "parts": [response.text]})
                st.rerun()
            elif not st.session_state.chat_session:
                st.warning("Önce vaka oluşturun.")

    # 2. FİZİK MUAYENE
    with st.expander("🩺 FİZİK MUAYENE"):
        fm_list = st.multiselect("Muayene Bölgesi:", 
            ["Genel Durum", "Baş-Boyun", "Solunum Sistemi", "Kardiyovasküler", 
             "Batın Muayenesi", "Nörolojik Muayene", "Ekstremiteler", "Deri", "Ruhsal Durum"])
        if st.button("Muayene Et"):
            if st.session_state.chat_session and fm_list:
                msg = f"(Doktor şu sistemleri muayene etti: {', '.join(fm_list)}. Sadece bu sistemlerdeki pozitif/negatif bulguları teknik dille yaz.)"
                response = st.session_state.chat_session.send_message(msg)
                st.session_state.history.append({"role": "user", "parts": [f"{', '.join(fm_list)} muayenesi yapılıyor..."]})
                st.session_state.history.append({"role": "model", "parts": [response.text]})
                st.rerun()
            elif not st.session_state.chat_session:
                st.warning("Önce vaka oluşturun.")

    # 3. LABORATUVAR
    with st.expander("🧪 LABORATUVAR"):
        lab_list = st.multiselect("Tetkik Seçin:", 
            ["Hemogram", "Geniş Biyokimya", "Elektrolitler", "Karaciğer Fonksiyon Testleri", 
             "Böbrek Fonksiyon Testleri", "Kardiyak Enzimler", "Koagülasyon", 
             "Kan Gazı", "D-Dimer", "CRP / Sedim", "TIT"])
        if st.button("Tetkik İste"):
            if st.session_state.chat_session and lab_list:
                msg = f"(Doktor şu tetkikleri istedi: {', '.join(lab_list)}. Sonuçları referans değerleri olmadan, patolojik olanları belirterek liste halinde ver.)"
                response = st.session_state.chat_session.send_message(msg)
                st.session_state.history.append({"role": "user", "parts": [f"{', '.join(lab_list)} isteniyor..."]})
                st.session_state.history.append({"role": "model", "parts": [response.text]})
                st.rerun()
            elif not st.session_state.chat_session:
                st.warning("Önce vaka oluşturun.")

    # 4. GÖRÜNTÜLEME
    with st.expander("🩻 GÖRÜNTÜLEME"):
        rad_modality = st.selectbox("Modalite:", ["Direkt Grafi", "BT", "USG", "MR", "EKG"])
        rad_area = st.text_input("Bölge (Örn: Akciğer, Tüm Batın, Beyin):")
        if st.button("Görüntüle"):
            if st.session_state.chat_session and rad_area:
                full_req = f"{rad_area} {rad_modality}"
                msg = f"(Doktor şunu istedi: {full_req}. Rapor sonucunu teknik dille, bir radyoloji uzmanının raporu şeklinde ver.)"
                response = st.session_state.chat_session.send_message(msg)
                st.session_state.history.append({"role": "user", "parts": [f"{full_req} çekiliyor..."]})
                st.session_state.history.append({"role": "model", "parts": [response.text]})
                st.rerun()
            elif not st.session_state.chat_session:
                st.warning("Lütfen önce vaka oluşturun veya bölge girin.")
    
    st.divider()
    
    # 5. ORDER / TANI
    with st.expander("💊 ORDER & TANI", expanded=True):
        order_text = st.text_area("Tedavi / Order / Tanı:", placeholder="Örn: 1000cc SF IV infüzyon veya Akut Pankreatit tanısı...")
        if st.button("Uygula / Tanı Koy"):
            if st.session_state.chat_session and order_text:
                msg = f"(Doktor şu girişimi yaptı veya tanıyı koydu: '{order_text}'. Bunu güncel resmi ve güvenilir kılavuzlara göre değerlendir. Eğer tanıysa doğru mu? Eğer tedaviyse uygun mu? Teknik bir dille geri bildirim ver.)"
                response = st.session_state.chat_session.send_message(msg)
                st.session_state.history.append({"role": "user", "parts": [f"📝 GİRİŞİM: {order_text}"]})
                st.session_state.history.append({"role": "model", "parts": [response.text]})
                st.rerun()
            elif not st.session_state.chat_session:
                st.warning("Önce vaka oluşturun.")

# --- ANA EKRAN (CHAT) ---
st.title("🩺 MedSim")
st.caption("Tıbbi Vaka Simülasyonu")
st.caption("Bu web uygulaması alpha sürümdedir. Tıbbi tavsiye yerine geçmez.")

# Geçmişi Göster
for message in st.session_state.history:
    role = message["role"]
    text = message["parts"][0]
    
    if role == "user":
        with st.chat_message("user", avatar="🧑‍⚕"):
            st.markdown(text)
    else:
        with st.chat_message("assistant", avatar="👤"):
            st.markdown(text)

# Kullanıcı Girişi (En altta)
# NOT: Eğer chat_session yoksa bile input görünmeli mi?
# Mobil tasarımda "sabit" bir footer istiyorsak bunu session kontrolü dışına çıkarabiliriz
# ancak mantık akışı gereği vaka yoksa soru sormak anlamsız.
if st.session_state.chat_session:
    user_input = st.chat_input("Hastaya soru sorun...")
    if user_input:
        st.session_state.history.append({"role": "user", "parts": [user_input]})
        try:
            response = st.session_state.chat_session.send_message(user_input)
            st.session_state.history.append({"role": "model", "parts": [response.text]})
            st.rerun()
        except Exception as e:
            st.error(f"Bağlantı hatası: {e}")
else:
    if not st.session_state.api_key:
         st.info("⬅ Sol menüden API Key girerek başlayın.")
    else:
         st.info("⬅ Sol menüden 'YENİ VAKA OLUŞTUR' butonuna basın.")
