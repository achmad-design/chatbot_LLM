import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_groq import ChatGroq

# ==========================================
# 1. KONFIGURASI HALAMAN & CUSTOM CSS
# ==========================================
st.set_page_config(
    page_title="EduBot - Asisten Belajar Pintar",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS untuk mempercantik UI Pendidikan
st.markdown(
    """
    <style>
    /* Styling utama area obrolan */
    .stChatMessage {
        border-radius: 12px;
        padding: 12px 16px;
        margin-bottom: 10px;
    }
    
    /* Header Kustom */
    .edu-header {
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
        padding: 24px;
        border-radius: 16px;
        color: white;
        margin-bottom: 24px;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    .edu-header h1 {
        color: white !important;
        margin: 0;
        font-weight: 700;
        font-size: 2.2rem;
    }
    
    .edu-header p {
        color: #E0E7FF !important;
        margin-top: 8px;
        font-size: 1rem;
    }

    /* Card untuk rekomendasi pertanyaan */
    .suggested-card {
        background-color: #F3F4F6;
        border: 1px solid #E5E7EB;
        border-radius: 10px;
        padding: 12px;
        font-size: 0.9rem;
        color: #374151;
        text-align: center;
        cursor: pointer;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==========================================
# 2. SIDEBAR (KONFIGURASI & API KEY)
# ==========================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3429/3429402.png", width=80)
    st.title("🎓 Pengaturan EduBot")
    st.caption("Asisten AI Interaktif untuk Pembelajaran")

    st.divider()

    # Input API Key
    api_key = st.text_input(
        "Groq API Key",
        type="password",
        placeholder="gsk_...",
        help="Dapatkan API Key gratis di console.groq.com",
    )

    # Pilihan Mata Pelajaran / Mode Tutor
    subject = st.selectbox(
        "Pilih Bidang Studi:",
        [
            "Sains & Matematika 🔬",
            "Bahasa & Sastra 📝",
            "Pengodingan & Teknologi 💻",
            "Tutor Umum / Kritis 💡",
        ],
    )

    # Pilihan Model
    model_name = st.selectbox(
        "Pilih Model AI:",
        ["groq/compound", "openai/gpt-oss-20b", "whisper-large-v3-turbo"],
        index=0,
    )

    st.divider()

    # Tombol Bersihkan Chat
    if st.button("🗑️ Hapus Riwayat Chat", use_container_width=True):
        st.session_state["chat_history"] = []
        st.rerun()

    st.markdown(
        "<div style='text-align: center; color: gray; font-size: 0.8rem; margin-top: 20px;'>"
        "Dikembangkan untuk Proyek Pendidikan Achmad"
        "</div>",
        unsafe_allow_html=True,
    )

# Validasi API Key
if not api_key:
    st.info("👈 Silakan masukkan **Groq API Key** Anda di sidebar untuk memulai pembelajaran.", icon="🔑")
    st.stop()

# Set prompt sistem berdasarkan subjek yang dipilih
system_prompts = {
    "Sains & Matematika 🔬": "Anda adalah seorang guru Sains dan Matematika yang sabar, analitis, dan pandai memberikan analogi visual sederhana.",
    "Bahasa & Sastra 📝": "Anda adalah ahli Bahasa dan Sastra yang membantu tata bahasa, kosa kata, serta penulisan kreatif secara interaktif.",
    "Pengodingan & Teknologi 💻": "Anda adalah mentor pemrograman yang menjelaskan kode langkah demi langkah dan menerapkan praktek terbaik.",
    "Tutor Umum / Kritis 💡": "Anda adalah tutor sokratik yang ramah, mendorong pemikiran kritis, dan membantu menjawab pertanyaan dengan jelas.",
}

# ==========================================
# 3. INISIALISASI SESSION STATE
# ==========================================
if "chat_history" not in st.session_state or len(st.session_state["chat_history"]) == 0:
    st.session_state["chat_history"] = [SystemMessage(content=system_prompts[subject])]

# Update system message jika pengguna mengubah subjek di tengah jalan
st.session_state["chat_history"][0] = SystemMessage(content=system_prompts[subject])

# ==========================================
# 4. HEADER UTAMA & WELCOME UI
# ==========================================
st.markdown(
    """
    <div class="edu-header">
        <h1>🎓 EduBot: Ruang Belajar AI</h1>
        <p>Tanyakan konsep sulit, minta penjelasan rumus, atau diskusikan topik apapun!</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Tampilkan ucapan selamat datang jika belum ada interaksi pengguna
if len(st.session_state["chat_history"]) <= 1:
    st.subheader("💡 Pertanyaan Pemantik untuk Memulai:")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("**Sains:**\n\n'Jelaskan proses fotosintesis dengan analogi pembuatan kue!'")
    with col2:
        st.info("**Matematika:**\n\n'Bagaimana cara cepat memahami Rumus Pythagoras?'")
    with col3:
        st.info("**Koding:**\n\n'Apa perbedaan mendasar antara list dan dictionary di Python?'")

# ==========================================
# 5. RIWAYAT CHAT & PERCAKAPAN
# ==========================================
# Inisialisasi Klien ChatGroq
client = ChatGroq(model=model_name, api_key=api_key)

# Tampilkan pesan yang tersimpan
for msg in st.session_state["chat_history"]:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user", avatar="🎒"):
            st.markdown(msg.content)
    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(msg.content)

# Input Chat Pengguna
user_prompt = st.chat_input("Ketik pertanyaan atau topik pembelajaran di sini...")

if user_prompt:
    # Tampilkan input pengguna
    with st.chat_message("user", avatar="🎒"):
        st.markdown(user_prompt)

    # Tambahkan ke riwayat
    st.session_state["chat_history"].append(HumanMessage(content=user_prompt))

    # Respon AI dengan Streaming
    with st.chat_message("assistant", avatar="🤖"):
        # Menggunakan stream untuk memberikan efek respons realtime
        stream = client.stream(st.session_state["chat_history"])
        response_content = st.write_stream(stream)

    # Simpan jawaban AI ke riwayat
    st.session_state["chat_history"].append(AIMessage(content=response_content))
