import streamlit as st
import pandas as pd

# --- โหลดข้อมูลจาก Google Sheet ---
sheet_url = "https://docs.google.com/spreadsheets/d/1ENpJYa3tnNrv6BBZJFG9pDNUTDqkbP7RQyBnA6pKSLI/edit?usp=sharing"
csv_url = sheet_url.replace("/edit?usp=sharing", "/export?format=csv")

@st.cache_data
def load_data(url):
    return pd.read_csv(url)

# โหลดข้อมูล
df = load_data(csv_url)

# --- หน้าแรก ---
st.header("🍽️ ระบบแนะนำร้านอาหาร")

# ตรวจสอบว่ามีการกดเริ่มใหม่หรือยัง
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "selected_result" not in st.session_state:
    st.session_state.selected_result = None

# --- แบบฟอร์มเลือกเงื่อนไข ---
if not st.session_state.submitted:
    with st.form("input_form"):
        all_types = pd.unique(pd.concat([df["type_1"], df["type_2"]]).dropna())

        user_location = st.selectbox("📍 บริเวณที่ต้องการ", df["location"].dropna().unique())
        user_type = st.selectbox("🍱 ประเภทอาหาร", all_types)
        user_budget = st.selectbox("💸 งบประมาณ", df["budget"].dropna().unique())
        user_time = st.selectbox("⏰ เวลาที่ต้องการจะไป (ร้านเปิด)", df["time_to_open"].dropna().unique())

        submitted = st.form_submit_button("✅ ยืนยัน")

    if submitted:
        st.session_state.submitted = True
        st.session_state.user_input = {
            "location": user_location,
            "type": user_type,
            "budget": user_budget,
            "time_to_open": user_time,
        }

# --- แสดงผลลัพธ์หลังการยืนยัน ---
if st.session_state.submitted and st.session_state.selected_result is None:
    user_input = st.session_state.user_input
    filtered_df = df[
        ((df["type_1"] == user_input["type"]) | (df["type_2"] == user_input["type"])) &
        (df["location"] == user_input["location"]) &
        (df["budget"] == user_input["budget"]) &
        (df["time_to_open"] == user_input["time_to_open"])
    ]

    if not filtered_df.empty:
        st.subheader("📋 กรุณาเลือกร้านอาหารที่ตรงใจคุณ:")

        selected = st.radio(
            "เลือกร้านที่ต้องการ",
            filtered_df["name"].tolist() + ["ไม่มีร้านไหนตรงใจ"]
        )

        if st.button("👉 ยืนยันร้านที่เลือก"):
            st.session_state.selected_result = selected

    else:
        st.warning("😥 ไม่พบร้านอาหารที่ตรงกับความต้องการของคุณ")
        if st.button("ไม่มีร้านไหนตรงใจ"):
            st.session_state.selected_result = "ไม่มีร้านไหนตรงใจ"

# --- แสดงหน้าขอบคุณ ---
if st.session_state.selected_result is not None:
    st.success("🎉 ขอบคุณที่เข้าร่วมการทำแบบทดสอบ!")
    if st.session_state.selected_result != "ไม่มีร้านไหนตรงใจ":
        st.markdown(f"คุณเลือกร้าน: **{st.session_state.selected_result}**")
    else:
        st.markdown("คุณเลือกว่าไม่มีร้านไหนตรงใจ")

    if st.button("🔁 ทำอีกครั้ง"):
        st.session_state.submitted = False
        st.session_state.selected_result = None
        st.experimental_rerun()
