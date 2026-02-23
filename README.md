# postal-helper

台灣郵遞區號查詢小幫手，使用 [zip5.5432.tw](https://zip5.5432.tw) API。

## 功能

- 輸入台灣地址，查詢對應的郵遞區號
- 優先顯示 6 碼郵遞區號，無 6 碼時自動 fallback 至 5 碼
- 支援命令列與互動兩種模式

## 環境需求

- [uv](https://github.com/astral-sh/uv)

## 使用方式

**命令列模式**

```bash
uv run python postal.py 台北市杭州南路一段23號
```

**互動模式**

```bash
uv run python postal.py
```

## 執行測試

```bash
uv run python test_postal.py
```

結果會寫入 `test_result.txt`。
