
# Interface.app.py

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

except Exception as e:
    st.error("เกิดข้อผิดพลาดในการโหลดข้อมูลจาก Google Sheet")
    st.exception(e)

import streamlit as st


