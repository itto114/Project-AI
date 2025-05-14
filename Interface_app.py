import streamlit as st
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import LabelEncoder


# --- โหลดข้อมูลจาก Google Sheet ---
sheet_url = "https://docs.google.com/spreadsheets/d/1ENpJYa3tnNrv6BBZJFG9pDNUTDqkbP7RQyBnA6pKSLI/edit#gid=0"
csv_url = sheet_url.replace("/edit#gid=", "/export?format=csv&gid=")

@st.cache_data
def load_data(url):
    return pd.read_csv(url)

df = load_data(csv_url)

# === ตั้งชื่อคอลัมน์ตามที่ผู้ใช้ระบุ ===
col_name = {
    "name": "ชื่อร้าน",
    "location": "บริเวณ",
    "budget": "งบประมาณ",
    "tto": "เวลา",
    "type1": "ประเภทอาหาร 1",
    "type2": "ประเภทอาหาร 2"
}

# === UI เลือกข้อมูลจากผู้ใช้ ===
st.header("🍽️ ระบบแนะนำร้านอาหารโดยใช้ KNN")

# สร้างตัวเลือกประเภทอาหารจากทั้งสองคอลัมน์
st.write("🧪 คอลัมน์ทั้งหมดในไฟล์:", df.columns.tolist())
all_types = pd.unique(pd.concat([df[col_name["type1"]], df[col_name["type2"]]]).dropna())

user_location = st.selectbox("📍 บริเวณที่ต้องการ", df[col_name["location"]].dropna().unique())
user_type = st.selectbox("🍱 ประเภทอาหาร", all_types)
user_budget = st.selectbox("💸 งบประมาณ", df[col_name["budget"]].dropna().unique())
user_time = st.selectbox("⏰ เวลา", df[col_name["tto"]].dropna().unique())

# === กรองจากประเภทอาหารที่ตรงกับ type1 หรือ type2 ===
filtered_df = df[
    (df[col_name["type1"]] == user_type) | 
    (df[col_name["type2"]] == user_type)
]

# === กรองจาก location, budget, tto ตามที่เลือก ===
filtered_df = filtered_df[
    (filtered_df[col_name["location"]] == user_location) &
    (filtered_df[col_name["budget"]] == user_budget) &
    (filtered_df[col_name["tto"]] == user_time)
]

# === หากมีข้อมูล ให้ทำ KNN ===
if not filtered_df.empty:
    # เตรียมข้อมูลสำหรับ KNN
    features = filtered_df[[col_name["location"], col_name["budget"], col_name["tto"], col_name["type1"], col_name["type2"]]].copy()

    # แปลงข้อมูลเป็นตัวเลขด้วย LabelEncoder
    encoders = {}
    for col in features.columns:
        enc = LabelEncoder()
        features[col] = enc.fit_transform(features[col])
        encoders[col] = enc

    # แปลงข้อมูลของผู้ใช้เป็นเวกเตอร์เดียวกัน
    user_input = pd.DataFrame([{
        col_name["location"]: user_location,
        col_name["budget"]: user_budget,
        col_name["tto"]: user_time,
        col_name["type1"]: user_type,
        col_name["type2"]: user_type  # สมมติว่า type1 กับ type2 เท่ากัน
    }])

    for col in user_input.columns:
        user_input[col] = encoders[col].transform(user_input[col])

    # ฝึก KNN และทำนาย
    knn = NearestNeighbors(n_neighbors=min(5, len(features)), metric='euclidean')
    knn.fit(features)

    distances, indices = knn.kneighbors(user_input)

    # แสดงผล
    st.subheader("✅ ร้านอาหารที่แนะนำ:")
    for idx in indices[0]:
        row = filtered_df.iloc[idx]
        st.markdown(f"- **{row[col_name['name']]}** ({row[col_name['type1']]} / {row[col_name['type2']]})")

else:
    st.warning("😥 ไม่พบร้านอาหารที่ตรงกับความต้องการของคุณ")
    st.button("ไม่มีร้านไหนตรงใจ")

if st.button("🔁 เริ่มใหม่อีกครั้ง"):
    st.experimental_rerun()
