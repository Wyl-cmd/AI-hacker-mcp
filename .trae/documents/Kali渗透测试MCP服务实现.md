## 简化Kali MCP服务 - 只提供提示词和工具列表

### 修改内容：

1. **简化 src/index.js**
   - 添加 `list_kali_tools` 工具（获取当前系统中实际存在的Kali工具）
   - 移除 `execute_command` 工具（iflow-cli本身就能控制终端）
   - 移除 `get_system_info` 工具

2. **创建 system-prompt.md**
   - 角色扮演指令（网络安全人员）
   - 指导AI自动发现和使用Kali工具
   - 不包含具体接入点信息

3. **更新 package.json**
   - 调整描述为提示词和工具列表服务

4. **更新 README.md**
   - 专注于iFlow CLI使用说明
   - 简化文档

### 核心功能：
- 提供渗透测试角色扮演的system提示词
- 获取当前系统中实际存在的Kali工具列表
- 让AI通过iflow-cli控制终端执行工具