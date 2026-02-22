import streamlit as st
import google.generativeai as genai

# 1. CẤU HÌNH API
genai.configure(api_key="AIzaSyAPr01OtkLHaNMXYc3nYRRbBuePtFE03OQ")

# 2. GIAO DIỆN
st.set_page_config(page_title="Robot Khủng Hoảng", page_icon="🤖")

# 3. SIDEBAR
with st.sidebar:
    st.title("⚙️ Cấu hình")
    tinh_huong = st.selectbox("🎯 Tình huống:", ["Sản phẩm lỗi", "Nhân viên thô lỗ", "Dịch vụ chậm"])
    muc_do = st.select_slider("🔥 Giận dữ:", options=["Thấp", "Vừa", "Cao", "Cực đoan"])

# 4. CHAT
st.title("🤖 Crisis Simulation AI")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Giải quyết thế nào đây?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    try:
        # DÙNG GEMINI-PRO ĐỂ KHÔNG BỊ LỖI NOTFOUND
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(f"Đóng vai khách hàng {muc_do} giận dữ vì {tinh_huong}. Trả lời đanh đá câu này: {prompt}")
        
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        with st.chat_message("assistant"):
            st.write(response.text)
    except Exception as e:
        st.error(f"Lỗi AI: {e}")
