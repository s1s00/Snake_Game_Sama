import json
from collections import Counter
from datetime import datetime

# قراءة الملف
with open("player_data.json", "r", encoding="utf-8") as f:
    logs = json.load(f)

# تنظيف وتحضير بيانات الحركة
moves = [log for log in logs if isinstance(log, dict) and log.get('x') is not None and log.get('y') is not None]

if not moves:
    print("❌ ما في بيانات حركة صالحة.")
    exit()

# حساب تغييرات الاتجاه
direction_changes = 0
last_dx, last_dy = None, None

for i in range(1, len(moves)):
    dx = moves[i]['x'] - moves[i-1]['x']
    dy = moves[i]['y'] - moves[i-1]['y']
    if (dx, dy) != (last_dx, last_dy):
        direction_changes += 1
        last_dx, last_dy = dx, dy

# تحويل timestamps من string إلى datetime
start_time = datetime.fromisoformat(moves[0]['timestamp'])
end_time = datetime.fromisoformat(moves[-1]['timestamp'])
duration = round((end_time - start_time).total_seconds(), 2)

# تحليل التكرار في نفس المكان
positions = [(log['x'], log['y']) for log in moves]
most_common_pos, count = Counter(positions).most_common(1)[0]
stuck = count / len(positions) > 0.5

# توليد توصيات
recommendations = []

if direction_changes < 5:
    recommendations.append("🧭 اللاعب ما غيّر الاتجاه كفاية – ممكن ما فهم طريقة التحكم.")

if duration < 10:
    recommendations.append(f"⏱️ مدة اللعب كانت قصيرة ({duration} ثانية) – اقترح عرض تعليمات أو تقليل صعوبة البداية.")

if stuck:
    recommendations.append(f"🚧 اللاعب ظل في نفس المكان {most_common_pos} لفترة طويلة – ضيف تنبيه عند التوقف.")

# طباعة التحليل
print("📊 تحليل الجلسة:")
print(f"- تغييرات الاتجاه: {direction_changes}")
print(f"- مدة الجلسة: {duration} ثانية")
print(f"- علق؟ {'نعم' if stuck else 'لا'}")

print("\n🔍 توصيات التصميم:")
if recommendations:
    for r in recommendations:
        print("-", r)
else:
    print("✅ الأداء ممتاز – لا توجد توصيات حالياً.")
