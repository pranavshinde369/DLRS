# Minimum Conformance Specification, MCS

## 硬门槛

| 项目 | 要求 |
|---|---|
| 主清单 | 必须有 `manifest.json` |
| 权利主体 | 仅接受 `self`、`authorized_agent`、`estate_authorized`、`public_data_only` |
| 同意证据 | 至少有一份同意/授权证据或公开资料说明 |
| 删除与撤回 | 必须声明 `deletion_policy` 与 `withdrawal_endpoint` |
| 跨境字段 | 必须声明 `cross_border_transfer_basis` |
| 审计 | 必须有 `audit/provenance.json` |
| 公开索引 | 必须通过 badge 与人工复核 |

## 建议门槛

| 项目 | 建议 |
|---|---|
| 语音 | 1–2 分钟为最低样本；专业克隆建议 30 分钟以上 |
| talking head 视频 | 至少 1080p、25fps、单人、单镜头、带口头同意 |
| 头像 | 至少一张 512×512 以上正脸照指针 |
| 3D | 至少支持 VRM 或 glTF 之一 |
| 公开输出 | 显式 AI 标识 + 隐式水印/内容凭证 |
