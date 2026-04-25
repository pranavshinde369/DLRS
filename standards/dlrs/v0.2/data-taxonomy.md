# Data Taxonomy

## 敏感级别

| 级别 | 示例 | 默认策略 |
|---|---|---|
| S0 Public | 公开简介、公开作品链接 | 可公开 |
| S1 Internal | 非敏感摘要、低风险元数据 | 私有或团队可见 |
| S2 Sensitive | 聊天记录、关系图谱、偏好 | 默认私有 |
| S3 Biometric | 声纹、人脸、步态、视频训练集 | 默认私有，单独同意 |
| S4 Restricted | 证件、未成年人、健康、逝者争议 | 禁止公开索引，需人工复核 |

## 数据类型

- `text_corpus`
- `voice_sample`
- `training_video_head`
- `training_video_full_body`
- `headshot`
- `avatar_vrm`
- `avatar_gltf`
- `avatar_openusd`
- `memory_atoms`
- `knowledge_graph`
- `embedding_index`
- `audit_log`
- `consent_evidence`
