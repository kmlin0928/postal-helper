#!/usr/bin/env python3
"""台灣郵遞區號查詢小幫手 - 使用 zip5.5432.tw API"""

import sys
import urllib.request
import urllib.parse
import json


API_URL = "https://zip5.5432.tw/zip5json.py"


def query_zipcode(address: str) -> dict:
    """查詢地址對應的郵遞區號，回傳 API 原始結果。"""
    params = urllib.parse.urlencode({"adrs": address})
    url = f"{API_URL}?{params}"
    req = urllib.request.Request(url, headers={"User-Agent": "postal-helper/1.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data


def format_result(data: dict, address: str) -> str:
    """將 API 回傳資料格式化為易讀字串。"""
    zipcode6 = data.get("zipcode6", "").strip()
    zipcode5 = data.get("zipcode", "").strip()
    std_adrs = data.get("new_adrs6", data.get("new_adrs", "")).strip()

    if zipcode6:
        code = zipcode6
        label = "6碼郵遞區號"
    elif zipcode5:
        code = zipcode5
        label = "5碼郵遞區號（查無6碼資料）"
    else:
        return f"找不到「{address}」的郵遞區號，請確認地址是否正確。"

    lines = [f"{label}: {code}"]
    if std_adrs:
        # 標準化地址通常包含郵遞區號前綴，去掉後只留地址
        clean = std_adrs.lstrip("0123456789 　").strip()
        if clean:
            lines.append(f"標準地址: {clean}")
    return "\n".join(lines)


def main():
    if len(sys.argv) > 1:
        # 從命令列參數取得地址（支援多個 token 合併）
        addresses = [" ".join(sys.argv[1:])]
    else:
        # 互動模式
        print("台灣郵遞區號查詢 (輸入地址後按 Enter，輸入 q 離開)")
        addresses = []
        while True:
            try:
                line = input("> ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                break
            if line.lower() in ("q", "quit", "exit"):
                break
            if line:
                addresses.append(line)
                # 互動模式：查詢後繼續等待輸入
                try:
                    data = query_zipcode(line)
                    print(format_result(data, line))
                except Exception as e:
                    print(f"查詢失敗: {e}", file=sys.stderr)
        return

    # 批次查詢（命令列參數模式）
    for addr in addresses:
        try:
            data = query_zipcode(addr)
            print(format_result(data, addr))
        except Exception as e:
            print(f"查詢失敗: {e}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
