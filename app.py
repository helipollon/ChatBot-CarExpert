"""
🚗 Araba Uzmanı ChatBot - Ana Uygulama
Streamlit ile oluşturulmuş araba sorunları uzmanı ChatBot arayüzü.
"""

import streamlit as st
from gemini_client import CarExpertChatBot

# Sayfa yapılandırması
st.set_page_config(
    page_title="🚗 Araba Uzmanı ChatBot",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Özel CSS stilleri
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
    
    /* Ana tema renkleri */
    :root {
        --primary-color: #0f0f23;
        --secondary-color: #1a1a3e;
        --accent-color: #ff4757;
        --accent-secondary: #ffa502;
        --text-color: #eaeaea;
        --success-color: #2ed573;
    }
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Genel sayfa stili */
    .stApp {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a3e 50%, #2d2d5a 100%);
    }
    
    /* Başlık stilleri */
    .main-header {
        background: linear-gradient(90deg, #ff4757, #ffa502, #ff6348);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0;
        text-shadow: 0 0 30px rgba(255, 71, 87, 0.5);
    }
    
    .sub-header {
        color: #a0a0a0;
        text-align: center;
        font-size: 1.2rem;
        margin-top: 5px;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    
    /* Chat container */
    .chat-container {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 24px;
        padding: 30px;
        margin: 20px auto;
        max-width: 900px;
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    }
    
    /* Hoş geldin kartı */
    .welcome-card {
        background: linear-gradient(135deg, rgba(255, 71, 87, 0.1) 0%, rgba(255, 165, 2, 0.1) 100%);
        border-radius: 20px;
        padding: 30px;
        margin: 20px 0;
        border: 1px solid rgba(255, 71, 87, 0.2);
    }
    
    .welcome-card h3 {
        color: #ff4757;
        margin-bottom: 15px;
    }
    
    .welcome-card ul {
        color: #ccc;
    }
    
    .welcome-card li {
        margin: 8px 0;
    }
    
    /* Chat mesaj stilleri */
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 18px 24px;
        border-radius: 24px 24px 6px 24px;
        margin: 15px 0;
        max-width: 75%;
        margin-left: auto;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.35);
        font-size: 1rem;
        line-height: 1.6;
    }
    
    .bot-message {
        background: linear-gradient(135deg, #2d3436 0%, #4a5568 100%);
        color: #fff;
        padding: 18px 24px;
        border-radius: 24px 24px 24px 6px;
        margin: 15px 0;
        max-width: 75%;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.35);
        font-size: 1rem;
        line-height: 1.6;
        border-left: 4px solid #ff4757;
    }
    
    .user-label {
        color: #a0a0ff;
        font-weight: 600;
        font-size: 0.85rem;
        margin-bottom: 8px;
    }
    
    .bot-label {
        color: #ff4757;
        font-weight: 600;
        font-size: 0.85rem;
        margin-bottom: 8px;
    }
    
    /* Input stilleri */
    .stChatInput > div {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 2px solid rgba(255, 71, 87, 0.3) !important;
        border-radius: 20px !important;
    }
    
    .stChatInput input {
        color: white !important;
        font-size: 1rem !important;
    }
    
    .stChatInput input::placeholder {
        color: #888 !important;
    }
    
    /* Sidebar stilleri */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0f23 0%, #1a1a3e 100%);
    }
    
    /* Buton stilleri */
    .stButton > button {
        background: linear-gradient(135deg, #ff4757 0%, #ff6348 100%);
        color: white;
        border: none;
        border-radius: 30px;
        padding: 14px 35px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 6px 20px rgba(255, 71, 87, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(255, 71, 87, 0.6);
    }
    
    /* Özellik kartları */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 15px;
        margin: 20px 0;
    }
    
    .feature-card {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.06);
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        border-color: rgba(255, 71, 87, 0.3);
        box-shadow: 0 10px 30px rgba(255, 71, 87, 0.15);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 10px;
    }
    
    .feature-title {
        color: #fff;
        font-weight: 600;
        font-size: 1rem;
        margin-bottom: 5px;
    }
    
    .feature-desc {
        color: #888;
        font-size: 0.85rem;
    }
    
    /* Uyarı kutusu */
    .warning-box {
        background: linear-gradient(135deg, rgba(255, 165, 2, 0.1) 0%, rgba(255, 99, 72, 0.1) 100%);
        border-left: 4px solid #ffa502;
        padding: 15px 20px;
        border-radius: 0 12px 12px 0;
        margin: 20px 0;
        color: #ffa502;
        font-size: 0.95rem;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0f0f23;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #ff4757, #ffa502);
        border-radius: 10px;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #555;
        font-size: 0.8rem;
        margin-top: 40px;
        padding: 20px;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-color: #ff4757 !important;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Session state'i başlatır"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = CarExpertChatBot()


def render_chat_message(role: str, content: str):
    """Chat mesajını render eder"""
    # Markdown içeriği HTML'e dönüştür
    content_html = content.replace('\n', '<br>').replace('**', '<strong>').replace('*', '<em>')
    
    if role == "user":
        st.markdown(f"""
        <div class="user-message">
            <div class="user-label">👤 Siz</div>
            {content_html}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="bot-message">
            <div class="bot-label">🚗 Araba Uzmanı</div>
            {content_html}
        </div>
        """, unsafe_allow_html=True)


def render_welcome_section():
    """Hoş geldin bölümünü render eder"""
    st.markdown("""
    <div class="welcome-card">
        <h3>👋 Hoş Geldiniz!</h3>
        <p style="color: #aaa;">Ben araba sorunları konusunda uzman bir yapay zeka asistanıyım. 
        Aracınızla ilgili teknik sorunlarınızda size yardımcı olmak için buradayım.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-grid">
        <div class="feature-card">
            <div class="feature-icon">🔧</div>
            <div class="feature-title">Motor Sorunları</div>
            <div class="feature-desc">Motor arızaları ve çözümleri</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🛞</div>
            <div class="feature-title">Fren Sistemleri</div>
            <div class="feature-desc">Fren ve süspansiyon</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">⚡</div>
            <div class="feature-title">Elektrik & Akü</div>
            <div class="feature-desc">Elektrik sistemleri</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🌡️</div>
            <div class="feature-title">Klima & Isıtma</div>
            <div class="feature-desc">İklimlendirme sorunları</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">⚙️</div>
            <div class="feature-title">Şanzıman</div>
            <div class="feature-desc">Vites ve aktarma</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🔍</div>
            <div class="feature-title">Bakım İpuçları</div>
            <div class="feature-desc">Genel bakım tavsiyeleri</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="warning-box">
        ⚠️ <strong>Not:</strong> Ben sadece araba ve araç sorunları hakkında uzmanım. 
        Diğer konulardaki sorularınıza yanıt veremiyorum.
    </div>
    """, unsafe_allow_html=True)


def render_chat_area():
    """Ana sohbet alanını oluşturur"""
    
    # Başlık
    st.markdown('<h1 class="main-header">🚗 Araba Uzmanı ChatBot</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Arabanızla ilgili her türlü teknik soruda yanınızdayım!</p>', unsafe_allow_html=True)
    
    # Hoş geldin mesajı (sadece ilk açılışta)
    if not st.session_state.messages:
        render_welcome_section()
    
    # Chat geçmişi
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.messages:
            render_chat_message(message["role"], message["content"])
    
    # Sohbeti temizle butonu (mesaj varsa göster)
    if st.session_state.messages:
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🗑️ Sohbeti Temizle", use_container_width=True):
                st.session_state.messages = []
                st.session_state.chatbot.clear_history()
                st.rerun()
    
    # Chat input
    user_input = st.chat_input("Arabanızla ilgili sorunuzu yazın... 🚗")
    
    if user_input:
        # Kullanıcı mesajını ekle
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })
        
        # Yanıt al
        with st.spinner("🔍 Düşünüyorum..."):
            response = st.session_state.chatbot.get_response(user_input)
        
        # Bot yanıtını ekle
        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })
        
        # Sayfayı yenile
        st.rerun()
    
    # Footer
    st.markdown("""
    <div class="footer">
        🚗 Araba Uzmanı ChatBot v1.0 | Sadece araba sorunları hakkında uzman
    </div>
    """, unsafe_allow_html=True)


def main():
    """Ana uygulama fonksiyonu"""
    initialize_session_state()
    render_chat_area()


if __name__ == "__main__":
    main()
