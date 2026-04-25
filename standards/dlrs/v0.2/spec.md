# DLRS v0.2 Standard

## 1. 范围

DLRS v0.2 适用于以下场景：

- 个人自愿创建数字生命档案；
- 家庭/遗产授权的纪念型档案；
- 研究型、非公开或受限公开人格样本；
- 可被文本、语音、视频或 3D avatar 运行时调用的档案；
- 全球母仓库中的公开索引与社区治理。

不适用于：未经授权的第三人克隆、未成年人公开克隆、身份认证、金融/医疗/法律/雇佣高风险决策。

## 2. 四层分离

| 层 | 内容 | GitHub 中保存什么 |
|---|---|---|
| Raw | 原始文本、音频、视频、图像、证件、同意视频 | pointer、hash、region、sensitivity |
| Derived | 转写、切片、embedding、memory atoms、KG | 摘要、schema、低风险派生样例 |
| Runtime | prompt、adapter、voice profile、avatar config | 配置、版本、hash、禁止直接下载的权重指针 |
| Public Output | 公开展示内容、gallery、示例片段 | 标识、权限、输出记录、C2PA/watermark 指针 |

## 3. 档案准入

每个档案至少包含：

- `manifest.json`
- `public_profile.json`，若完全私有可最小化
- `consent/` 目录
- `profile/` 目录
- `artifacts/raw_pointers/` 目录
- `audit/` 目录

## 4. 公开索引准入

公开索引必须满足：

1. `visibility` 为 `public_indexed` 或 `public_unlisted`。
2. `rights.allow_public_listing` 为 `true`。
3. `review.status` 为 `approved_public`。
4. 具有 `verified-consent` 或 `public-data-only` badge。
5. 主体不是未成年人。
6. 有撤回入口、删除策略和审计记录。

## 5. 母仓库职责

母仓库负责：

- 发布标准；
- 保存模板；
- 接受自愿参与档案；
- 构建公开索引；
- 管理 badge；
- 处理投诉、撤回和下架；
- 维护工具链。

母仓库不应承担：

- 直接托管高敏感原始素材；
- 承诺“复活真人”；
- 对数字生命输出真实性作保证；
- 绕过目标法域的个人信息与肖像/声纹规则。
