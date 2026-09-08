import json
import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

from backend.search import search


with open("tests/queries.json", "r", encoding="utf-8") as f:
    queries = json.load(f)


correct = 0

for i, test in enumerate(queries, 1):

    results = search(test["query"], top_k=5)

    returned_ids = [
        r["message"]["id"]
        for r in results
    ]

    expected = test["expected_message_id"]

    if expected in returned_ids:
        correct += 1
        status = "✅"
    else:
        status = "❌"

    print(
        f"{status} {i:02d} | "
        f"Expected: {expected} | "
        f"Found: {returned_ids}"
    )


total = len(queries)

print("\n" + "=" * 50)
print(f"Correct: {correct}/{total}")
print(f"Top-5 Retrieval Accuracy: {(correct/total)*100:.2f}%")
print("=" * 50)