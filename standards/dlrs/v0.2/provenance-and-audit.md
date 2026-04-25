# Provenance and Audit

每个档案至少记录以下事件：

- `record_created`
- `consent_submitted`
- `consent_verified`
- `artifact_registered`
- `build_started`
- `build_completed`
- `public_listing_requested`
- `public_listing_approved`
- `consent_withdrawn`
- `runtime_frozen`
- `takedown_requested`
- `export_requested`
- `record_deleted`

审计事件必须包含：`event_id`、`event_type`、`record_id`、`actor_role`、`timestamp`、`reason`、`hash`。
