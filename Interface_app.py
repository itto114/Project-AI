import streamlit as st
import pandas as pd

# === ดึงข้อมูลจาก Google Sheet ===
sheet_id = "1ENpJYa3tnNrv6BBZJFG9pDNUTDqkbP7RQyBnA6pKSLI"
sheet_name = "Sheet1"
csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

try:
    df = pd.read_csv(csv_url)

    st.title("🍽️ ระบบแนะนำร้านอาหารใกล้ มทส.")

    st.subheader("📊 ข้อมูลร้านอาหารทั้งหมด:")
    st.dataframe(df)

    st.success("โหลดข้อมูลจาก Google Sheet สำเร็จแล้ว!")

    # === ฟอร์มให้ผู้ใช้เลือก ===
    user_location = st.selectbox("📍 บริเวณที่ต้องการจะไป", df['location'].unique())
    user_choice = st.selectbox("🍱 เลือกประเภทอาหาร", df['food_type'].unique())
    user_budget = st.radio("💸 งบประมาณต่อมื้อ (บาท)", ["ไม่เกิน 50", "50 - 100", "100 - 200", "200+"])
    user_time = st.selectbox("⏰ เวลาที่มักออกไปกิน", ["เช้า", "กลางวัน", "เย็น"])

    st.write(f"คุณเลือก: {user_location}, {user_choice}, {user_budget}, {user_time}")

except Exception as e:
    st.error("เกิดข้อผิดพลาดในการโหลดข้อมูลจาก Google Sheet")
    st.exception(e)

#Start KNN
from sklearn.neighbors import KNeighborsClassifier

# === แปลงข้อมูลที่ผู้ใช้เลือกเป็นตัวเลข ===
location_map = {"ประตู 1": 0, "ประตู 2": 1, "ประตู 3": 2, "ประตู 4": 3}
choice_map = {"อาหารตามสั่ง": 0, "อาหารอีสาน": 1, "อาหารจานเดียว": 2, "ปิ้งย่าง": 3, "อาหารเกาหลี": 4, "อาหารญี่ปุ่น": 5}
budget_map = {"50 - 100": 0, "100 - 200": 1, "200+": 2, "ไม่เกิน 50": 3}
time_map = {"กลางวัน": 0, "เช้า": 1, "เย็น": 2}

# แปลงข้อมูลของผู้ใช้
user_data = [[location_map[user_location], choice_map[user_choice], budget_map[user_budget], time_map[user_time]]]

# === คำนวณและทำนายร้านอาหาร ===
# สร้างโมเดล KNN จากข้อมูลที่มี
# (กรณีนี้เราต้องฝึกโมเดล KNN และบันทึกไฟล์โมเดลไว้ล่วงหน้า)
# ตัวอย่างการฝึกโมเดลและบันทึกโมเดล (ใช้ในกรณีที่คุณต้องการฝึกโมเดล)

X = df[['location', 'food_type', 'budget', 'time']]  # ข้อมูลฝึก
y = df['restaurant_name']  # ชื่อร้านอาหาร
knn_model = KNeighborsClassifier(n_neighbors=5)  # สร้างโมเดล KNN
knn_model.fit(X, y)

# ทำนายผลร้านที่แนะนำ
predicted_restaurant = knn_model.predict(user_data)

# แสดงผล
st.write(f"ร้านที่แนะนำ: {predicted_restaurant[0]}")

# ทำนายร้านอาหารที่ใกล้เคียง
k_neighbors = knn_model.kneighbors(user_data, n_neighbors=5)  # คำนวณ 5 ร้านที่ใกล้เคียง

st.write("ร้านที่ใกล้เคียง:")
for i, index in enumerate(k_neighbors[1][0]):
    st.write(f"{i+1}. {df['restaurant_name'][index]}")  # แสดงชื่อร้านที่ใกล้เคียง

if st.button("ไม่มีร้านไหนตรงใจ"):
    st.write("ขออภัย, ไม่มีร้านที่ตรงกับความต้องการของคุณ")
