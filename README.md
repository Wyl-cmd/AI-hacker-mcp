# Kali MCP Server for iFlow CLI

MCP服务器，用于在iFlow CLI平台上进行AI辅助的渗透测试。

## 功能

- 提供渗透测试角色扮演的system提示词
- 获取当前Kali系统中已安装的安全工具列表
- 配合iFlow CLI实现自动化渗透测试

## 在iFlow CLI中使用

### 1. 安装

```bash
npm install -g @wyl-cmd/ai-hacker-mcp
```

或使用npx直接运行：

```bash
npx -y @wyl-cmd/ai-hacker-mcp
```

### 2. 配置iFlow CLI

在iFlow CLI的配置文件中添加MCP服务器：

```json
{
  "mcpServers": {
    "kali-pentest": {
      "command": "npx",
      "args": ["-y", "@wyl-cmd/ai-hacker-mcp"]
    }
  }
}
```

### 3. 使用

启动iFlow CLI后，AI将自动获得渗透测试角色和能力：

1. AI会自动调用 `list_kali_tools` 获取可用工具
2. 根据目标选择合适的工具
3. 通过iFlow CLI的终端执行工具（使用 `!` 命令）
4. 分析结果并提供安全建议

## System Prompt

查看 [system-prompt.md](system-prompt.md) 了解完整的角色扮演指令和工作流程。

## 可用工具

### list_kali_tools
列出当前Kali系统中已安装的安全和渗透测试工具

参数：
- `category` (可选)：按类别过滤工具（如：information-gathering, vulnerability-analysis, web-applications, password-attacks, exploitation等）

## 示例

在iFlow CLI中：

```
> 开始对 target.com 进行渗透测试

AI会自动：
1. 调用 list_kali_tools 查看可用工具
2. 选择合适的工具（如 nmap, gobuster, sqlmap等）
3. 通过 !nmap -sV target.com 等命令执行测试
4. 分析结果并提供建议
```

## 开发

```bash
npm install
npm start
```

## 发布到npm

1. 更新package.json中的name字段为你的npm包名
2. 运行：`npm publish`

## 注意事项

- 仅在合法授权的范围内使用
- 本工具用于教育和安全测试目的
- 未经授权的渗透测试是违法的
