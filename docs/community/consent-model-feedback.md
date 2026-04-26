# Request for Feedback: DLRS v0.2 Consent Model and Privacy Boundary

**Status**: Open for Discussion  
**Version**: DLRS v0.2 Draft  
**Last Updated**: 2026-04-26

---

## English Version

### Overview

The DLRS v0.2 consent model is a critical component of the standard. We need community feedback to ensure it adequately protects privacy, respects autonomy, and provides clear boundaries for what can and cannot be done with digital life archives.

---

### Key Questions for Discussion

#### 1. What data should NEVER be stored directly in Git?

**Current recommendation**:
- ❌ Raw biometric data (fingerprints, iris scans, DNA sequences)
- ❌ High-resolution face images
- ❌ Raw voice recordings
- ❌ Identity documents (passports, national IDs, driver's licenses)
- ❌ Medical records
- ❌ Financial information
- ❌ Private keys, passwords, or authentication tokens

**Questions**:
- Is this list complete?
- Should we allow low-resolution thumbnails?
- What about voice samples under 10 seconds?
- Should text transcripts of conversations be restricted?

---

#### 2. How should consent be recorded?

**Current approach**:
```
consent/
├── consent_statement.md (written statement)
├── consent_video.pointer.json (video recording, external)
├── id_verification.pointer.json (ID verification, external)
└── signer_signature.json (digital signature)
```

**Questions**:
- Is a written statement sufficient?
- Should video consent be mandatory?
- How should we verify identity?
- What if the person cannot provide video consent (disability, etc.)?
- Should we require witness signatures?
- How often should consent be reaffirmed?

---

#### 3. How should withdrawal be handled?

**Current approach**:
- User contacts `consent.withdrawal_endpoint`
- Archive is frozen (not immediately deleted)
- Review period (e.g., 30 days) for verification
- After review, archive is deleted or anonymized
- Audit logs are retained

**Questions**:
- Is 30 days an appropriate review period?
- Should deletion be immediate in some cases?
- What should happen to derived data (embeddings, summaries)?
- Should heirs be able to override withdrawal?
- How should we handle partial withdrawal (e.g., "delete voice but keep text")?

---

#### 4. How should biometric, voice, image, memory, and avatar data be referenced safely?

**Current approach**: Use pointer files

```json
{
  "artifact_id": "voice_001",
  "type": "voice_sample",
  "format": "wav",
  "storage_uri": "s3://bucket/voice/master.wav",
  "checksum": "sha256:abc123...",
  "size_bytes": 1048576,
  "region": "CN",
  "sensitivity": "S3_BIOMETRIC",
  "contains_sensitive_data": true,
  "encryption": "AES256",
  "access_control": "private"
}
```

**Questions**:
- Should we mandate encryption?
- Should we support multiple storage backends?
- How should we handle storage provider failures?
- Should checksums be mandatory?
- What metadata is safe to store in Git?

---

#### 5. What should be FORBIDDEN even with consent?

**Current prohibitions**:
- ❌ Using archives for harassment, fraud, or impersonation
- ❌ Creating deepfakes without clear AI disclosure
- ❌ Selling or transferring archives without explicit permission
- ❌ Using archives for political manipulation
- ❌ Creating archives of minors without guardian consent
- ❌ Creating archives of deceased persons without estate authorization

**Questions**:
- Is this list sufficient?
- Should we prohibit commercial use entirely?
- Should we prohibit certain types of AI training?
- What about research use?
- Should there be geographic restrictions?

---

#### 6. How should heirs, guardians, or institutions interact with a digital-life archive?

**Current approach**:
- Heirs must provide `inheritance_policy.json`
- Guardians must provide `guardian_consent` for minors
- Institutions must provide `authorized_agent` documentation
- All must respect original consent boundaries

**Questions**:
- Should heirs have full control or limited access?
- Can heirs modify the archive?
- Can heirs revoke consent on behalf of the deceased?
- How should we handle disputes between heirs?
- Should institutions have different rules than individuals?
- What if there's no inheritance policy?

---

#### 7. How should AI-generated or synthetic content be marked?

**Current approach**:
- All AI-generated content must have `ai_generated: true` flag
- Watermarks recommended for images and videos
- C2PA content credentials recommended
- Clear disclosure in public outputs

**Questions**:
- Is metadata marking sufficient?
- Should watermarks be mandatory?
- How should we handle partially AI-edited content?
- What about AI-assisted transcription or translation?
- Should there be different levels of AI involvement?

---

### Recommended Best Practices

#### ✅ DO:
- Store only metadata and pointers in Git
- Use encrypted external storage for sensitive files
- Require explicit consent for each use case
- Provide clear withdrawal mechanisms
- Mark all AI-generated content
- Respect sensitivity levels
- Maintain audit logs
- Provide data export functionality

#### ❌ DON'T:
- Store raw biometric data in Git
- Assume consent is permanent
- Use archives without checking permissions
- Create deepfakes without disclosure
- Transfer archives without permission
- Ignore withdrawal requests
- Delete audit logs
- Make legal guarantees

---

### Privacy Boundary Examples

#### Example 1: Voice Clone Training

**Scenario**: User wants to train a voice clone

**Consent requirements**:
- ✅ Explicit consent for voice cloning
- ✅ Consent for specific use cases (personal assistant, memorial, etc.)
- ✅ Understanding that voice can be misused
- ✅ Right to revoke at any time

**Storage**:
- ❌ Don't store raw audio in Git
- ✅ Store pointer to encrypted S3/OSS storage
- ✅ Store metadata (duration, language, quality)
- ✅ Store checksum for verification

**Usage**:
- ✅ Only for consented use cases
- ✅ Must mark outputs as AI-generated
- ✅ Must respect withdrawal requests
- ❌ Cannot be sold or transferred without permission

---

#### Example 2: Memorial Archive

**Scenario**: Family wants to create a memorial for deceased person

**Consent requirements**:
- ✅ Inheritance policy from deceased (if available)
- ✅ Estate authorization
- ✅ Consent from all heirs (if disputed)
- ✅ Respect deceased's original consent boundaries

**Storage**:
- ✅ Can use public_unlisted or public_indexed visibility
- ✅ Must mark as memorial archive
- ✅ Must include provenance information
- ❌ Cannot add new data without authorization

**Usage**:
- ✅ Can display publicly if authorized
- ✅ Can create AI avatar if originally consented
- ❌ Cannot use for commercial purposes without permission
- ❌ Cannot modify original consent terms

---

#### Example 3: Research Dataset

**Scenario**: Researcher wants to use archives for AI training

**Consent requirements**:
- ✅ Explicit consent for research use
- ✅ IRB approval (if applicable)
- ✅ Data use agreement
- ✅ Right to withdraw from research

**Storage**:
- ✅ Can use anonymized or pseudonymized data
- ✅ Must maintain consent records
- ✅ Must provide data export
- ❌ Cannot re-identify individuals

**Usage**:
- ✅ Only for approved research purposes
- ✅ Must publish results with proper attribution
- ✅ Must respect withdrawal requests
- ❌ Cannot commercialize without separate consent

---

## 中文版本

### 概述

DLRS v0.2 授权模型是标准的关键组成部分。我们需要社区反馈，以确保它充分保护隐私、尊重自主权，并为数字生命档案的使用提供明确边界。

---

### 讨论的关键问题

#### 1. 哪些数据绝不应直接存储在 Git 中？

**当前建议**：
- ❌ 原始生物识别数据（指纹、虹膜扫描、DNA 序列）
- ❌ 高分辨率人脸图像
- ❌ 原始语音录音
- ❌ 身份证明文件（护照、身份证、驾照）
- ❌ 医疗记录
- ❌ 财务信息
- ❌ 私钥、密码或认证令牌

**问题**：
- 这个列表完整吗？
- 是否应允许低分辨率缩略图？
- 10 秒以下的语音样本呢？
- 对话的文本转录是否应受限？

---

#### 2. 授权应如何记录？

**当前方法**：
```
consent/
├── consent_statement.md（书面声明）
├── consent_video.pointer.json（视频录制，外部）
├── id_verification.pointer.json（身份验证，外部）
└── signer_signature.json（数字签名）
```

**问题**：
- 书面声明是否足够？
- 视频授权是否应强制要求？
- 应如何验证身份？
- 如果无法提供视频授权（残疾等）怎么办？
- 是否应要求见证人签名？
- 授权应多久重新确认一次？

---

#### 3. 撤回应如何处理？

**当前方法**：
- 用户联系 `consent.withdrawal_endpoint`
- 档案被冻结（不立即删除）
- 审核期（例如 30 天）用于验证
- 审核后，档案被删除或匿名化
- 保留审计日志

**问题**：
- 30 天是否是合适的审核期？
- 在某些情况下是否应立即删除？
- 派生数据（嵌入、摘要）应如何处理？
- 继承人是否可以推翻撤回？
- 如何处理部分撤回（例如"删除语音但保留文本"）？

---

#### 4. 生物识别、语音、图像、记忆和虚拟形象数据应如何安全引用？

**当前方法**：使用指针文件

```json
{
  "artifact_id": "voice_001",
  "type": "voice_sample",
  "format": "wav",
  "storage_uri": "s3://bucket/voice/master.wav",
  "checksum": "sha256:abc123...",
  "size_bytes": 1048576,
  "region": "CN",
  "sensitivity": "S3_BIOMETRIC",
  "contains_sensitive_data": true,
  "encryption": "AES256",
  "access_control": "private"
}
```

**问题**：
- 是否应强制加密？
- 是否应支持多个存储后端？
- 如何处理存储提供商故障？
- 校验和是否应强制要求？
- 哪些元数据可以安全存储在 Git 中？

---

#### 5. 即使有授权，哪些行为也应被禁止？

**当前禁止事项**：
- ❌ 使用档案进行骚扰、欺诈或冒充
- ❌ 创建深度伪造而不明确披露 AI
- ❌ 未经明确许可出售或转让档案
- ❌ 使用档案进行政治操纵
- ❌ 未经监护人同意创建未成年人档案
- ❌ 未经遗产授权创建已故者档案

**问题**：
- 这个列表是否充分？
- 是否应完全禁止商业使用？
- 是否应禁止某些类型的 AI 训练？
- 研究用途呢？
- 是否应有地理限制？

---

#### 6. 继承人、监护人或机构应如何与数字生命档案互动？

**当前方法**：
- 继承人必须提供 `inheritance_policy.json`
- 监护人必须为未成年人提供 `guardian_consent`
- 机构必须提供 `authorized_agent` 文档
- 所有人必须尊重原始授权边界

**问题**：
- 继承人应拥有完全控制权还是有限访问权？
- 继承人可以修改档案吗？
- 继承人可以代表已故者撤销授权吗？
- 如何处理继承人之间的争议？
- 机构是否应有不同于个人的规则？
- 如果没有继承政策怎么办？

---

#### 7. AI 生成或合成内容应如何标记？

**当前方法**：
- 所有 AI 生成的内容必须有 `ai_generated: true` 标志
- 建议为图像和视频添加水印
- 建议使用 C2PA 内容凭证
- 在公开输出中明确披露

**问题**：
- 元数据标记是否足够？
- 水印是否应强制要求？
- 如何处理部分 AI 编辑的内容？
- AI 辅助转录或翻译呢？
- 是否应有不同级别的 AI 参与？

---

### 推荐最佳实践

#### ✅ 应该：
- 仅在 Git 中存储元数据和指针
- 对敏感文件使用加密外部存储
- 对每个用例要求明确授权
- 提供明确的撤回机制
- 标记所有 AI 生成的内容
- 尊重敏感度级别
- 维护审计日志
- 提供数据导出功能

#### ❌ 不应该：
- 在 Git 中存储原始生物识别数据
- 假设授权是永久的
- 未检查权限就使用档案
- 创建深度伪造而不披露
- 未经许可转让档案
- 忽略撤回请求
- 删除审计日志
- 做出法律保证

---

### 隐私边界示例

#### 示例 1：语音克隆训练

**场景**：用户想要训练语音克隆

**授权要求**：
- ✅ 明确授权语音克隆
- ✅ 授权特定用例（个人助理、纪念等）
- ✅ 理解语音可能被滥用
- ✅ 随时撤销的权利

**存储**：
- ❌ 不要在 Git 中存储原始音频
- ✅ 存储指向加密 S3/OSS 存储的指针
- ✅ 存储元数据（时长、语言、质量）
- ✅ 存储校验和以供验证

**使用**：
- ✅ 仅用于授权的用例
- ✅ 必须将输出标记为 AI 生成
- ✅ 必须尊重撤回请求
- ❌ 未经许可不能出售或转让

---

#### 示例 2：纪念档案

**场景**：家人想为已故者创建纪念档案

**授权要求**：
- ✅ 已故者的继承政策（如果有）
- ✅ 遗产授权
- ✅ 所有继承人的同意（如有争议）
- ✅ 尊重已故者的原始授权边界

**存储**：
- ✅ 可以使用 public_unlisted 或 public_indexed 可见性
- ✅ 必须标记为纪念档案
- ✅ 必须包含来源信息
- ❌ 未经授权不能添加新数据

**使用**：
- ✅ 如果授权可以公开展示
- ✅ 如果最初授权可以创建 AI 虚拟形象
- ❌ 未经许可不能用于商业目的
- ❌ 不能修改原始授权条款

---

#### 示例 3：研究数据集

**场景**：研究人员想使用档案进行 AI 训练

**授权要求**：
- ✅ 明确授权研究使用
- ✅ IRB 批准（如适用）
- ✅ 数据使用协议
- ✅ 退出研究的权利

**存储**：
- ✅ 可以使用匿名或假名数据
- ✅ 必须维护授权记录
- ✅ 必须提供数据导出
- ❌ 不能重新识别个人

**使用**：
- ✅ 仅用于批准的研究目的
- ✅ 必须以适当归属发布结果
- ✅ 必须尊重撤回请求
- ❌ 未经单独授权不能商业化

---

## How to Provide Feedback

1. **Open an Issue**: Use the "Consent Model Feedback" template
2. **Comment on this document**: Submit a PR with your suggestions
3. **Start a Discussion**: Use GitHub Discussions
4. **Email**: Contact maintainers (see SECURITY.md)

---

## Related Documents

- [RFC: DLRS v0.2](RFC-DLRS-v0.2.md)
- [Privacy Policy](../../policies/privacy.md)
- [Consent Schema](../../schemas/consent.schema.json)
- [Manifest Schema](../../schemas/manifest.schema.json)

---

## License

This document is part of the DLRS project and is licensed under MIT License.
