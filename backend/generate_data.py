import json
import random
from datetime import datetime, timedelta

random.seed(42)

people = [
    "Rahul", "Priya", "Aman", "Neha",
    "Rohit", "Anjali", "Karan", "Sneha"
]

templates = [
    "bhai kya scene hai?",
    "haan bro",
    "kal milte hain",
    "assignment complete hua?",
    "notes bhej dena",
    "haan almost done",
    "okay cool",
    "wait kar",
    "kya plan hai?",
    "done 👍",
    "lol 😂",
    "same doubt",
    "check kar",
    "acha okay",
    "haan samajh gaya"
]

messages = []

# ---------------------------------------
# RANDOM CHAT
# ---------------------------------------

start = datetime(2026, 1, 1, 9, 0)

for i in range(3950):

    timestamp = start + timedelta(
        minutes=random.randint(0, 350000)
    )

    messages.append({
        "id": i + 1,
        "sender": random.choice(people),
        "timestamp": timestamp.isoformat(),
        "message": random.choice(templates)
    })


# ---------------------------------------
# IMPORTANT THREADS
# ---------------------------------------

threads = [

# MANALI
("Rahul", "2026-03-10T20:15:00",
 "guys break me kahi ghoomne chalte hain"),

("Priya", "2026-03-10T20:16:00",
 "mountains would be nice"),

("Aman", "2026-03-10T20:17:00",
 "Manali kaisa rahega?"),

("Neha", "2026-03-10T20:18:00",
 "haan mujhe Manali chalega"),

("Priya", "2026-03-10T20:20:00",
 "20 se 25 March mere liye free hai"),

("Aman", "2026-03-10T20:21:00",
 "8k per head ke around rakhte hain"),

("Neha", "2026-03-10T20:22:00",
 "ye budget reasonable hai"),

("Karan", "2026-03-10T20:23:00",
 "bus tickets main check kar leta hu"),

("Rahul", "2026-03-10T20:25:00",
 "done Manali locked then"),


# EVENT BUDGET
("Priya", "2026-05-18T18:10:00",
 "event expense sheet dekhi?"),

("Aman", "2026-05-18T18:12:00",
 "haan total expected se zyada hai"),

("Priya", "2026-05-18T18:14:00",
 "decorations unnecessary expensive hain"),

("Rahul", "2026-05-18T18:16:00",
 "lights vendor ka quote bahut high hai"),

("Priya", "2026-05-18T18:18:00",
 "main cheaper vendor se baat karti hu"),


# FINAL YEAR PROJECT
("Neha", "2026-07-05T21:00:00",
 "final year project ka idea?"),

("Rohit", "2026-07-05T21:02:00",
 "AI resume analyzer bana sakte hain"),

("Anjali", "2026-07-05T21:04:00",
 "dataset available hoga kya?"),

("Rohit", "2026-07-05T21:06:00",
 "public resume datasets mil jayenge"),

("Neha", "2026-07-05T21:08:00",
 "okay resume analyzer final"),


# PLACEMENT
("Sneha", "2026-08-03T12:10:00",
 "placement preparation ka kya scene?"),

("Rahul", "2026-08-03T12:12:00",
 "DSA daily kar raha hu"),

("Priya", "2026-08-03T12:14:00",
 "main aptitude start karungi"),

("Aman", "2026-08-03T12:16:00",
 "mock interviews weekend pe karte hain"),

("Sneha", "2026-08-03T12:18:00",
 "Saturday evening fixed"),


# FEST
("Karan", "2026-08-20T16:00:00",
 "fest ke liye sponsor kaun handle karega?"),

("Anjali", "2026-08-20T16:02:00",
 "main 2 companies ko mail karungi"),

("Rohit", "2026-08-20T16:05:00",
 "proposal ready hai"),

("Karan", "2026-08-20T16:07:00",
 "great kal bhej dete hain"),


# EXAM
("Rahul", "2026-08-25T19:00:00",
 "exam timetable dekha?"),

("Priya", "2026-08-25T19:02:00",
 "haan database ka paper pehle hai"),

("Aman", "2026-08-25T19:05:00",
 "DBMS ke notes kisi ke paas hain?"),

("Neha", "2026-08-25T19:07:00",
 "main pdf bhej deti hu")
]


for i, (sender, timestamp, message) in enumerate(threads):

    messages.append({
        "id": 5000 + i,
        "sender": sender,
        "timestamp": timestamp,
        "message": message
    })


with open(
    "data/messages.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        messages,
        f,
        ensure_ascii=False,
        indent=2
    )

print(f"Generated {len(messages)} messages")