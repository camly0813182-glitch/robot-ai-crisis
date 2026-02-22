import streamlit as st
import google.generativeai as genai

# 1. CẤU HÌNH BỘ NÃO AI
# Thay dãy chữ dưới đây bằng API Key của bạn nếu nó thay đổi
genai.configure(api_key="AIzaSyAPr01OtkLHaNMXYc3nYRRbBuePtFE03OQ")

# 2. THIẾT LẬP GIAO DIỆN
st.set_page_config(page_title="Crisis AI Agent", page_icon="🤖")

# CSS để khung chat bo tròn và sidebar đẹp hơn
st.markdown("""
    <style>
    .stChatMessage { border-radius: 15px; border: 1px solid #ddd; margin-bottom: 10px; }
    [data-testid="stSidebar"] { background-color: #f0f2f6; }
    </style>
    """, unsafe_allow_html=True)

# 3. THANH ĐIỀU KHIỂN BÊN TRÁI (SIDEBAR)
with st.sidebar:
    st.header("⚙️ Cấu hình kịch bản")
    tinh_huong = st.selectbox("🎯 Tình huống:", 
                             ["Sản phẩm có dị vật", "Nhân viên thô lỗ", "Giao hàng chậm 5 ngày"])
    muc_do = st.select_slider("🔥 Mức độ giận dữ:", 
                             options=["Nhẹ nhàng", "Bực bội", "Cực đoan"])
    if st.button("🗑️ Xóa hội thoại cũ"):
        st.session_state.messages = []
        st.rerun()

# 4. KHU VỰC HIỂN THỊ CHAT
st.title("🤖 Crisis Simulation Bot")
st.info(f"Kịch bản: {tinh_huong} | Thái độ khách hàng: {muc_do}")

# Khởi tạo bộ nhớ tin nhắn
if "messages" not in st.session_state:
    st.session_state.messages = []

# Vẽ lại các tin nhắn đã chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 5. XỬ LÝ NHẬP LIỆU VÀ PHẢN HỒI AI
if prompt := st.chat_input("Bạn sẽ giải quyết thế nào?"):
    # Hiển thị tin nhắn người dùng
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Gọi AI suy nghĩ
    with st.spinner("Khách hàng đang soạn câu trả lời..."):
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Chỉ dẫn AI đóng vai
        huong_dan = f"""
        Bạn là khách hàng Việt Nam đang gặp sự cố: {tinh_huong}.
        Thái độ của bạn đang rất {muc_do}.
        Hãy phản hồi lại nhân viên một cách đanh đá, thực tế, ngắn gọn (dưới 2 câu).
        Không được đồng ý ngay lập tức, hãy làm khó nhân viên.
        """
        
        response = model.generate_content(huong_dan + prompt)
        ai_reply = response.text

    # Hiển thị câu trả lời của AI
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
    with st.chat_message("assistant"):
        st.write(ai_reply)