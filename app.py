"""郵遞區號查詢網頁應用程式"""

from flask import Flask, render_template, request, jsonify
from postal import query_zipcode

app = Flask(__name__)


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/api/query")
def api_query():
    body = request.get_json(silent=True) or {}
    address = (body.get("address") or "").strip()
    if not address:
        return jsonify({"success": False, "error": "請輸入地址。"})

    try:
        data = query_zipcode(address)
    except Exception as e:
        return jsonify({"success": False, "error": f"查詢失敗：{e}"})

    zipcode6 = (data.get("zipcode6") or "").strip()
    zipcode5 = (data.get("zipcode") or "").strip()
    std_adrs = (data.get("new_adrs6") or data.get("new_adrs") or "").strip()
    clean_adrs = std_adrs.lstrip("0123456789 \u3000").strip()

    if zipcode6:
        return jsonify({
            "success": True,
            "code": zipcode6,
            "label": "6碼郵遞區號",
            "std_address": clean_adrs,
        })
    elif zipcode5:
        return jsonify({
            "success": True,
            "code": zipcode5,
            "label": "5碼郵遞區號（查無6碼資料）",
            "std_address": clean_adrs,
        })
    else:
        return jsonify({
            "success": False,
            "error": f"找不到「{address}」的郵遞區號，請確認地址是否正確。",
        })
