# Getting Started

## 建立母仓库

```bash
git init
git add .
git commit -m "Initial DLRS Hub"
```

## 新增一个参与者档案

```bash
python tools/new_human_record.py --record-id dlrs_xxxxxxxx --display-name "Name" --region asia --country cn
python tools/validate_repo.py
python tools/build_registry.py
```
