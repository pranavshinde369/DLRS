# Directory Convention

人类档案建议按地区和国家/法域分层：

```text
humans/{region}/{country_or_jurisdiction}/{record_id_slug}/
```

示例：

```text
humans/asia/cn/dlrs_94f1c9b8_lin-example/
humans/europe/de/dlrs_abcd1234_anna-demo/
humans/north-america/us/dlrs_efgh5678_alex-demo/
```

`record_id_slug` 应由稳定 ID 和可读 slug 组成：

```text
dlrs_{8+ chars}_{display_slug}
```
