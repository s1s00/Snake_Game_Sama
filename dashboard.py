import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# تحميل البيانات
url = "https://raw.githubusercontent.com/s1s00/Snake_Game_Sama/main/player_data.json"

st.title("📊 لوحة تحكم تحليلات Snake Game")

try:
    df = pd.read_json(url)
    st.success("✅ تم تحميل البيانات بنجاح.")
except Exception as e:
    st.error(f"❌ فشل في تحميل البيانات: {e}")
    st.stop()

# معالجة الطابع الزمني
if "timestamp" in df.columns:
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors='coerce')
    df.dropna(subset=["timestamp"], inplace=True)

# ✅ 1. أوقات اللعب
st.header("⏰ أوقات اللعب")
if "timestamp" in df.columns:
    df["hour"] = df["timestamp"].dt.hour
    st.line_chart(df["hour"].value_counts().sort_index())
else:
    st.warning("⚠️ لا يمكن عرض أوقات اللعب بدون عمود 'timestamp'.")

# ✅ 2. حركة الثعبان
st.header("🧭 حركة الثعبان")
if {"x", "y"}.issubset(df.columns):
    fig1, ax1 = plt.subplots()
    ax1.plot(df["x"], df["y"], marker='o', linestyle='-', alpha=0.6)
    ax1.set_xlabel("X")
    ax1.set_ylabel("Y")
    ax1.set_title("مسار حركة الثعبان")
    st.pyplot(fig1)
else:
    st.warning("⚠️ لا يمكن عرض الحركة بدون أعمدة 'x' و'y'.")

# ✅ 3. توزيع نتائج اللعبة
st.header("✅❌ توزيع نتائج اللعبة")
if "finalScore" in df.columns:
    st.bar_chart(df["finalScore"].value_counts().sort_index())
elif "result" in df.columns:
    st.bar_chart(df["result"].value_counts())
else:
    st.warning("⚠️ لا يوجد عمود 'finalScore' أو 'result' في البيانات.")

# ✅ 4. الخريطة الحرارية
st.header("🔥 الخريطة الحرارية للإحداثيات")
if {"x", "y"}.issubset(df.columns):
    heatmap_data = df.groupby(["y", "x"]).size().unstack(fill_value=0)
    fig2, ax2 = plt.subplots()
    sns.heatmap(heatmap_data, cmap="YlOrRd", ax=ax2, linewidths=0.5, linecolor='white')
    ax2.invert_yaxis()
    ax2.set_title("الخريطة الحرارية لتحركات الثعبان")
    st.pyplot(fig2)
else:
    st.warning("⚠️ لا يمكن إنشاء الخريطة الحرارية بدون أعمدة 'x' و'y'.")

# python analyze.py
# streamlit run dashboard.py
