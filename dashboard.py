import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# رابط البيانات
url = "https://raw.githubusercontent.com/s1s00/Snake_Game_Sama/main/player_data.json"

try:
    df = pd.read_json(url)
    st.success("✅ تم تحميل البيانات بنجاح.")
except Exception as e:
    st.error(f"❌ فشل في تحميل البيانات: {e}")
    st.stop()

# تحويل عمود position إلى أعمدة x و y
if 'position' in df.columns:
    df['x'] = df['position'].apply(lambda pos: pos.get('x') if isinstance(pos, dict) else None)
    df['y'] = df['position'].apply(lambda pos: pos.get('y') if isinstance(pos, dict) else None)

st.title("📊 لوحة تحكم تحليلات Snake Game")

# 1. حركة اللاعبين (كل الأحداث مع إحداثيات)
st.header("🧭 حركة الثعبان (إحداثيات الأحداث)")
if {"x", "y"}.issubset(df.columns):
    fig1, ax1 = plt.subplots()
    ax1.plot(df["x"], df["y"], marker='o', linestyle='-', alpha=0.7, color='blue')
    ax1.set_xlabel("X")
    ax1.set_ylabel("Y")
    ax1.set_title("حركة الثعبان عبر الإحداثيات")
    st.pyplot(fig1)
else:
    st.warning("⚠️ لا توجد إحداثيات x و y في البيانات.")

# 2. توزيع نتائج اللعبة (finalScore)
st.header("✅ توزيع نتائج اللعبة (finalScore)")
if "finalScore" in df.columns:
    st.bar_chart(df["finalScore"].value_counts())
else:
    st.warning("⚠️ عمود 'finalScore' غير موجود في البيانات.")

# 3. أوقات اللعب
st.header("⏰ أوقات اللعب")
if "timestamp" in df.columns:
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors='coerce')
    df.dropna(subset=["timestamp"], inplace=True)
    df["hour"] = df["timestamp"].dt.hour
    st.line_chart(df["hour"].value_counts().sort_index())
else:
    st.warning("⚠️ العمود 'timestamp' غير موجود في البيانات.")

# 4. الخريطة الحرارية
st.header("🔥 الخريطة الحرارية للإحداثيات")
if {"x", "y"}.issubset(df.columns):
    heatmap_data = df.groupby(["y", "x"]).size().unstack(fill_value=0)
    fig2, ax2 = plt.subplots()
    sns.heatmap(heatmap_data, cmap="YlOrRd", ax=ax2, linewidths=0.5, linecolor='white')
    ax2.invert_yaxis()
    st.pyplot(fig2)
else:
    st.warning("⚠️ لا يمكن إنشاء الخريطة الحرارية بدون أعمدة x و y.")
