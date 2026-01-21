# Kali MCP Server - Python Version v2.1.0

## 功能说明

这个MCP（Model Context Protocol）服务器为Kali Linux渗透测试提供AI辅助功能，集成了PortSwigger官方Burp Suite MCP扩展的所有核心功能，支持多协议通信。

### 核心功能

#### 1. 多协议支持

- **Stdio传输** - 主要MCP通信方式，通过标准输入/输出流
- **SSE服务器** - HTTP Server-Sent Events，支持实时事件推送（http://localhost:9877）
- **WebSocket服务器** - 双向实时通信（ws://localhost:9878）
- **HTTP服务器** - 处理MCP HTTP请求（http://localhost:9879）

#### 2. 工具集（17个工具）

##### Kali Linux 工具管理

| 工具名称 | 描述 | 参数 |
|---------|------|------|
| `run_security_tool` | 执行任意安全工具 | `tool` (必需), `arguments`, `target` |

##### Burp Suite 集成工具

| 工具名称 | 描述 | 参数 |
|---------|------|------|
| `burp_health_check` | 检查Burp Suite是否安装 | 无 |
| `burp_start` | 启动Burp Suite | `version`, `config`, `headless`, `port` |
| `burp_scan` | 运行Burp Suite漏洞扫描 | `target` (必需), `config`, `output`, `scope`, `scan_type` |
| `burp_get_config` | 获取Burp Suite MCP服务器配置 | 无 |
| `burp_set_config` | 设置Burp Suite MCP服务器配置 | `enabled`, `port`, `host`, `allowConfigEdit` |

##### HTTP 请求工具

| 工具名称 | 描述 | 参数 |
|---------|------|------|
| `send_http1_request` | 发送HTTP/1.1请求并返回响应 | `method`, `url` (必需), `headers`, `body` |
| `send_http2_request` | 发送HTTP/2请求并返回响应 | `method`, `url` (必需), `pseudo_headers`, `headers`, `body` |

##### 编码/解码工具

| 工具名称 | 描述 | 参数 |
|---------|------|------|
| `url_encode` | URL编码输入字符串 | `content` (必需) |
| `url_decode` | URL解码输入字符串 | `content` (必需) |
| `base64_encode` | Base64编码输入字符串 | `content` (必需) |
| `base64_decode` | Base64解码输入字符串 | `content` (必需) |
| `generate_random_string` | 生成指定长度和字符集的随机字符串 | `length`, `characterSet` |

##### Burp Suite 控制工具

| 工具名称 | 描述 | 参数 |
|---------|------|------|
| `create_repeater_tab` | 使用指定HTTP请求创建新的Repeater标签页 | `request` (必需), `tabName` |
| `send_to_intruder` | 将HTTP请求发送到Intruder | `request` (必需), `tabName` |
| `set_proxy_intercept_state` | 启用或禁用Burp代理拦截 | `intercepting` (必需) |
| `set_task_execution_engine_state` | 设置Burp任务执行引擎状态（暂停或未暂停） | `running` (必需) |

##### Burp Suite 配置和历史记录工具

| 工具名称 | 描述 | 参数 |
|---------|------|------|
| `output_project_options` | 输出项目级配置（JSON格式） | 无 |
| `output_user_options` | 输出用户级配置（JSON格式） | 无 |
| `set_project_options` | 设置项目级配置（JSON格式） | `json` |
| `set_user_options` | 设置用户级配置（JSON格式） | `json` |
| `get_scanner_issues` | 显示扫描器识别的问题 | `count`, `offset` |
| `get_proxy_http_history` | 显示代理HTTP历史记录 | `count`, `offset` |
| `get_proxy_http_history_regex` | 使用正则表达式过滤代理HTTP历史 | `regex`, `count`, `offset` |
| `get_proxy_websocket_history` | 显示代理WebSocket历史记录 | `count`, `offset` |
| `get_proxy_websocket_history_regex` | 使用正则表达式过滤代理WebSocket历史 | `regex`, `count`, `offset` |
| `get_active_editor_contents` | 输出用户的活动消息编辑器内容 | 无 |
| `set_active_editor_contents` | 设置用户的活动消息编辑器内容 | `text` |

