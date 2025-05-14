import streamlit as st
import pandas as pd

# --- โหลดข้อมูลจาก Google Sheet ---
sheet_url = "https://docs.google.com/spreadsheets/d/1ENpJYa3tnNrv6BBZJFG9pDNUTDqkbP7RQyBnA6pKSLI/edit?usp=sharing"
csv_url = sheet_url.replace("/edit?usp=sharing", "/export?format=csv")

@st.cache_data
def load_data(url):
    return pd.read_csv(url)

df = load_data(csv_url)

# --- แสดงคอลัมน์ที่มีใน DataFrame ---
st.write("🧪 คอลัมน์ทั้งหมดในไฟล์:", df.columns.tolist())

# --- UI เลือกข้อมูลจากผู้ใช้ ---
st.header("🍽️ ระบบแนะนำร้านอาหาร")

# สร้างตัวเลือกประเภทอาหารจากทั้งสองคอลัมน์
all_types = pd.unique(pd.concat([df["type_1"], df["type_2"]]).dropna())

# สร้าง session state เพื่อเก็บสถานะการเลือก
if "step" not in st.session_state:
    st.session_state.step = 1  # เริ่มต้นที่ขั้นตอนแรก

if "selected_results" not in st.session_state:
    st.session_state.selected_results = []

# --- Step 1: เลือกข้อมูลจากผู้ใช้ ---
if st.session_state.step == 1:
    # ให้ผู้ใช้เลือกข้อมูลที่ต้องการ
    user_location = st.selectbox("📍 บริเวณที่ต้องการ", df["location"].dropna().unique())
    user_type = st.selectbox("🍱 ประเภทอาหาร", all_types)
    user_budget = st.selectbox("💸 งบประมาณ", df["budget"].dropna().unique())
    user_time = st.selectbox("⏰ เวลาที่ต้องการจะไป (ร้านเปิด)", df["time_to_open"].dropna().unique())

    # ปุ่มยืนยันเลือกข้อมูล
    if st.button("ยืนยันการเลือก"):
        # กรองข้อมูลจากเงื่อนไขที่เลือก
        filtered_df = df[
            (df["type_1"] == user_type) | 
            (df["type_2"] == user_type)
        ]
        filtered_df = filtered_df[
            (filtered_df["location"] == user_location) &
            (filtered_df["budget"] == user_budget) &
            (filtered_df["time_to_open"] == user_time)
        ]

        # หากพบผลลัพธ์ที่ตรงกับเงื่อนไข
        if not filtered_df.empty:
            st.session_state.selected_results = filtered_df
            st.session_state.step = 2  # เปลี่ยนไปขั้นตอนการแสดงผลลัพธ์
        else:
            st.warning("ไม่พบร้านอาหารที่ตรงกับความต้องการของคุณ")
            st.session_state.step = 3  # ถ้าไม่มีผลลัพธ์ เปลี่ยนไปขั้นตอนที่ 3 (ไม่มีร้านตรงใจ)
        
# --- Step 2: แสดงผลลัพธ์ที่ตรงกับเงื่อนไข ---
if st.session_state.step == 2:
    st.subheader("ร้านอาหารที่ตรงกับเงื่อนไขของคุณ:")
    for index, row in st.session_state.selected_results.iterrows():
        st.markdown(f"- **{row['name']}** ({row['type_1']} / {row['type_2']})")
    
    if st.button("เลือกแล้ว"):
        st.session_state.step = 4  # ถ้าเลือกแล้ว ไปที่หน้า "ขอบคุณ"
    
    if st.button("ไม่มีร้านตรงใจ"):
        st.session_state.step = 1  # กลับไปที่การเลือกข้อมูลใหม่

# --- Step 3: ไม่มีร้านตรงใจ ---
if st.session_state.step == 3:
    st.subheader("😥 ไม่มีร้านอาหารที่ตรงกับความต้องการของคุณ")
    if st.button("ลองใหม่"):
        st.session_state.step = 1  # กลับไปที่การเลือกข้อมูลใหม่

# --- Step 4: ขอบคุณที่เข้าร่วม ---
if st.session_state.step == 4:
    st.subheader("🙏 ขอบคุณที่เข้าร่วมการทำแบบทดสอบ!")
    if st.button("ทำอีกครั้ง"):
        st.session_state.step = 1  # กลับไปที่การเลือกข้อมูลใหม่
