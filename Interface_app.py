import streamlit as st
import pandas as pd
import random

# --- ตัวเลือกฐานข้อมูลหลักสำหรับการกรอก ---
LOCATIONS = ["ประตู1", "ประตู2", "ประตู3", "ประตู4"]
BUDGETS = ["น้อยกว่า50", "50 - 100", "100 - 200", "200+"]
TYPES = ["อาหารตามสั่ง", "อาหารอีสาน (เช่น ส้มตำ ลาบ ก้อย)", "อาหารจานเดียว", "ปิ้งย่าง", "อาหารเกาหลี", "อาหารญี่ปุ่น"]
TIMES = ["เช้า (ก่อน 10 โมงเช้า)", "กลางวัน (10โมงเช้า - 4โมงเย็น)", "เย็น (ตั้งแต่ 4 โมงเย็น)"]

# --- ข้อมูลร้านอาหาร (สุ่มตัวอย่าง) ---
data = [
    {"name": "ร้าน A", "location": "ประตู1", "budget": "50 - 100", "type_1": "อาหารตามสั่ง", "time_to_open": "กลางวัน (10โมงเช้า - 4โมงเย็น)", "url": "https://abc.com/a"},
    {"name": "ร้าน B", "location": "ประตู1", "budget": "50 - 100", "type_1": "อาหารตามสั่ง", "time_to_open": "กลางวัน (10โมงเช้า - 4โมงเย็น)", "url": "https://abc.com/b"},
    {"name": "ร้าน C", "location": "ประตู2", "budget": "100 - 200", "type_1": "ปิ้งย่าง", "time_to_open": "เย็น (ตั้งแต่ 4 โมงเย็น)", "url": "https://abc.com/c"},
    {"name": "ร้าน D", "location": "ประตู3", "budget": "200+", "type_1": "อาหารญี่ปุ่น", "time_to_open": "เย็น (ตั้งแต่ 4 โมงเย็น)", "url": "https://abc.com/d"},
    {"name": "ร้าน E", "location": "ประตู1", "budget": "50 - 100", "type_1": "อาหารตามสั่ง", "time_to_open": "กลางวัน (10โมงเช้า - 4โมงเย็น)", "url": "https://abc.com/e"}
]
df = pd.DataFrame(data)

# --- เริ่มต้นค่า session_state ถ้ายังไม่ถูกตั้งค่า ---
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'history' not in st.session_state:
    st.session_state.history = []

# === ส่วนที่ 1: เลือกปัจจัย ===
if st.session_state.step == 1:
    st.header("🍽️ ระบบแนะนำร้านอาหาร")

    user_location = st.selectbox("📍 บริเวณที่ต้องการ", LOCATIONS)
    user_type = st.selectbox("🍱 ประเภทอาหาร", TYPES)
    user_budget = st.selectbox("💸 งบประมาณ", BUDGETS)
    user_time = st.selectbox("⏰ เวลาที่ต้องการจะไป (ร้านเปิด)", TIMES)

    if st.button("🔍 ยืนยัน"):
        filtered_df = df[
            (df["type_1"] == user_type) &
            (df["location"] == user_location) &
            (df["budget"] == user_budget) &
            (df["time_to_open"] == user_time)
        ]
        st.session_state.filtered_df = filtered_df
        st.session_state.step = 2

    # แนะนำร้านยอดนิยมแบบสุ่ม
    st.markdown("---")
    st.subheader("🔥 ร้านแนะนำสำหรับคุณ")
    for rec in random.sample(data, 2):
        st.markdown(f"**{rec['name']}** — {rec['type_1']} | {rec['budget']} | {rec['location']} | {rec['time_to_open']}")

# === ส่วนที่ 2: เลือกร้านอาหาร ===
elif st.session_state.step == 2:
    st.subheader("🍴 ร้านอาหารที่ตรงกับเงื่อนไขของคุณ")

    filtered_df = st.session_state.filtered_df

    if not filtered_df.empty:
        selected_restaurants = []

        # แสดงรายการร้านอาหารพร้อม checkbox และรายละเอียดในบรรทัดเดียวกัน
        for index, row in filtered_df.iterrows():
            col1, col2 = st.columns([1, 5])
            with col1:
                selected = st.checkbox("", key=row['name'])
            with col2:
                st.markdown(f"### 🏪 {row['name']}")
                st.markdown(f"📌 ประเภท: {row['type_1']}")
                st.markdown(f"📍 บริเวณ: {row['location']}")
                st.markdown(f"💸 งบประมาณ: {row['budget']}")
                st.markdown(f"⏰ เวลาเปิด: {row['time_to_open']}")

                if selected:
                    selected_restaurants.append(row['name'])

        # ปุ่มยืนยันการเลือก
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("✅ ยืนยันการเลือกร้าน"):
                if selected_restaurants:
                    st.session_state.selected_restaurants = selected_restaurants
                    st.session_state.step = 3  # ไปยังขั้นตอนที่ 3
                else:
                    st.warning("🚫 กรุณาเลือกอย่างน้อย 1 ร้าน")
        with col2:
            if st.button("❌ ไม่มีร้านไหนถูกใจ"):
                st.session_state.selected_restaurants = []
                st.session_state.step = 3

    else:
        st.warning("🚫 ไม่พบร้านอาหารที่ตรงกับความต้องการของคุณ")
        if st.button("🔙 กลับไปเลือกใหม่"):
            st.session_state.step = 1

# === ส่วนที่ 3: ขอบคุณและแสดงผลลัพธ์ ===
elif st.session_state.step == 3:
    st.subheader("🙏 ขอบคุณที่ใช้ระบบแนะนำร้านอาหาร!")

    if 'selected_restaurants' in st.session_state and st.session_state.selected_restaurants:
        st.write("คุณเลือก: 🏆")
        for restaurant in st.session_state.selected_restaurants:
            row = df[df['name'] == restaurant].iloc[0]
            st.write(f"**{restaurant}**")
            st.write(f"📌 ประเภท: {row['type_1']}")
            st.write(f"📍 บริเวณ: {row['location']}")
            st.write(f"💸 งบประมาณ: {row['budget']}")
            st.write(f"⏰ เวลาเปิด: {row['time_to_open']}")
            st.write(f"🔗 [ดูรายละเอียดเพิ่มเติม]({row['url']})")
    else:
        st.write("😕 **ขออภัย ไม่มีร้านไหนถูกใจคุณ**")

    if st.button("🔄 เริ่มใหม่"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
