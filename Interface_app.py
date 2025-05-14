import streamlit as st
import pandas as pd
import random
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ฟังก์ชันที่ใช้เชื่อมต่อกับ Google Sheets
def send_log_to_sheet(action, user_location, user_type, user_budget, user_time, result):
    try:
        # เชื่อมต่อกับ Google Sheets
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(
            {
                "type": "service_account",
                "project_id": "project-ai-459806",
                "private_key_id": "c9267de79b8d3d6a8a560627af5639e414a9443f",
                "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDJTTTOJcRENLTM\n+c0tVlSXOkn8KYYJilOQ0AhRIWrWcyYbzUUGZF4nL7ZlIEwOOHc6x9GfBZcJdBow\n6nxx1yaWFEmAaet6XjYLOlkj1sAvTNY6TsN76Hp/mDtxY0KlQfOBlTKBbZBI0CUl\neaO9+HPdyYGB2Qvx4kpCN1p+6LN0JEowL7WhdDTe5m1YjpbqTgnkI4BWLB+hBq8P\nxGROoHIjLqU/o3zG1OvzkDcuBiYsOV7G4nbp99bB8F+ppLU4InLt7FE6CBs/sGsb\nAk4K+UW6+MLEpd4vDUN2n62IcGko9LtA2m42h+gnJO9c5qmkXx44VxC0DAOslJUr\nJKCdYEBzAgMBAAECggEAG6/o0WnUYuU08PRyygeTvvEfd/VmIC3MbKCQZEhKX5Ca\n7zv+gHCRmqYvWh1lGJefnpAZPtwP+Bbl+1BlKWtEPWQw796hqsUGfejaldlVuavB\n02c97+772kzf8CqM4hn+GhahSbf+HmWylkLyyJBBr4GltGxb/jr3p7/hTI9JD3In\n5YiVglRBhgIrg3cnq6VSFcoO0rzLqAZT3/azsW6PXRoj4Xs+FYnxFTJowSAvjmC0\nWSL2TBJSwE4B6nCaaeI6w1BZIAPLVGJ9RkSbTNwpbvviOqHRab44+W6SoSwRIsfd\nCcFMmNBO91wLCw4PcTbkm5eqcD/E+U2cBzlRoIp8oQKBgQDmvrl6jKFwdXFttJC1\nlZ+EycZ9nNQ4ORIiih2OHR0u954on5Vc/S0HocrKwrJMuo7IYK/63vMe+kpmJ2dv\n4taK/yURkPkGtfLT1DwlgkbSp88uBO0gkNeEqsTAH5n4QXKSawKULNhGzYXLUjs5\nW2Vz1MJRMJozuh4zn7h9kRHHGQKBgQDfVYCYfgZKHOYLlD0uN0mmW0hC1EcUbPRE\njCrZ0yjtTCAM91NgWQUG73bBk5KJrhg/q1fRjic6r/DjZpAP0DHQ8QTO2B7VJMEf\nSs9t2IRgPcg/Tmc7C8ncV6d238IZAoRhP8Q+2wbwXnpSlkEJfydIDbDdDVmxsuLV\nDaC1xJBxawKBgQDElft58DReloBj4fFj8yyruiiUvjeECwNrT9ZsTFuftzEVFRjw\n13Y0yV/3rTaw7kRVbSKhDq99Vepq6+lRRqZYV5YiSCwRzpQqaugvYLWsJXH6mBHa\nq+whyEfGE2ZfPos5OVhCG47Li7AQkGeKr1ZZAAvplgnaRhgTDWHmAOFviQKBgQDK\n8SZe674JYMNGaFlEAueBLNe4Kq/AhtVc6MYTlEdPgupo/eIc3iesSrPuaYwyYioU\nyT2O5g8NzE0oRs3IINbz1+AXmdpCsxhuuAtP9P0te1bY+ATkaezvthMt+VymX1wu\nBsTsnRlsGV4sZ+8Hkyz907sQ1A3aZQSst6p/IfRjqwKBgEEv1dKIDujQLQqQUnEH\nPuEGfnEgp43Rb4U4llRz72ilGA48BU/Oef0eANUlAGCa8ncMGRcDTuUT/KAoJyWd\n1Xy+ACjXGjSIfvI9pbZFByRbhO+ROEhVCEoEn0u7guY9lFXTm8+hJaf7NYU9FyBc\n+cPMAcOOElIuTJ8hoAnLqBRU\n-----END PRIVATE KEY-----\n",
                "client_email": "project-ai-access@project-ai-459806.iam.gserviceaccount.com",
                "client_id": "101094804846571311433",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/project-ai-access%40project-ai-459806.iam.gserviceaccount.com",
                "universe_domain": "googleapis.com"
            }, scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1Zh-XCctlshCQMczWf9Ztrv1CPtw1lkOb_7rt5qqssi0/edit?gid=0#gid=0").sheet1
        sheet.append_row([action, user_location, user_type, user_budget, user_time, result])
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการส่งข้อมูลไปยัง Google Sheet: {e}")

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

# --- ฟังก์ชันเชื่อมต่อ Google Sheets ---
def send_log_to_sheet(action, user_location, user_type, user_budget, user_time, result):
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("config/credentials.json", scope)
        client = gspread.authorize(creds)
        sheet = client.open("MealMatch").sheet1
        sheet.append_row([action, user_location, user_type, user_budget, user_time, result])
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการส่งข้อมูลไปยัง Google Sheet: {e}")

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
    user_budget = st.selectbox("💰 งบประมาณ", BUDGETS)
    user_time = st.selectbox("⏰ เวลาเปิด", TIMES)

    if st.button("แนะนำร้าน"):
        # ค้นหาจากข้อมูลที่ตรงกับตัวเลือก
        filtered_df = df[
            (df['location'] == user_location) &
            (df['type_1'] == user_type) &
            (df['budget'] == user_budget) &
            (df['time_to_open'] == user_time)
        ]
        recommended_restaurants = filtered_df.sample(n=3)
        st.write("ร้านที่แนะนำ:")
        for index, row in recommended_restaurants.iterrows():
            st.write(f"✔️ {row['name']} - {row['url']}")

        send_log_to_sheet("แนะนำร้าน", user_location, user_type, user_budget, user_time, ", ".join(recommended_restaurants['name']))
        st.session_state.step = 2

# === ส่วนที่ 2: เลือกร้านจากข้อมูลที่แนะนำ ---
if st.session_state.step == 2:
    st.header("🏆 เลือกร้านที่สนใจ")
    for index, row in recommended_restaurants.iterrows():
        if st.checkbox(row['name']):
            st.write(f"✔️ {row['name']} - {row['url']}")
