import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# تحميل البيانات
url = "https://raw.githubusercontent.com/s1s00/Snake_Game_Sama/main/player_data.json"
try:
    df = pd.read_json(url)
    st.success("✅ تم تحميل البيانات بنجاح.")
except Exception as e:
    st.error(f"❌ فشل في تحميل البيانات: {e}")
    st.stop()

st.title("📊 لوحة تحكم تحليلات Snake Game")

# حركة اللاعبين
st.header("🧭 حركة اللاعبين")
if {"player_id", "x", "y"}.issubset(df.columns):
    fig1, ax1 = plt.subplots()
    for pid, group in df.groupby("player_id"):
        ax1.plot(group["x"], group["y"], marker='o', label=f"لاعب {pid}")
    ax1.set_xlabel("X")
    ax1.set_ylabel("Y")
    ax1.legend()
    st.pyplot(fig1)
else:
    st.warning("⚠️ البيانات لا تحتوي على الأعمدة المطلوبة: 'player_id', 'x', 'y'.")

# توزيع النجاح والفشل
st.header("✅❌ توزيع النتائج")
if "result" in df.columns:
    st.bar_chart(df["result"].value_counts())
else:
    st.warning("⚠️ عمود 'result' غير موجود في البيانات.")

# أوقات اللعب
st.header("⏰ أوقات اللعب")
if "timestamp" in df.columns:
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors='coerce')
    df.dropna(subset=["timestamp"], inplace=True)
    df["hour"] = df["timestamp"].dt.hour
    st.line_chart(df["hour"].value_counts().sort_index())
else:
    st.warning("⚠️ العمود 'timestamp' غير موجود في البيانات.")

# الخريطة الحرارية
st.header("🔥 الخريطة الحرارية")
if {"x", "y"}.issubset(df.columns):
    heatmap_data = df.groupby(["y", "x"]).size().unstack(fill_value=0)
    fig2, ax2 = plt.subplots()
    sns.heatmap(heatmap_data, cmap="YlOrRd", ax=ax2, linewidths=0.5, linecolor='white')
    ax2.invert_yaxis()
    st.pyplot(fig2)
else:
    st.warning("⚠️ لا يمكن إنشاء الخريطة الحرارية بدون أعمدة x و y.")
