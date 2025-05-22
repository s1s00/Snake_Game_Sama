import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ----------------------
# 🟡 تحميل البيانات من GitHub
url = "https://raw.githubusercontent.com/s1s00/Snake_Game_Sama/main/player_data.json"

try:
    df = pd.read_json(url)
    st.success("✅ تم تحميل البيانات بنجاح.")
except Exception as e:
    st.error(f"❌ فشل في تحميل البيانات: {e}")
    st.stop()

st.title("📊 لوحة تحكم تحليلات Snake Game")

# ----------------------
# 🔵 تحويل الطابع الزمني إلى datetime
if "timestamp" in df.columns:
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors='coerce')
    df.dropna(subset=["timestamp"], inplace=True)
else:
    st.warning("⚠️ العمود 'timestamp' غير موجود في البيانات.")

# ----------------------
# ⏰ تحليل أوقات اللعب
st.header("⏰ أوقات اللعب")
if "timestamp" in df.columns:
    df["hour"] = df["timestamp"].dt.hour
    st.line_chart(df["hour"].value_counts().sort_index())
else:
    st.write("لا يمكن عرض أوقات اللعب بدون عمود timestamp.")

# ----------------------
# 🧭 تحليل حركة اللاعبين
st.header("🧭 حركة اللاعبين")
if {"x", "y"}.issubset(df.columns):
    fig, ax = plt.subplots()
    ax.scatter(df["x"], df["y"], alpha=0.6)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    st.pyplot(fig)
else:
    st.write("لا يمكن عرض حركة اللاعبين بدون أعمدة x و y.")
