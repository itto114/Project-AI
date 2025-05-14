import streamlit as st
import pandas as pd

# --- โหลดข้อมูลจาก Google Sheet ---
sheet_url = "https://docs.google.com/spreadsheets/d/1ENpJYa3tnNrv6BBZJFG9pDNUTDqkbP7RQyBnA6pKSLI/edit?gid=0#gid=0"
csv_url = sheet_url.replace("/edit?gid=0#gid=0", "/export?format=csv")

@st.cache_data
def load_data(url):
    return pd.read_csv(url)

df = load_data(csv_url)

# --- เริ่มต้นค่า session_state ถ้ายังไม่ถูกตั้งค่า ---
if 'step' not in st.session_state:
    st.session_state.step = 1  # เริ่มจากขั้นตอนที่ 1

# === ส่วนที่ 1: เลือกปัจจัย ===
if st.session_state.step == 1:
    st.header("🍽️ **ระบบแนะนำร้านอาหาร**")

    all_types = pd.unique(pd.concat([df["type_1"], df["type_2"]]).dropna())

    user_location = st.selectbox("📍 **บริเวณที่ต้องการ**", df["location"].dropna().unique())
    user_type = st.selectbox("🍱 **ประเภทอาหาร**", all_types)
    user_budget = st.selectbox("💸 **งบประมาณ**", df["budget"].dropna().unique())
    user_time = st.selectbox("⏰ **เวลาที่ต้องการจะไป (ร้านเปิด)**", df["time_to_open"].dropna().unique())

    if st.button("🔍 **ยืนยัน**"):
        # === กรองข้อมูลตามปัจจัยที่เลือก ===
        filtered_df = df[
            (df["type_1"] == user_type) | 
            (df["type_2"] == user_type)
        ]

        filtered_df = filtered_df[
            (filtered_df["location"] == user_location) &
            (filtered_df["budget"] == user_budget) &
            (filtered_df["time_to_open"] == user_time)
        ]

        # เปลี่ยนไปขั้นตอนที่ 2
        st.session_state.filtered_df = filtered_df
        st.session_state.step = 2

# === ส่วนที่ 2: เลือกร้านอาหาร ===
elif st.session_state.step == 2:
    st.subheader("🍴 **ร้านอาหารที่ตรงกับเงื่อนไขของคุณ**:")

    filtered_df = st.session_state.filtered_df

    if not filtered_df.empty:
        selected_restaurants = []  # เก็บร้านที่เลือก

        # แสดงร้านทั้งหมดที่กรองไว้ในขั้นตอนที่ 1
        for index, row in filtered_df.iterrows():
            st.markdown(f"### 🏆 **{row['name']}**")

            # แสดงข้อมูลของร้านในบรรทัดเดียวกัน
            st.write(f"**ประเภทอาหาร**: {row['type_1']} / {row['type_2']} | **บริเวณ**: {row['location']} | **งบประมาณ**: {row['budget']} | **เวลาเปิดร้าน**: {row['time_to_open']}")

            # ปุ่มเลือกสำหรับแต่ละร้าน
            selected = st.checkbox(f"✅ **เลือก {row['name']}**", key=row['name'])
            if selected:
                selected_restaurants.append(row['name'])

        # ปุ่ม "ยืนยัน" ทางซ้าย
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("✅ **ยืนยัน**"):
                if selected_restaurants:
                    st.session_state.selected_restaurants = selected_restaurants
                    st.session_state.step = 3  # ไปยังขั้นตอนที่ 3
                else:
                    st.warning("🚫 **กรุณาเลือกอย่างน้อย 1 ร้าน**")

        # ปุ่ม "ไม่ตรงใจ" ทางขวา
        with col2:
            if st.button("❌ **ไม่มีร้านไหนถูกใจ**"):
                st.session_state.step = 3  # ไปยังขั้นตอนที่ 3 (ไม่เลือกร้าน)

    else:
        st.warning("🚫 **ไม่พบร้านอาหารที่ตรงกับความต้องการของคุณ**")
        if st.button("🔙 **กลับไปเลือกใหม่**"):
            st.session_state.step = 1  # กลับไปยังขั้นตอนที่ 1

# === ส่วนที่ 3: ขอบคุณและเริ่มใหม่ ===
elif st.session_state.step == 3:
    st.subheader("🎉 **ขอบคุณที่ใช้ระบบแนะนำร้านอาหาร!**")

    if 'selected_restaurants' in st.session_state and st.session_state.selected_restaurants:
        st.write("คุณเลือก: 🏆")
        for restaurant in st.session_state.selected_restaurants:
            st.write(f"**{restaurant}**")
    else:
        st.write("😕 **ขออภัย ไม่มีร้านไหนถูกใจคุณ**")

    st.write("🙏 **ขอบคุณที่เลือกใช้งาน เราหวังว่าคุณจะพบร้านที่ถูกใจ!**")
    
    if st.button("🔄 **เริ่มใหม่**"):
        # รีเซ็ตสถานะและกลับไปยังขั้นตอนที่ 1
        st.session_state.step = 1
        del st.session_state.filtered_df  # ลบข้อมูลที่กรองไว้ก่อนหน้านี้
        if 'selected_restaurants' in st.session_state:
            del st.session_state.selected_restaurants  # ลบร้านที่เลือกไว้