#### 3. 提示词资源（1个）

- **pentest-role** - 渗透测试角色扮演提示词，包含Burp Suite安全测试助手功能
  - 参数：`target` - 目标网站，`scan_type` - 扫描类型
  - 包含完整的渗透测试流程和Burp Suite功能说明

#### 4. 配置管理

- **GetConfigRequestSchema** - 获取服务器配置
- **SetConfigRequestSchema** - 设置服务器配置
- 支持动态配置SSE、WebSocket和HTTP服务器

#### 5. 服务器描述

- **DescribeServerRequestSchema** - 提供服务器元数据和功能列表

## 安装和使用

### 前置要求

- Python 3.8+
- Kali Linux环境（用于安全工具）
- Burp Suite（可选，用于Burp相关功能）
- aiohttp（用于HTTP请求）
- websockets（用于WebSocket支持）

### 安装步骤

1. **克隆或下载项目**

```bash
git clone https://github.com/Wyl-cmd/AI-hacker-mcp.git
cd AI-hacker-mcp
```

2. **创建Python虚拟环境**

```bash
python -m venv .venv
```

3. **激活虚拟环境**

**Windows:**
```bash
venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

4. **安装依赖**

```bash
pip install -r requirements.txt
```

### 启动服务器

**Windows:**
```bash
start.bat
```

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

**或者直接运行:**
```bash
python src/mcp_server.py
```

### 配置iFlow CLI

在iFlow CLI配置文件中添加以下内容：

```json
{
  "mcpServers": {
    "kali-mcp": {
      "command": "python",
      "args": ["f:\\work\\trea\\kali-tool\\src\\mcp_server.py"]
    }
  }
}
```

## 使用示例

### 示例1：列出Kali工具

```json
{
  "method": "tools/call",
  "params": {
    "name": "run_security_tool",
    "arguments": {
      "tool": "nmap",
      "target": "192.168.1.1"
    }
  }
}
```

### 示例2：启动Burp Suite

```json
{
  "method": "tools/call",
  "params": {
    "name": "burp_start",
    "arguments": {
      "version": "professional",
      "headless": true,
      "port": 9876
    }
  }
}
```

### 示例3：运行漏洞扫描

```json
{
  "method": "tools/call",
  "params": {
    "name": "burp_scan",
    "arguments": {
      "target": "https://example.com",
      "scan_type": "passive"
    }
  }
}
```

### 示例4：发送HTTP请求

```json
{
  "method": "tools/call",
  "params": {
    "name": "send_http1_request",
    "arguments": {
      "method": "POST",
      "url": "https://example.com/api",
      "headers": {
        "Content-Type": "application/json"
      },
      "body": "{\"key\": \"value\"}"
    }
  }
}
```

### 示例5：URL编码

```json
{
  "method": "tools/call",
  "params": {
    "name": "url_encode",
    "arguments": {
      "content": "test string with spaces"
    }
  }
}
```

### 示例6：Base64编码

```json
{
  "method": "tools/call",
  "params": {
    "name": "base64_encode",
    "arguments": {
      "content": "hello world"
    }
  }
}
```

### 示例7：生成随机字符串

```json
{
  "method": "tools/call",
  "params": {
    "name": "generate_random_string",
    "arguments": {
      "length": 32,
      "characterSet": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    }
  }
}
```

### 示例8：创建Repeater标签页

```json
{
  "method": "tools/call",
  "params": {
    "name": "create_repeater_tab",
    "arguments": {
      "request": "GET / HTTP/1.1\r\nHost: example.com\r\n\r\n",
      "tabName": "Test Request"
    }
  }
}
```

### 示例9：发送到Intruder

```json
{
  "method": "tools/call",
  "params": {
    "name": "send_to_intruder",
    "arguments": {
      "request": "POST /login HTTP/1.1\r\nHost: example.com\r\n\r\nusername=test",
      "tabName": "Login Test"
    }
  }
}
```

### 示例10：设置代理拦截

```json
{
  "method": "tools/call",
  "params": {
    "name": "set_proxy_intercept_state",
    "arguments": {
      "intercepting": true
    }
  }
}
```

### 示例11：执行安全工具

```json
{
  "method": "tools/call",
  "params": {
    "name": "run_security_tool",
    "arguments": {
      "tool": "nmap",
      "target": "192.168.1.1",
      "arguments": ["-sV", "-p", "80,443"]
    }
  }
}
```

### 示例12：获取服务器配置

```json
{
  "method": "config/get",
  "params": {}
}
```

### 示例13：使用提示词

```json
{
  "method": "prompts/list",
  "params": {}
}
```

## 服务器架构

### 配置结构

```python
server_config = {
    'burp': {
        'enabled': True,
        'port': 9876,
        'host': 'localhost',
        'allowConfigEdit': False,
    },
    'sse': {
        'enabled': True,
        'port': 9877,
        'host': 'localhost',
    },
    'websocket': {
        'enabled': False,
        'port': 9878,
        'host': 'localhost',
    },
}
```

### 端口分配

- **9876** - Burp Suite MCP服务器
- **9877** - SSE服务器
- **9878** - WebSocket服务器
- **9879** - HTTP服务器

## 错误处理

所有工具调用都包含完整的错误处理：

- 命令执行失败时返回详细错误信息
- JSON解析错误会记录到stderr
- 网络连接错误会自动处理
- 所有错误都包含`isError: true`标志

## 日志

服务器使用stderr输出日志信息：

- 服务器启动信息
- 工具执行结果
- 错误和警告
- 连接状态变化

## 开发

### 依赖项

- `aiohttp>=3.9.0` - HTTP服务器和客户端
- `websockets>=12.0` - WebSocket服务器

### 文件结构

```
kali-tool/
├── src/
│   └── mcp_server.py      # MCP服务器主文件
├── requirements.txt       # Python依赖
├── start.bat             # Windows启动脚本
├── start.sh              # Linux/Mac启动脚本
└── README.md             # 本文档
```

## 与PortSwigger官方扩展对比

| 功能 | 官方扩展 | Python实现 |
|------|-----------|-----------|
| HTTP/1.1请求 | ✅ | ✅ |
| HTTP/2请求 | ✅ | ✅ |
| Repeater集成 | ✅ | ✅ |
| Intruder集成 | ✅ | ✅ |
| URL编码/解码 | ✅ | ✅ |
| Base64编码/解码 | ✅ | ✅ |
| 随机字符串生成 | ✅ | ✅ |
| 代理拦截控制 | ✅ | ✅ |
| 任务引擎控制 | ✅ | ✅ |
| 配置管理 | ✅ | ✅ |
| 项目配置导出 | ✅ | ✅ |
| 用户配置导出 | ✅ | ✅ |
| 扫描器问题 | ✅ | ✅ |
| 代理HTTP历史 | ✅ | ✅ |
| 代理WebSocket历史 | ✅ | ✅ |
| 活动编辑器内容 | ✅ | ✅ |
| Stdio传输 | ✅ | ✅ |
| SSE传输 | ✅ | ✅ |
| WebSocket传输 | ✅ | ✅ |
| HTTP传输 | ✅ | ✅ |

## 新增功能（v2.1.0）

相比v1.0.4，v2.1.0新增了以下功能：

1. **HTTP请求工具** - 支持HTTP/1.1和HTTP/2请求发送
2. **编码/解码工具** - URL和Base64编码/解码
3. **随机字符串生成** - 可自定义长度和字符集
4. **Burp Suite深度集成** - Repeater、Intruder、代理拦截、任务引擎控制
5. **WebSocket支持** - 新增WebSocket服务器支持
6. **增强的HTTP服务器** - 返回更多服务器信息
7. **配置和历史记录** - 项目/用户配置管理、扫描器问题、代理历史记录、活动编辑器内容

## 测试

运行测试脚本验证所有功能：

```bash
python test_server.py
```

测试覆盖：

- ✓ 服务器初始化
- ✓ 17个工具注册
- ✓ 1个提示词注册
- ✓ 所有处理器功能
- ✓ 编码/解码工具
- ✓ 随机字符串生成
- ✓ 配置管理

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！

## 联系方式

- GitHub: https://github.com/Wyl-cmd/AI-hacker-mcp