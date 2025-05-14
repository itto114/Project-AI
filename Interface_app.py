import streamlit as st
import pandas as pd

# --- โหลดข้อมูลจาก Google Sheet ---
sheet_url = "https://docs.google.com/spreadsheets/d/1ENpJYa3tnNrv6BBZJFG9pDNUTDqkbP7RQyBnA6pKSLI/edit?usp=sharing"
csv_url = sheet_url.replace("/edit?usp=sharing", "/export?format=csv")

@st.cache_data
def load_data(url):
    return pd.read_csv(url)

df = load_data(csv_url)

# --- Header ---
st.header("🍽️ ระบบแนะนำร้านอาหาร")

# ตรวจสอบสถานะของขั้นตอน
if "step" not in st.session_state:
    st.session_state.step = "selecting"

# ขั้นตอน 1: ให้ผู้ใช้เลือกเงื่อนไข
if st.session_state.step == "selecting":
    all_types = pd.unique(pd.concat([df["type_1"], df["type_2"]]).dropna())

    user_location = st.selectbox("📍 บริเวณที่ต้องการ", df["location"].dropna().unique())
    user_type = st.selectbox("🍱 ประเภทอาหาร", all_types)
    user_budget = st.selectbox("💸 งบประมาณ", df["budget"].dropna().unique())
    user_time = st.selectbox("⏰ เวลาที่ต้องการจะไป (ร้านเปิด)", df["time_to_open"].dropna().unique())

    if st.button("🔍 ยืนยันการเลือก"):
        # กรองข้อมูล
        filtered_df = df[
            ((df["type_1"] == user_type) | (df["type_2"] == user_type)) &
            (df["location"] == user_location) &
            (df["budget"] == user_budget) &
            (df["time_to_open"] == user_time)
        ]

        if filtered_df.empty:
            st.session_state.step = "no_result"
        else:
            st.session_state.filtered_df = filtered_df
            st.session_state.step = "choosing_result"

# ขั้นตอน 2: แสดงผลลัพธ์ที่กรองได้
elif st.session_state.step == "choosing_result":
    st.subheader("🔎 ร้านอาหารที่ตรงกับความต้องการของคุณ")

    options = st.radio(
        "กรุณาเลือกร้านที่คุณสนใจ", 
        st.session_state.filtered_df["name"].tolist()
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ เลือกร้านนี้"):
            st.session_state.step = "thank_you"
    with col2:
        if st.button("❌ ไม่มีร้านไหนตรงใจ"):
            st.session_state.step = "thank_you"

# ขั้นตอน 3: ไม่พบผลลัพธ์
elif st.session_state.step == "no_result":
    st.warning("😥 ไม่พบร้านอาหารที่ตรงกับความต้องการของคุณ")
    if st.button("🔁 ลองใหม่"):
        st.session_state.step = "selecting"

# ขั้นตอน 4: หน้าขอบคุณ
elif st.session_state.step == "thank_you":
    st.success("🙏 ขอบคุณที่เข้าร่วมการทำแบบทดสอบ")
    if st.button("🔁 ทำอีกครั้ง"):
        st.session_state.step = "selecting"
