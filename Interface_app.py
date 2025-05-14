import streamlit as st
import pandas as pd

# --- โหลดข้อมูลจาก Google Sheet ---
sheet_url = "https://docs.google.com/spreadsheets/d/1ENpJYa3tnNrv6BBZJFG9pDNUTDqkbP7RQyBnA6pKSLI/edit?usp=sharing"
csv_url = sheet_url.replace("/edit?usp=sharing", "/export?format=csv")

@st.cache_data(ttl=300)
def load_data(url):
    return pd.read_csv(url)

df = load_data(csv_url)

# --- กำหนดค่า default ใน session_state ---
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "selected_result" not in st.session_state:
    st.session_state.selected_result = None
if "user_input" not in st.session_state:
    st.session_state.user_input = {}

# --- ส่วนของการรีเซ็ต ---
def reset_all():
    st.session_state.submitted = False
    st.session_state.selected_result = None
    st.session_state.user_input = {}

# --- UI หลัก ---
st.title("🍽️ ระบบแนะนำร้านอาหาร")

# --- แบบฟอร์มให้ผู้ใช้กรอกตัวเลือก ---
if not st.session_state.submitted:
    with st.form("input_form"):
        st.markdown("### 🔍 กรุณาเลือกความต้องการของคุณ")

        user_location = st.selectbox("📍 บริเวณที่ต้องการ", df["location"].dropna().unique())
        all_types = pd.unique(pd.concat([df["type_1"], df["type_2"]]).dropna())
        user_type = st.selectbox("🍱 ประเภทอาหาร", all_types)
        user_budget = st.selectbox("💸 งบประมาณ", df["budget"].dropna().unique())
        user_time = st.selectbox("⏰ เวลาที่ต้องการไป (ร้านเปิด)", df["time_to_open"].dropna().unique())

        submitted = st.form_submit_button("✅ ยืนยัน")

    if submitted:
        st.session_state.user_input = {
            "location": user_location,
            "type": user_type,
            "budget": user_budget,
            "time_to_open": user_time,
        }
        st.session_state.submitted = True
        st.experimental_rerun()

# --- หลังจากกด "ยืนยัน" แล้ว ---
if st.session_state.submitted and not st.session_state.selected_result:
    user_input = st.session_state.user_input

    # กรองข้อมูล
    filtered_df = df[
        ((df["type_1"] == user_input["type"]) | (df["type_2"] == user_input["type"])) &
        (df["location"] == user_input["location"]) &
        (df["budget"] == user_input["budget"]) &
        (df["time_to_open"] == user_input["time_to_open"])
    ]

    if not filtered_df.empty:
        st.subheader("🎯 กรุณาเลือกร้านอาหารที่ตรงใจคุณ:")

        for i, row in filtered_df.iterrows():
            if st.button(f"เลือก: {row['name']} ({row['type_1']} / {row['type_2']})", key=f"select_{i}"):
                st.session_state.selected_result = row['name']
                st.experimental_rerun()

        st.button("❌ ไม่มีร้านไหนตรงใจ", on_click=lambda: st.session_state.update(selected_result="none"))
    else:
        st.warning("😥 ไม่พบร้านอาหารที่ตรงกับความต้องการของคุณ")
        st.button("❌ ไม่มีร้านไหนตรงใจ", on_click=lambda: st.session_state.update(selected_result="none"))

# --- แสดงหน้าขอบคุณ ---
if st.session_state.selected_result:
    st.success("🙏 ขอบคุณที่เข้าร่วมการทำแบบทดสอบ")
    if st.session_state.selected_result != "none":
        st.write(f"คุณเลือกร้าน: **{st.session_state.selected_result}**")
    else:
        st.write("คุณไม่ได้เลือกร้านใดเลย")

    if st.button("🔁 ทำอีกครั้ง"):
        reset_all()
        st.experimental_rerun()
