"""測試 postal.py 的功能，結果寫到 test_result.txt"""
import sys
import urllib.request
import urllib.parse
import json

sys.path.insert(0, "C:/Users/charl/Downloads/postal-helper")
from postal import query_zipcode, format_result

TEST_CASES = [
    ("台北市杭州南路一段23號",   "應有6碼結果"),
    ("高雄市前金區中正四路211號", "應有6碼結果"),
]

results = []
for addr, note in TEST_CASES:
    try:
        data = query_zipcode(addr)
        output = format_result(data, addr)
        raw_z6 = data.get("zipcode6", "")
        raw_z5 = data.get("zipcode", "")
        results.append(
            f"[輸入] {addr}\n"
            f"[備註] {note}\n"
            f"[API zipcode6] {raw_z6!r}\n"
            f"[API zipcode]  {raw_z5!r}\n"
            f"[輸出]\n{output}\n"
        )
    except Exception as e:
        results.append(f"[輸入] {addr}\n[錯誤] {e}\n")

report = "\n" + ("=" * 50 + "\n").join(results)
with open("C:/Users/charl/Downloads/postal-helper/test_result.txt", "w", encoding="utf-8") as f:
    f.write(report)

print("Done")
