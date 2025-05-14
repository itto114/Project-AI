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
        restaurant_names = filtered_df['name'].tolist()

        # ตรวจสอบว่า restaurant_names มีค่าหรือไม่
        if restaurant_names:
            selected = st.radio("✅ เลือกร้านที่ต้องการ", options=restaurant_names)

            for row in filtered_df.itertuples():
                st.markdown(f"### 🏪 {row.name}")
                st.markdown(f"📌 ประเภท: {row.type_1}\n\n📍 บริเวณ: {row.location}\n\n💸 งบประมาณ: {row.budget}\n\n⏰ เวลาเปิด: {row.time_to_open}")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ ยืนยันการเลือกร้านนี้"):
                    st.session_state.selected_restaurant = selected
                    st.session_state.history.append(selected)
                    st.session_state.step = 3
            with col2:
                if st.button("❌ ไม่มีร้านไหนถูกใจ"):
                    st.session_state.selected_restaurant = None
                    st.session_state.step = 3
        else:
            st.warning("🚫 ไม่มีร้านอาหารให้เลือกในตอนนี้")
    else:
        st.warning("🚫 ไม่พบร้านอาหารที่ตรงกับความต้องการของคุณ")
        if st.button("🔙 กลับไปเลือกใหม่"):
            st.session_state.step = 1


# === ส่วนที่ 3: ขอบคุณและแสดงผลลัพธ์ ===
elif st.session_state.step == 3:
    st.subheader("🙏 ขอบคุณที่ใช้ระบบแนะนำร้านอาหาร!")

    if st.session_state.get('selected_restaurant'):
        selected_name = st.session_state.selected_restaurant
        selected_row = df[df['name'] == selected_name].iloc[0]
        st.success(f"🎉 คุณเลือกร้าน: **{selected_name}**")
        st.markdown(f"📌 ประเภท: {selected_row['type_1']}")
        st.markdown(f"📍 บริเวณ: {selected_row['location']}")
        st.markdown(f"💸 งบประมาณ: {selected_row['budget']}")
        st.markdown(f"⏰ เวลาเปิด: {selected_row['time_to_open']}")
        st.markdown(f"🔗 [ดูรายละเอียดเพิ่มเติม]({selected_row['url']})")
    else:
        st.info("😕 ไม่มีร้านไหนตรงใจคุณในครั้งนี้")

    if st.session_state.history:
        st.markdown("---")
        st.subheader("🕘 ประวัติการเลือกร้านก่อนหน้า")
        for hist_name in st.session_state.history:
            row = df[df['name'] == hist_name].iloc[0]
            st.markdown(f"- **{hist_name}** — {row['type_1']}, {row['location']}, {row['budget']}, {row['time_to_open']}")

    if st.button("🔄 เริ่มใหม่"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
