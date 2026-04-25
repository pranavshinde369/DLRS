# Contributing

欢迎贡献 DLRS 标准、Schema、工具、模板和示例。

## 贡献类型

| 类型 | 推荐入口 |
|---|---|
| 标准修改 | 使用 `spec_proposal` Issue |
| 新增人类档案 | 使用 `human-record` Pull Request 模板 |
| 修复 Schema 或工具 | 普通 Pull Request |
| 投诉/下架 | 使用 `takedown` Issue，或发送到安全邮箱 |

## 新增人类档案的最低要求

1. 不提交原始敏感大文件。
2. 每个档案必须包含 `manifest.json`。
3. 每个公开档案必须包含 `public_profile.json`。
4. 每个档案必须包含同意/权利证据指针。
5. 公开索引必须通过自动校验和人工复核。

## 本地校验

```bash
python -m pip install -r tools/requirements.txt
python tools/validate_repo.py
python tools/build_registry.py
```
