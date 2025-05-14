import streamlit as st
import pandas as pd

# --- โหลดข้อมูลจาก Google Sheet ---
sheet_url = "https://docs.google.com/spreadsheets/d/1ENpJYa3tnNrv6BBZJFG9pDNUTDqkbP7RQyBnA6pKSLI/edit#gid=0"
csv_url = sheet_url.replace("/edit#gid=", "/export?format=csv&gid=")

@st.cache_data
def load_data(url):
    return pd.read_csv(url)

df = load_data(csv_url)

# === ตรวจสอบชื่อคอลัมน์ ===
st.write("🧾 คอลัมน์ที่พบ:", df.columns.tolist())

# === สร้างหน้าต่างให้ผู้ใช้เลือกข้อมูล ===
st.header("🍽️ ระบบแนะนำร้านอาหารใกล้มหาวิทยาลัยเทคโนโลยีสุรนารี")

# ดึงตัวเลือกประเภทอาหารจากทั้ง 2 คอลัมน์โดยรวมให้ไม่ซ้ำ
all_food_types = pd.unique(pd.concat([df["ประเภทอาหาร 1"], df["ประเภทอาหาร 2"]]).dropna())

user_location = st.selectbox("📍 บริเวณที่ต้องการจะไป", df["บริเวณ"].dropna().unique())
user_choice = st.selectbox("🍱 เลือกประเภทอาหาร", all_food_types)
user_budget = st.selectbox("💸 งบประมาณต่อมื้อ", df["งบประมาณ"].dropna().unique())
user_time = st.selectbox("⏰ เวลาที่มักออกไปกิน", df["เวลา"].dropna().unique())

# === กรองข้อมูลตามประเภทอาหารที่ตรงกับ user_choice ===
filtered_df = df[
    (df["ประเภทอาหาร 1"] == user_choice) | 
    (df["ประเภทอาหาร 2"] == user_choice)
]

# === กรองเพิ่มจากปัจจัยอื่น ๆ ===
filtered_df = filtered_df[
    (filtered_df["บริเวณ"] == user_location) &
    (filtered_df["งบประมาณ"] == user_budget) &
    (filtered_df["เวลา"] == user_time)
]

# === แสดงผลลัพธ์ ===
if not filtered_df.empty:
    st.subheader("✅ ร้านอาหารที่แนะนำ:")
    for idx, row in filtered_df.iterrows():
        st.markdown(f"- **{row['ชื่อร้าน']}** ({row['ประเภทอาหาร 1']} / {row['ประเภทอาหาร 2']})")
else:
    st.warning("😥 ไม่พบร้านอาหารที่ตรงกับความต้องการของคุณ")
    st.button("ไม่มีร้านไหนตรงใจ")

# ปุ่มเริ่มใหม่
if st.button("🔁 เริ่มใหม่อีกครั้ง"):
    st.experimental_rerun()
