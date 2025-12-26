"""
🚗 Araba Uzmanı ChatBot - Ana Uygulama
Streamlit ile oluşturulmuş araba sorunları uzmanı ChatBot arayüzü.
"""

import streamlit as st
import os
from gemini_client import CarExpertChatBot
from document_processor import DocumentProcessor, SimpleDocumentStore
from datetime import datetime

# Sayfa yapılandırması
st.set_page_config(
    page_title="🚗 Araba Uzmanı ChatBot",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Kategori soruları
CATEGORY_QUESTIONS = {
    "motor": "Arabalarda en sık karşılaşılan motor sorunları nelerdir ve çözümleri nasıldır?",
    "fren": "Arabalarda en sık karşılaşılan fren sistemi sorunları nelerdir ve çözümleri nasıldır?",
    "elektrik": "Arabalarda en sık karşılaşılan elektrik ve akü sorunları nelerdir ve çözümleri nasıldır?",
    "klima": "Arabalarda en sık karşılaşılan klima ve ısıtma sorunları nelerdir ve çözümleri nasıldır?",
    "sanziman": "Arabalarda en sık karşılaşılan şanzıman ve vites sorunları nelerdir ve çözümleri nasıldır?",
    "bakim": "Araba bakımı için en önemli ipuçları ve yapılması gerekenler nelerdir?"
}

# Özel CSS stilleri
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a3e 50%, #2d2d5a 100%);
    }
    
    /* Sidebar stilleri */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a0a1a 0%, #151530 100%);
        border-right: 1px solid rgba(255, 71, 87, 0.2);
    }
    
    section[data-testid="stSidebar"] .stButton > button {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: #fff;
        border-radius: 12px;
        padding: 10px 15px;
        text-align: left;
        box-shadow: none;
        margin: 5px 0;
    }
    
    section[data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(255, 71, 87, 0.2);
        border-color: rgba(255, 71, 87, 0.4);
    }
    
    .sidebar-title {
        color: #ff4757;
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 20px;
        padding-bottom: 10px;
        border-bottom: 2px solid rgba(255, 71, 87, 0.3);
    }
    
    .chat-history-item {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        padding: 12px 15px;
        margin: 8px 0;
        border-left: 3px solid #ff4757;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .chat-history-item:hover {
        background: rgba(255, 71, 87, 0.1);
    }
    
    .chat-history-title {
        color: #fff;
        font-size: 0.9rem;
        font-weight: 500;
        margin-bottom: 5px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    
    .chat-history-date {
        color: #666;
        font-size: 0.75rem;
    }
    
    .main-header {
        background: linear-gradient(90deg, #ff4757, #ffa502, #ff6348);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0;
    }
    
    .sub-header {
        color: #a0a0a0;
        text-align: center;
        font-size: 1.2rem;
        margin-top: 5px;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    
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
    
    .stChatInput {
        position: relative !important;
    }
    
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
    
    .warning-box {
        background: linear-gradient(135deg, rgba(255, 165, 2, 0.1) 0%, rgba(255, 99, 72, 0.1) 100%);
        border-left: 4px solid #ffa502;
        padding: 15px 20px;
        border-radius: 0 12px 12px 0;
        margin: 20px 0;
        color: #ffa502;
        font-size: 0.95rem;
    }
    
    .footer {
        text-align: center;
        color: #555;
        font-size: 0.8rem;
        margin-top: 40px;
        padding: 20px;
    }
    
    div[data-testid="column"] .stButton > button {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 20px 15px;
        min-height: 120px;
        width: 100%;
        box-shadow: none;
    }
    
    div[data-testid="column"] .stButton > button:hover {
        background: rgba(255, 71, 87, 0.15);
        border-color: rgba(255, 71, 87, 0.4);
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(255, 71, 87, 0.2);
    }
    
    .new-chat-btn {
        background: linear-gradient(135deg, #2ed573 0%, #26de81 100%) !important;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Session state'i başlatır"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'chatbot' not in st.session_state:
        try:
            st.session_state.chatbot = CarExpertChatBot()
        except Exception as e:
            st.error(f"Gemini başlatılamadı: {e}")
            st.session_state.chatbot = None
    
    if 'show_welcome' not in st.session_state:
        st.session_state.show_welcome = True
    
    # Sohbet geçmişi için
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []  # [{id, title, messages, date}]
    
    if 'current_chat_id' not in st.session_state:
        st.session_state.current_chat_id = None
    
    # Doküman işleme için
    if 'doc_processor' not in st.session_state:
        st.session_state.doc_processor = DocumentProcessor("documents")
    
    if 'doc_store' not in st.session_state:
        st.session_state.doc_store = SimpleDocumentStore()
        # İlk yüklemede dokümanları yükle
        chunks = st.session_state.doc_processor.get_document_chunks()
        st.session_state.doc_store.add_documents(chunks)




def get_chat_title(messages):
    """Sohbetin ilk mesajından başlık oluşturur"""
    if messages:
        first_msg = messages[0]["content"]
        return first_msg[:40] + "..." if len(first_msg) > 40 else first_msg
    return "Yeni Sohbet"


def save_current_chat():
    """Mevcut sohbeti geçmişe kaydeder"""
    if st.session_state.messages:
        chat_data = {
            "id": st.session_state.current_chat_id or datetime.now().strftime("%Y%m%d%H%M%S"),
            "title": get_chat_title(st.session_state.messages),
            "messages": st.session_state.messages.copy(),
            "date": datetime.now().strftime("%d.%m.%Y %H:%M")
        }
        
        # Eğer mevcut chat varsa güncelle, yoksa ekle
        existing_idx = None
        for i, chat in enumerate(st.session_state.chat_history):
            if chat["id"] == chat_data["id"]:
                existing_idx = i
                break
        
        if existing_idx is not None:
            st.session_state.chat_history[existing_idx] = chat_data
        else:
            st.session_state.chat_history.insert(0, chat_data)


def load_chat(chat_id):
    """Geçmişten sohbet yükler"""
    for chat in st.session_state.chat_history:
        if chat["id"] == chat_id:
            st.session_state.messages = chat["messages"].copy()
            st.session_state.current_chat_id = chat_id
            st.session_state.show_welcome = False
            return True
    return False


def start_new_chat():
    """Yeni sohbet başlatır"""
    # Mevcut sohbeti kaydet
    save_current_chat()
    
    # Yeni sohbet
    st.session_state.messages = []
    st.session_state.current_chat_id = datetime.now().strftime("%Y%m%d%H%M%S")
    st.session_state.show_welcome = True
    st.session_state.chatbot.clear_history()


def delete_chat(chat_id):
    """Sohbeti siler"""
    st.session_state.chat_history = [c for c in st.session_state.chat_history if c["id"] != chat_id]
    if st.session_state.current_chat_id == chat_id:
        start_new_chat()


def render_sidebar():
    """Sol panel - Sohbet Geçmişi"""
    with st.sidebar:
        st.markdown('<div class="sidebar-title">💬 Sohbet Geçmişi</div>', unsafe_allow_html=True)
        
        # Yeni sohbet butonu
        if st.button("➕ Yeni Sohbet", key="new_chat", use_container_width=True):
            start_new_chat()
            st.rerun()
        
        st.markdown("---")
        
        # Sohbet geçmişi listesi
        if st.session_state.chat_history:
            for chat in st.session_state.chat_history:
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    # Aktif sohbeti vurgula
                    is_active = chat["id"] == st.session_state.current_chat_id
                    btn_label = f"{'🔸 ' if is_active else '💬 '}{chat['title'][:25]}..."
                    
                    if st.button(btn_label, key=f"chat_{chat['id']}", use_container_width=True):
                        save_current_chat()
                        load_chat(chat["id"])
                        st.rerun()
                
                with col2:
                    if st.button("🗑️", key=f"del_{chat['id']}"):
                        delete_chat(chat["id"])
                        st.rerun()
                
                st.caption(f"📅 {chat['date']}")
        else:
            st.markdown("""
            <div style="color: #666; text-align: center; padding: 20px;">
                <p>Henüz sohbet geçmişi yok</p>
                <p style="font-size: 0.8rem;">Yeni bir sohbet başlatın!</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Doküman Yönetimi
        st.markdown('<div class="sidebar-title">📄 Dokümanlar</div>', unsafe_allow_html=True)
        
        # Doküman yükleme
        uploaded_files = st.file_uploader(
            "Doküman Yükle",
            type=['pdf', 'docx', 'xlsx'],
            accept_multiple_files=True,
            help="PDF, DOCX veya XLSX dosyaları yükleyin",
            key="doc_uploader"
        )
        
        if uploaded_files:
            for uploaded_file in uploaded_files:
                file_path = os.path.join("documents", uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
            st.success(f"✅ {len(uploaded_files)} dosya yüklendi!")
            # Dokümanları yeniden yükle
            chunks = st.session_state.doc_processor.get_document_chunks()
            st.session_state.doc_store.clear()
            st.session_state.doc_store.add_documents(chunks)
            st.rerun()
        
        # Dokümanları yenile butonu
        if st.button("🔄 Dokümanları Yenile", key="reload_docs", use_container_width=True):
            chunks = st.session_state.doc_processor.get_document_chunks()
            st.session_state.doc_store.clear()
            st.session_state.doc_store.add_documents(chunks)
            st.success(f"✅ {len(chunks)} parça yüklendi!")
            st.rerun()
        
        # Doküman istatistikleri
        doc_count = len(st.session_state.doc_store.documents)
        if doc_count > 0:
            st.caption(f"📊 {doc_count} doküman parçası yüklü")
        
        st.markdown("---")
        
        # Tüm geçmişi temizle
        if st.session_state.chat_history:
            if st.button("🗑️ Tüm Geçmişi Temizle", key="clear_all", use_container_width=True):
                st.session_state.chat_history = []
                start_new_chat()
                st.rerun()


def render_chat_message(role: str, content: str):
    """Chat mesajını render eder"""
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


def send_message(message: str, doc_context: str = ""):
    """Mesaj gönderir"""
    st.session_state.show_welcome = False
    
    if st.session_state.current_chat_id is None:
        st.session_state.current_chat_id = datetime.now().strftime("%Y%m%d%H%M%S")
    
    # Doküman bağlamı varsa mesaja ekle
    if doc_context:
        message_with_context = f"{message}\n\n📚 Dokümanlardan Bilgiler:\n{doc_context}"
    else:
        message_with_context = message
    
    st.session_state.messages.append({
        "role": "user",
        "content": message_with_context
    })


def main():
    """Ana uygulama fonksiyonu"""
    initialize_session_state()
    
    # Sidebar - Sohbet Geçmişi
    render_sidebar()
    
    # Başlık
    st.markdown('<h1 class="main-header">🚗 Araba Uzmanı ChatBot</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Arabanızla ilgili her türlü teknik soruda yanınızdayım!</p>', unsafe_allow_html=True)
    
    # Welcome Section
    if st.session_state.show_welcome and not st.session_state.messages:
        st.markdown("""
        <div class="welcome-card">
            <h3>👋 Hoş Geldiniz!</h3>
            <p style="color: #aaa;">Ben araba sorunları konusunda uzman bir yapay zeka asistanıyım. 
            Aracınızla ilgili teknik sorunlarınızda size yardımcı olmak için buradayım. 
            Aşağıdaki kategorilere tıklayarak sık karşılaşılan sorunları öğrenebilirsiniz.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔧\n\nMotor Sorunları", key="btn_motor", use_container_width=True):
                category = "motor"
                question = CATEGORY_QUESTIONS[category]
                # Dokümanlardan bilgi çek
                doc_context = st.session_state.doc_store.get_category_context(category)
                send_message(question, doc_context)
                st.rerun()
        
        with col2:
            if st.button("🛞\n\nFren Sistemleri", key="btn_fren", use_container_width=True):
                category = "fren"
                question = CATEGORY_QUESTIONS[category]
                doc_context = st.session_state.doc_store.get_category_context(category)
                send_message(question, doc_context)
                st.rerun()
        
        with col3:
            if st.button("⚡\n\nElektrik & Akü", key="btn_elektrik", use_container_width=True):
                category = "elektrik"
                question = CATEGORY_QUESTIONS[category]
                doc_context = st.session_state.doc_store.get_category_context(category)
                send_message(question, doc_context)
                st.rerun()
        
        col4, col5, col6 = st.columns(3)
        
        with col4:
            if st.button("🌡️\n\nKlima & Isıtma", key="btn_klima", use_container_width=True):
                category = "klima"
                question = CATEGORY_QUESTIONS[category]
                doc_context = st.session_state.doc_store.get_category_context(category)
                send_message(question, doc_context)
                st.rerun()
        
        with col5:
            if st.button("⚙️\n\nŞanzıman", key="btn_sanziman", use_container_width=True):
                category = "sanziman"
                question = CATEGORY_QUESTIONS[category]
                doc_context = st.session_state.doc_store.get_category_context(category)
                send_message(question, doc_context)
                st.rerun()
        
        with col6:
            if st.button("🔍\n\nBakım İpuçları", key="btn_bakim", use_container_width=True):
                category = "bakim"
                question = CATEGORY_QUESTIONS[category]
                doc_context = st.session_state.doc_store.get_category_context(category)
                send_message(question, doc_context)
                st.rerun()
        
        st.markdown("""
        <div class="warning-box">
            ⚠️ <strong>Not:</strong> Ben sadece araba ve araç sorunları hakkında uzmanım. 
            Diğer konulardaki sorularınıza yanıt veremiyorum.
        </div>
        """, unsafe_allow_html=True)
    
    # Chat Section
    if st.session_state.messages:
        for message in st.session_state.messages:
            render_chat_message(message["role"], message["content"])
        
        # Son mesaj user ise yanıt al
        if st.session_state.messages[-1]["role"] == "user":
            user_msg = st.session_state.messages[-1]["content"]
            
            # Chatbot instance'ını kontrol et
            if not st.session_state.chatbot:
                st.error("❌ Gemini modeli başlatılamadı. Lütfen API anahtarınızı kontrol edin.")
                st.stop()
            
            with st.spinner("🔍 Düşünüyorum..."):
                response = st.session_state.chatbot.get_response(user_msg)
            
            st.session_state.messages.append({
                "role": "assistant",
                "content": response
            })
            
            # Sohbeti kaydet
            save_current_chat()
            st.rerun()
        
        # Sohbeti temizle butonu
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🗑️ Sohbeti Temizle", use_container_width=True):
                st.session_state.messages = []
                st.session_state.show_welcome = True
                if st.session_state.chatbot:
                    st.session_state.chatbot.clear_history()
                st.session_state.current_chat_id = None
                st.rerun()
    
    # Chat input
    user_input = st.chat_input("Arabanızla ilgili sorunuzu yazın... 🚗")
    
    if user_input:
        # Chatbot instance'ını kontrol et
        if not st.session_state.chatbot:
            st.error("❌ Gemini modeli başlatılamadı. Lütfen API anahtarınızı kontrol edin.")
        else:
            # Dokümanlardan ilgili bilgiyi çek
            doc_context = st.session_state.doc_store.get_context(user_input)
            send_message(user_input, doc_context)
            st.rerun()
    
    # Footer
    st.markdown("""
    <div class="footer">
        🚗 Araba Uzmanı ChatBot 
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
