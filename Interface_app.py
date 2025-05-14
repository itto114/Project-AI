import streamlit as st
import pandas as pd

# --- โหลดข้อมูลจาก Google Sheet ---
sheet_url = "https://docs.google.com/spreadsheets/d/1ENpJYa3tnNrv6BBZJFG9pDNUTDqkbP7RQyBnA6pKSLI/edit#gid=0"
csv_url = sheet_url.replace("/edit#gid=", "/export?format=csv&gid=")

@st.cache_data
def load_data(url):
    return pd.read_csv(url)

df = load_data(csv_url)

# === กำหนดชื่อคอลัมน์ให้ตรงกับ Google Sheet ===
col_name = {
    "name": "name",
    "location": "location",
    "budget": "budget",
    "tto": "time_to_open",
    "type1": "type1",
    "type2": "type2"
}

# === UI รับข้อมูลจากผู้ใช้ ===
st.header("🍽️ ระบบแนะนำร้านอาหาร (เฉพาะร้านที่ตรงเงื่อนไข)")

# สร้างตัวเลือกประเภทอาหารจาก type1 และ type2
all_types = pd.unique(pd.concat([df[col_name["type1"]], df[col_name["type2"]]]).dropna())

user_location = st.selectbox("📍 เลือกบริเวณ", df[col_name["location"]].dropna().unique())
user_type = st.selectbox("🍱 เลือกประเภทอาหาร", all_types)
user_budget = st.selectbox("💸 เลือกงบประมาณ", df[col_name["budget"]].dropna().unique())
user_time = st.selectbox("⏰ เลือกเวลา", df[col_name["tto"]].dropna().unique())

# === กรองข้อมูลจากเงื่อนไขผู้ใช้ ===
filtered_df = df[
    (df[col_name["location"]] == user_location) &
    (df[col_name["budget"]] == user_budget) &
    (df[col_name["tto"]] == user_time) &
    (
        (df[col_name["type1"]] == user_type) |
        (df[col_name["type2"]] == user_type)
    )
]

# === แสดงผลลัพธ์ ===
if not filtered_df.empty:
    st.subheader("✅ ร้านอาหารที่ตรงกับความต้องการ:")
    for _, row in filtered_df.iterrows():
        st.markdown(f"- **{row[col_name['name']]}** ({row[col_name['type1']]} / {row[col_name['type2']]})")
else:
    st.warning("😥 ไม่พบร้านอาหารที่ตรงกับความต้องการของคุณ")

# ปุ่มเริ่มใหม่
if st.button("🔁 เริ่มใหม่อีกครั้ง"):
    st.experimental_rerun()
