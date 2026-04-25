# Registry

`registry/` 是母仓库的公开索引层。

## 文件

| 文件 | 作用 |
|---|---|
| `humans.index.jsonl` | 公开索引，机器读取 |
| `humans.index.csv` | 公开索引，人工浏览 |
| `badges.json` | badge 定义 |
| `regions.json` | 地区/法域代码 |
| `collections/*.jsonl` | 按用途拆分的集合索引 |

## 生成方式

```bash
python tools/build_registry.py
```
