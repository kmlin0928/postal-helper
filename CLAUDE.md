# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# Python 環境

- 使用 uv 管理 Python 環境
- 回覆是中文時，請都使用台灣繁體中文

# 常用指令

```bash
# 執行主程式（命令列模式）
uv run python postal.py <地址>

# 執行主程式（互動模式）
uv run python postal.py

# 執行測試，結果寫入 test_result.txt
uv run python test_postal.py
```

# 架構說明

純標準函式庫實作，無第三方依賴。

- `postal.py` — 核心邏輯，含兩個函式：
  - `query_zipcode(address)` — 呼叫 `zip5.5432.tw` API，回傳原始 dict
  - `format_result(data, address)` — 格式化輸出；優先顯示 6 碼（`zipcode6`），無 6 碼時顯示 5 碼並加註「查無6碼資料」
- `test_postal.py` — 以固定地址呼叫上述函式，將結果寫入 `test_result.txt`

# API 說明

- 端點：`https://zip5.5432.tw/zip5json.py?adrs=<地址>`
- 回傳欄位：`zipcode6`（6碼）、`zipcode`（5碼）、`new_adrs6` / `new_adrs`（標準化地址）
- 部分地址 `zipcode6` 為空字串，程式需正確 fallback 至 5 碼
