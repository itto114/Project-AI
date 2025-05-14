import streamlit as st
import pandas as pd

# ---------- 1. สร้างฐานข้อมูลตัวเลือก ----------
locations = ["ประตู1", "ประตู2", "ประตู3", "ประตู4"]
budgets = ["น้อยกว่า50", "50 - 100", "100 - 200", "200+"]
types = ["อาหารตามสั่ง", "อาหารอีสาน", "อาหารจานเดียว", "ปิ้งย่าง", "อาหารเกาหลี", "อาหารญี่ปุ่น"]
times = ["เช้า (ก่อน 10 โมงเช้า)", "กลางวัน (10โมงเช้า - 4โมงเย็น)", "เย็น (ตั้งแต่ 4 โมงเย็น)"]

# ---------- 2. สร้างข้อมูลร้านตัวอย่าง ----------
restaurant_data = [
    {"name": "ร้าน A", "location": "ประตู1", "budget": "50 - 100", "type_1": "อาหารอีสาน", "time_to_open": "กลางวัน (10โมงเช้า - 4โมงเย็น)"},
    {"name": "ร้าน B", "location": "ประตู1", "budget": "50 - 100", "type_1": "อาหารอีสาน", "time_to_open": "กลางวัน (10โมงเช้า - 4โมงเย็น)"},
    {"name": "ร้าน C", "location": "ประตู2", "budget": "100 - 200", "type_1": "ปิ้งย่าง", "time_to_open": "เย็น (ตั้งแต่ 4 โมงเย็น)"},
    {"name": "ร้าน D", "location": "ประตู3", "budget": "200+", "type_1": "อาหารเกาหลี", "time_to_open": "เย็น (ตั้งแต่ 4 โมงเย็น)"},
    {"name": "ร้าน E", "location": "ประตู4", "budget": "น้อยกว่า50", "type_1": "อาหารจานเดียว", "time_to_open": "เช้า (ก่อน 10 โมงเช้า)"},
]

df = pd.DataFrame(restaurant_data)

# ---------- 3. ตั้งค่า Session State ----------
if "step" not in st.session_state:
    st.session_state.step = 1
if "selected_restaurant" not in st.session_state:
    st.session_state.selected_restaurant = None

# ---------- ส่วนที่ 1: เลือกปัจจัย ----------
if st.session_state.step == 1:
    st.header("🍽️ ระบบแนะนำร้านอาหาร")

    user_location = st.selectbox("📍 เลือกบริเวณ", locations)
    user_type = st.selectbox("🍱 เลือกประเภทอาหาร", types)
    user_budget = st.selectbox("💸 เลือกงบประมาณ", budgets)
    user_time = st.selectbox("⏰ เลือกเวลาที่ต้องการ", times)

    if st.button("🔍 ยืนยัน"):
        filtered = df[
            (df["location"] == user_location) &
            (df["type_1"] == user_type) &
            (df["budget"] == user_budget) &
            (df["time_to_open"] == user_time)
        ]
        st.session_state.filtered_df = filtered
        st.session_state.step = 2

# ---------- ส่วนที่ 2: เลือกร้านอาหาร ----------
elif st.session_state.step == 2:
    st.subheader("🍴 ร้านที่ตรงกับความต้องการของคุณ")

    filtered_df = st.session_state.filtered_df
    selected_radio = None

    if not filtered_df.empty:
        options = [row["name"] for index, row in filtered_df.iterrows()]
        selected_radio = st.radio("เลือกร้านที่คุณต้องการ:", options)

        for index, row in filtered_df.iterrows():
            if row["name"] == selected_radio:
                st.markdown(f"""
                    └ 📍 **บริเวณ:** {row['location']}  
                    └ 💸 **งบประมาณ:** {row['budget']}  
                    └ 🍱 **ประเภทอาหาร:** {row['type_1']}  
                    └ ⏰ **เวลาเปิด:** {row['time_to_open']}  
                """)
                st.markdown("---")

        # ปุ่มด้านล่าง
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ ยืนยันร้านที่เลือก"):
                st.session_state.selected_restaurant = selected_radio
                st.session_state.step = 3
        with col2:
            if st.button("❌ ไม่มีร้านไหนถูกใจ"):
                st.session_state.selected_restaurant = None
                st.session_state.step = 3
    else:
        st.warning("ไม่พบร้านที่ตรงกับเงื่อนไข 😥")
        if st.button("🔙 กลับไปเลือกใหม่"):
            st.session_state.step = 1

# ---------- ส่วนที่ 3: ขอบคุณ ----------
elif st.session_state.step == 3:
    st.header("🙏 ขอบคุณที่ใช้ระบบแนะนำร้านอาหาร")

    if st.session_state.selected_restaurant:
        st.write("🎉 คุณเลือกร้าน:")
        st.markdown(f"- 🏆 **{st.session_state.selected_restaurant}**")
    else:
        st.write("😕 ไม่มีร้านไหนถูกใจคุณ")

    if st.button("🔄 เริ่มใหม่"):
        st.session_state.step = 1
        st.session_state.selected_restaurant = None
        st.session_state.pop("filtered_df", None)
