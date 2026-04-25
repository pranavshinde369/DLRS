# DLRS Hub：全球数字生命母仓库模板

> Digital Life Repository Standard Hub，简称 **DLRS Hub**。  
> 这是一个用于建立“全球数字生命计划”的母仓库结构：它既保存标准、模板、Schema、工具和治理规则，也可以收纳自愿参与者的数字生命档案索引。

## 这个仓库解决什么问题

DLRS Hub 的目标不是把每个人的原始音视频直接塞进 GitHub，而是建立一个可审计、可撤回、可验证、可扩展的数字生命档案体系。

本仓库默认遵守以下原则：

1. **原始敏感素材不直接入 Git**：音频、视频、证件、人脸、声纹、聊天记录等高敏感材料应进入区域化对象存储，本仓库只保存 `.pointer.json`、哈希、摘要、同意证据指针与审核状态。
2. **自愿参与优先**：公开索引只接收本人授权、自愿参与、可撤回的档案。
3. **公开不等于无限使用**：每个档案必须声明是否允许公开展示、模型微调、语音克隆、avatar 克隆、商业化、跨境处理。
4. **先冻结，后复核，再删除**：遇到投诉、冒充、撤回同意、继承争议时，先冻结运行态并保留必要审计证据。
5. **AI 合成必须标识**：任何公开输出都必须显式标记为 AI 生成/编辑内容，音视频建议额外加入隐式水印或 C2PA 内容凭证。

## 仓库总结构

```text
.
├─ standards/              # DLRS 标准正文、版本和规范
├─ schemas/                # 机器可校验 JSON Schema
├─ registry/               # 全局公开索引、徽章、地区和集合索引
├─ humans/                 # 自愿参与者档案目录，按地区/法域分层
├─ templates/              # 各类档案模板、同意书、PR 包
├─ examples/               # 示例档案，不含真实敏感数据
├─ tools/                  # 校验、建索引、新建档案脚本
├─ policies/               # 隐私、下架、未成年人、逝者、跨境等政策
├─ operations/             # 审核台、事故响应、SLA、徽章签发手册
├─ api/                    # 仓库层 / 运行层接口草案
├─ docs/                   # 上手指南、架构图、FAQ、原始草案
└─ .github/                # PR 模板、Issue 模板、CI 校验
```

## 三类核心对象

| 对象 | 所在目录 | 作用 |
|---|---|---|
| 标准 | `standards/dlrs/` | 定义 DLRS 的最低合格规范、目录规范、权限模型、审计模型 |
| 模板 | `templates/` | 供新参与者复制填写，生成自己的数字生命档案 |
| 人类档案 | `humans/{region}/{country}/{record_id_slug}/` | 自愿参与者的档案清单、授权状态、公开资料和指针 |

## 自愿参与者如何加入

1. 复制 `templates/archive-types/self-owned/` 到 `humans/{region}/{country}/{record_id_slug}/`。
2. 填写 `manifest.json`、`public_profile.json`、`consent/consent_statement.md`。
3. 所有大文件只填写 `.pointer.json`，不要直接提交原始敏感素材。
4. 运行：

```bash
python tools/validate_repo.py
python tools/build_registry.py
```

5. 提交 Pull Request，并选择 `.github/PULL_REQUEST_TEMPLATE/human-record.md`。

## 公开索引准入条件

一个档案要进入 `registry/humans.index.jsonl`，至少需要：

- `review.status = approved_public`
- `visibility = public_indexed` 或 `public_unlisted`
- `review.verified_consent_badge = true` 或 `review.public_data_only_badge = true`
- `rights.allow_public_listing = true`
- `consent.withdrawal_endpoint` 非空
- 未成年人档案不得公开索引
- 逝者档案必须有 `profile/inheritance_policy.json`

## 当前状态

这是 **v0.2 母仓库结构草案**。适合用作 GitHub 新仓库的初始提交。

## 重要提醒

本项目涉及肖像、声纹、生物识别、个人信息、逝者权益、跨境传输、AI 合成标识和深伪滥用风险。正式上线前必须由目标法域律师审核 `policies/`、`templates/consent/` 和 `LEGAL_DISCLAIMER.md`。
