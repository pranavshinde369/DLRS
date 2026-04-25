# Runtime Interface

运行层不是母仓库必须实现的功能，但母仓库需要定义运行态配置：

- `runtime/build_spec.json`
- `runtime/session_policies.json`
- `runtime/prompts/system.md`
- `runtime/adapters.pointer.json`

运行态必须支持：

- 撤回同意后冻结；
- 公开输出带标识；
- 高风险用途拒绝；
- 审计会话创建和导出；
- 不暴露原始权重和敏感索引。
