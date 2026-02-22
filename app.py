import streamlit as st
import google.generativeai as genai

# 1. CẤU HÌNH AI - Dán mã của bạn vào giữa dấu ""
genai.configure(api_key="AIzaSyAPr01OtkLHaNMXYc3nYRRbBuePtFE03OQ")

# 2. GIAO DIỆN ĐẸP
st.set_page_config(page_title="Crisis Bot 2.0", page_icon="🛡️")

st.markdown("""
    <style>
    .stChatMessage { border-radius: 15px; border: 1px solid #ddd; }
    [data-testid="stSidebar"] { background-color: #f0f2f6; }
    </style>
    """, unsafe_allow_html=True)

# 3. THANH ĐIỀU KHIỂN (SIDEBAR)
with st.sidebar:
    st.title("⚙️ Cấu hình")
    tinh_huong = st.selectbox("🎯 Kịch bản:", ["Sản phẩm lỗi", "Nhân viên thô lỗ", "Dịch vụ chậm"])
    muc_do = st.select_slider("🔥 Độ giận dữ:", options=["Thấp", "Vừa", "Cao", "Cực đoan"])
    if st.button("🔄 Làm mới"):
        st.session_state.messages = []
        st.rerun()

# 4. KHU VỰC CHAT
st.title("🛡️ Crisis Simulation Bot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("Bạn sẽ giải quyết thế nào?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # GỌI AI THÔNG MINH
    try:
        model = genai.GenerativeModel('gemini-1.5-flash') # Tên chuẩn nhất
        context = f"Bạn là khách hàng VN đang {muc_do} giận dữ vì {tinh_huong}. Phản hồi đanh đá, ngắn gọn câu này: {prompt}"
        
        response = model.generate_content(context)
        ai_reply = response.text
        
        st.session_state.messages.append({"role": "assistant", "content": ai_reply})
        with st.chat_message("assistant"):
            st.write(ai_reply)
    except Exception as e:
        st.error(f"Lỗi rồi: {e}")