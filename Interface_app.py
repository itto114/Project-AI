import streamlit as st
import pandas as pd

# --- โหลดข้อมูลจาก Google Sheet ---
sheet_url = "https://docs.google.com/spreadsheets/d/1ENpJYa3tnNrv6BBZJFG9pDNUTDqkbP7RQyBnA6pKSLI/edit?usp=sharing"
csv_url = sheet_url.replace("/edit?usp=sharing", "/export?format=csv")

@st.cache_data(ttl=300)
def load_data():
    return pd.read_csv(csv_url)

# --- โหลดข้อมูล ---
if "data" not in st.session_state:
    st.session_state.data = load_data()

df = st.session_state.data

# --- UI โหลดข้อมูลใหม่แบบแมนนวล ---
if st.button("🔄 รีโหลดข้อมูลจาก Google Sheet"):
    st.session_state.data = load_data()
    st.success("โหลดข้อมูลใหม่เรียบร้อยแล้ว!")
    st.experimental_rerun()

# --- Session State สำหรับควบคุมการแสดงผล ---
if "submitted" not in st.session_state:
    st.session_state.submitted = False

if "selected_result" not in st.session_state:
    st.session_state.selected_result = None

# --- หากยังไม่ยืนยัน ให้แสดงแบบฟอร์ม ---
if not st.session_state.submitted:
    st.header("🍽️ ระบบแนะนำร้านอาหาร")

    with st.form("input_form"):
        all_types = pd.unique(pd.concat([df["type_1"], df["type_2"]]).dropna())

        user_location = st.selectbox("📍 บริเวณที่ต้องการ", df["location"].dropna().unique())
        user_type = st.selectbox("🍱 ประเภทอาหาร", all_types)
        user_budget = st.selectbox("💸 งบประมาณ", df["budget"].dropna().unique())
        user_time = st.selectbox("⏰ เวลาที่ต้องการจะไป (ร้านเปิด)", df["time_to_open"].dropna().unique())

        submitted = st.form_submit_button("✅ ยืนยัน")

        if submitted:
            # เก็บค่าไว้ใน session_state แล้ว rerun เพื่อแสดงผลลัพธ์ทันที
            st.session_state.user_input = {
                "location": user_location,
                "type": user_type,
                "budget": user_budget,
                "time_to_open": user_time,
            }
            st.session_state.submitted = True
            st.experimental_rerun()

# --- หากยืนยันแล้ว แสดงผลลัพธ์ที่กรองได้ ---
elif st.session_state.submitted and st.session_state.selected_result is None:
    user_input = st.session_state.user_input

    filtered_df = df[
        ((df["type_1"] == user_input["type"]) | (df["type_2"] == user_input["type"])) &
        (df["location"] == user_input["location"]) &
        (df["budget"] == user_input["budget"]) &
        (df["time_to_open"] == user_input["time_to_open"])
    ]

    st.subheader("📋 ผลลัพธ์ร้านอาหารที่ตรงกับเงื่อนไขของคุณ:")

    if not filtered_df.empty:
        for idx, row in filtered_df.iterrows():
            if st.button(f"เลือก: {row['name']}", key=f"result_{idx}"):
                st.session_state.selected_result = row['name']
                st.experimental_rerun()
    else:
        st.warning("😥 ไม่พบร้านอาหารที่ตรงกับความต้องการของคุณ")

    if st.button("❌ ไม่มีร้านไหนตรงใจ"):
        st.session_state.selected_result = "none"
        st.experimental_rerun()

# --- หน้าขอบคุณหลังเลือกผลลัพธ์ ---
elif st.session_state.selected_result is not None:
    st.header("🙏 ขอบคุณที่เข้าร่วมการทำแบบทดสอบ")

    if st.session_state.selected_result != "none":
        st.success(f"คุณเลือก: {st.session_state.selected_result}")
    else:
        st.info("คุณระบุว่าไม่มีร้านที่ตรงใจ")

    if st.button("🔁 ทำอีกครั้ง"):
        for key in ["submitted", "selected_result", "user_input"]:
            st.session_state.pop(key, None)
        st.experimental_rerun()
