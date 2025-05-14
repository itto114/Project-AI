import streamlit as st
import pandas as pd

# --- โหลดข้อมูลจาก Google Sheet ---
sheet_url = "https://docs.google.com/spreadsheets/d/1ENpJYa3tnNrv6BBZJFG9pDNUTDqkbP7RQyBnA6pKSLI/edit#gid=0"
csv_url = sheet_url.replace("/edit#gid=", "/export?format=csv&gid=")

@st.cache_data
def load_data(url):
    return pd.read_csv(url)

df = load_data(csv_url)

# ตรวจสอบชื่อคอลัมน์ทั้งหมดใน DataFrame
st.write("ชื่อคอลัมน์ใน DataFrame:", df.columns.tolist())

# === UI รับข้อมูลจากผู้ใช้ ===
st.header("🍽️ ระบบแนะนำร้านอาหาร (เฉพาะร้านที่ตรงเงื่อนไข)")

# สร้างตัวเลือกประเภทอาหารจาก type1 และ type2
all_types = pd.unique(pd.concat([df["type_1"], df["type_2"]]).dropna())

user_location = st.selectbox("📍 เลือกบริเวณ", df["location"].dropna().unique())
user_type = st.selectbox("🍱 เลือกประเภทอาหาร", all_types)
user_budget = st.selectbox("💸 เลือกงบประมาณ", df["budget"].dropna().unique())
user_time = st.selectbox("⏰ เลือกเวลา", df["time_to_open"].dropna().unique())

# === กรองข้อมูลจากเงื่อนไขผู้ใช้ ===
filtered_df = df[
    (df["location"] == user_location) &
    (df["budget"] == user_budget) &
    (df["time_to_open"] == user_time) &
    (
        (df["type_1"] == user_type) |
        (df["type_2"] == user_type)
    )
]

# === แสดงผลลัพธ์ ===
if not filtered_df.empty:
    st.subheader("✅ ร้านอาหารที่ตรงกับความต้องการ:")
    for _, row in filtered_df.iterrows():
        st.markdown(f"- **{row['name']}** ({row['type_1']} / {row['type_2']})")
else:
    st.warning("😥 ไม่พบร้านอาหารที่ตรงกับความต้องการของคุณ")

# ปุ่มเริ่มใหม่
if st.button("🔁 เริ่มใหม่อีกครั้ง"):
    st.experimental_rerun()
