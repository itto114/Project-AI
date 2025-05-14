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
all_types = pd.unique(pd.concat([df["ประเภทอาหาร 1"], df["ประเภทอาหาร 2"]]).dropna())

# ให้ผู้ใช้เลือกข้อมูลที่ต้องการ
user_location = st.selectbox("📍 บริเวณที่ต้องการ", df["บริเวณ"].dropna().unique())
user_type = st.selectbox("🍱 ประเภทอาหาร", all_types)
user_budget = st.selectbox("💸 งบประมาณ", df["งบประมาณ"].dropna().unique())
user_time = st.selectbox("⏰ เวลา", df["เวลา"].dropna().unique())

# === กรองจากประเภทอาหารที่ตรงกับ type1 หรือ type2 ===
filtered_df = df[
    (df["ประเภทอาหาร 1"] == user_type) | 
    (df["ประเภทอาหาร 2"] == user_type)
]

# === กรองจาก location, budget, tto ตามที่เลือก ===
filtered_df = filtered_df[
    (filtered_df["บริเวณ"] == user_location) &
    (filtered_df["งบประมาณ"] == user_budget) &
    (filtered_df["เวลา"] == user_time)
]

# === แสดงผลลัพธ์ ===
if not filtered_df.empty:
    st.subheader("ร้านอาหารที่ตรงกับเงื่อนไขของคุณ:")
    for index, row in filtered_df.iterrows():
        st.markdown(f"- **{row['ชื่อร้าน']}** ({row['ประเภทอาหาร 1']} / {row['ประเภทอาหาร 2']})")
else:
    st.warning("ไม่พบร้านอาหารที่ตรงกับความต้องการของคุณ")
    
if st.button("🔁 เริ่มใหม่"):
    st.experimental_rerun()
