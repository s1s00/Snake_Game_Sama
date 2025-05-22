import json
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# تحميل البيانات من ملف JSON
with open("player_data.json", "r") as file:
    data = json.load(file)

# تحويل البيانات إلى DataFrame
df = pd.DataFrame(data)

# 🟡 حساب الميزات
direction_changes = df[df["type"] == "direction_change"].shape[0]
food_eaten = df[df["type"] == "food_eaten"].shape[0]

# زمن اللعب (لو موجود)
if "totalDuration" in df.columns:
    total_duration = df[df["type"] == "game_over"]["totalDuration"].iloc[0]
else:
    total_duration = None

# ✅ إنشاء DataFrame فيه ميزات اللاعب
features = pd.DataFrame([{
    "direction_changes": direction_changes,
    "food_eaten": food_eaten,
    "total_duration": total_duration
}])

print("بيانات الميزات:\n", features)

# ✅ تطبيق KMeans (عدد المجموعات = 2 كمثال)
kmeans = KMeans(n_clusters=2, random_state=0)
features_clean = features.dropna()  # حذف أي صف فيه None
kmeans.fit(features_clean)

# عرض نتائج التجميع
features_clean['cluster'] = kmeans.labels_
print("\nنتائج K-Means:\n", features_clean)

# ✅ رسم بياني
plt.figure(figsize=(6, 4))
plt.scatter(features_clean['direction_changes'], features_clean['food_eaten'],
            c=features_clean['cluster'], cmap='viridis', s=100)
plt.xlabel("تغييرات الاتجاه")
plt.ylabel("عدد الأطعمة")
plt.title("تجميع اللاعبين - K-Means")
plt.grid(True)
plt.show()
