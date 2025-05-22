import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 🎯 إعداد الصفحة
st.set_page_config(page_title="لوحة تحكم Snake Game", layout="wide")

# 📥 تحميل البيانات
url = "https://raw.githubusercontent.com/s1s00/Snake_Game_Sama/main/player_data.json"
st.title("📊 لوحة تحكم تحليلات Snake Game")

@st.cache_data
def load_data(url):
    df = pd.read_json(url)
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors='coerce')
    df = df.dropna(subset=["timestamp"])
    return df

try:
    df = load_data(url)
    st.success("✅ تم تحميل البيانات بنجاح.")
except Exception as e:
    st.error(f"❌ فشل في تحميل البيانات: {e}")
    st.stop()

# 🧠 اختيار لاعب معين (إن وجد)
if "player_id" in df.columns:
    player_ids = df["player_id"].dropna().unique()
    selected_player = st.selectbox("🎮 اختر اللاعب", options=["جميع اللاعبين"] + list(player_ids))
    if selected_player != "جميع اللاعبين":
        df = df[df["player_id"] == selected_player]

# ✅ 1. أوقات اللعب
st.header("⏰ تحليل أوقات اللعب")
if "timestamp" in df.columns:
    df["hour"] = df["timestamp"].dt.hour
    hourly_counts = df["hour"].value_counts().sort_index()
    st.bar_chart(hourly_counts)
else:
    st.warning("⚠️ لا يمكن عرض أوقات اللعب بدون عمود 'timestamp'.")

# ✅ 2. حركة الثعبان
st.header("🧭 مسار حركة الثعبان")
if {"x", "y"}.issubset(df.columns):
    fig1, ax1 = plt.subplots()
    ax1.plot(df["x"], df["y"], marker='o', linestyle='-', alpha=0.6)
    ax1.set_xlabel("X")
    ax1.set_ylabel("Y")
    ax1.set_title("مسار حركة الثعبان")
    st.pyplot(fig1)
else:
    st.warning("⚠️ لا يمكن عرض المسار بدون أعمدة 'x' و'y'.")

# ✅ 3. توزيع النتائج أو النقاط
st.header("✅❌ نتائج أو درجات اللاعبين")
if "finalScore" in df.columns:
    st.subheader("📈 توزيع النقاط")
    st.bar_chart(df["finalScore"].value_counts().sort_index())
elif "result" in df.columns:
    st.subheader("📊 توزيع النتائج")
    st.bar_chart(df["result"].value_counts())
else:
    st.warning("⚠️ لا يوجد عمود 'finalScore' أو 'result' في البيانات.")

# ✅ 4. الخريطة الحرارية
st.header("🔥 الخريطة الحرارية لتحركات الثعبان")
if {"x", "y"}.issubset(df.columns):
    heatmap_data = df.groupby(["y", "x"]).size().unstack(fill_value=0)
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    sns.heatmap(heatmap_data, cmap="YlOrRd", ax=ax2, linewidths=0.5, linecolor='white')
    ax2.invert_yaxis()
    ax2.set_title("الخريطة الحرارية لتحركات الثعبان")
    st.pyplot(fig2)
else:
    st.warning("⚠️ لا يمكن رسم الخريطة الحرارية بدون 'x' و'y'.")
