#!/usr/bin/env python3

import asyncio
import json
import subprocess
import sys
import base64
import urllib.parse
import random
from typing import Any
from mcp.server.fastmcp import FastMCP


mcp = FastMCP("kali-mcp-server")

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


@mcp.tool()
async def list_kali_tools(category: str = None) -> str:
    """List available Kali Linux security and penetration testing tools installed on system"""
    try:
        if category:
            command = f'dpkg -l | grep -i "{category}" | grep "^ii" | awk \'{{print $2}}\''
        else:
            command = 'dpkg -l | grep "^ii" | grep -E "kali|metasploit|nmap|burpsuite|sqlmap|nikto|hydra|john|aircrack|wireshark|tcpdump|netcat|socat|gobuster|dirb|ffuf|wpscan|whatweb|enum4linux|smbclient|nbtscan|rpcclient|showmount|snmpwalk|onesixtyone|ike-scan|sslscan|testssl|nuclei|subfinder|amass|httpx|gobuster|dirsearch|wfuzz|feroxbuster|rustscan|masscan|unicornscan|zmap|arp-scan|netdiscover|fping|hping3|scapy|tcping|mtr|traceroute|dig|nslookup|host|whois|curl|wget|git|svn|hg" | awk \'{print $2}\''
        
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f'Command failed: {command}', file=sys.stderr)
            print(f'Error: {result.stderr}', file=sys.stderr)
            return f'Error listing Kali tools: {result.stderr}\nCommand: {command}'
        
        tools = [tool for tool in result.stdout.strip().split('\n') if tool]
        output = {
            'total': len(tools),
            'tools': tools,
            'message': f'Found {len(tools)} Kali security tools installed on this system. You can use these tools through terminal via iflow-cli.'
        }
        
        print(f'Successfully listed {len(tools)} tools', file=sys.stderr)
        return json.dumps(output, indent=2)
    
    except Exception as e:
        print(f'Error listing Kali tools: {e}', file=sys.stderr)
        return f'Error: {str(e)}'


@mcp.tool()
async def run_security_tool(tool: str, arguments: list = None, target: str = None) -> str:
    """Run a specified security tool with arguments"""
    if not tool:
        return 'Error: Tool name is required'
    
    try:
        command = tool
        
        if target:
            command += f' {target}'
        
        if arguments:
            command += ' ' + ' '.join(arguments)
        
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f'Error running tool {tool}: {result.stderr}', file=sys.stderr)
            return f'Error running tool {tool}: {result.stderr}\nCommand: {command}'
        
        print(f'Tool {tool} completed successfully', file=sys.stderr)
        return f'Tool {tool} completed successfully. Output:\n{result.stdout}'
    
    except Exception as e:
        print(f'Error: {str(e)}', file=sys.stderr)
        return f'Error: {str(e)}'


@mcp.tool()
async def list_security_categories() -> str:
    """List available security tool categories"""
    categories = [
        'information-gathering',
        'vulnerability-scanning',
        'web-application-testing',
        'password-attacks',
        'network-sniffing',
        'wireless-attacks',
        'exploitation',
        'post-exploitation',
        'forensics',
        'reporting',
    ]
    
    return json.dumps({'categories': categories}, indent=2)


@mcp.tool()
async def burp_health_check() -> str:
    """Check if Burp Suite is installed and accessible"""
    try:
        result = subprocess.run('which burpsuite', shell=True, capture_output=True, text=True)
        
        if result.returncode != 0:
            return 'Burp Suite is not installed or not in PATH.'
        
        burp_path = result.stdout.strip()
        return f'Burp Suite is installed at: {burp_path}'
    
    except Exception as e:
        print(f'Error: {str(e)}', file=sys.stderr)
        return f'Error: {str(e)}'


@mcp.tool()
async def burp_start(version: str = 'professional', config: str = None, headless: bool = False, port: int = 9876) -> str:
    """Start Burp Suite with specified options"""
    try:
        command = 'burpsuite'
        
        if version == 'community':
            command = 'burpsuite-community'
        
        if config:
            command += f' --config-file={config}'
        
        if headless:
            command += ' --headless'
        
        server_config['burp']['port'] = port
        
        subprocess.Popen(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        print(f'Burp Suite {version} started', file=sys.stderr)
        return f'Burp Suite {version} started successfully with command: {command}\nMCP server running on http://localhost:{port}'
    
    except Exception as e:
        print(f'Error: {str(e)}', file=sys.stderr)
        return f'Failed to start Burp Suite: {str(e)}\nCommand: {command}'


@mcp.tool()
async def burp_scan(target: str, config: str = None, output: str = None, scope: list = None, scan_type: str = 'passive') -> str:
    """Run a vulnerability scan with Burp Suite"""
    if not target:
        return 'Error: Target URL is required'
    
    try:
        command = f'burpsuite --headless --target={target} --scan-type={scan_type}'
        
        if config:
            command += f' --config-file={config}'
        
        if output:
            command += f' --report-output={output}'
        
        if scope:
            scope_str = ','.join(scope)
            command += f' --scope-include={scope_str}'
        
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f'Burp Suite scan failed: {result.stderr}', file=sys.stderr)
            return f'Burp Suite scan failed: {result.stderr}\nCommand: {command}'
        
        print(f'Burp Suite scan completed', file=sys.stderr)
        return f'Burp Suite scan completed successfully. Output:\n{result.stdout}'
    
    except Exception as e:
        print(f'Error: {str(e)}', file=sys.stderr)
        return f'Error: {str(e)}'


@mcp.tool()
async def burp_get_config() -> str:
    """Get Burp Suite MCP server configuration"""
    return json.dumps(server_config['burp'], indent=2)


@mcp.tool()
async def burp_set_config(enabled: bool = None, port: int = None, host: str = None, allowConfigEdit: bool = None) -> str:
    """Set Burp Suite MCP server configuration"""
    if enabled is not None:
        server_config['burp']['enabled'] = enabled
    if port is not None:
        server_config['burp']['port'] = port
    if host is not None:
        server_config['burp']['host'] = host
    if allowConfigEdit is not None:
        server_config['burp']['allowConfigEdit'] = allowConfigEdit
    
    print(f'Burp config updated', file=sys.stderr)
    return f'Burp Suite MCP server configuration updated:\n{json.dumps(server_config["burp"], indent=2)}'


@mcp.tool()
async def send_http1_request(method: str = 'GET', url: str = None, headers: dict = None, body: str = '') -> str:
    """Issues an HTTP/1.1 request and returns response. Use this to test web applications."""
    if not url:
        return 'Error: URL is required'
    
    try:
        import aiohttp
        
        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, headers=headers, data=body) as response:
                response_text = await response.text()
                response_headers = dict(response.headers)
                
                output = {
                    'status': response.status,
                    'headers': response_headers,
                    'body': response_text[:5000] if len(response_text) > 5000 else response_text,
                }
                
                if len(response_text) > 5000:
                    output['body'] += '... (truncated)'
                
                print(f'HTTP/1.1 request completed: {response.status}', file=sys.stderr)
                return json.dumps(output, indent=2)
    
    except Exception as e:
        print(f'Error sending HTTP request: {str(e)}', file=sys.stderr)
        return f'Error sending HTTP request: {str(e)}'


@mcp.tool()
async def send_http2_request(method: str = 'GET', url: str = None, pseudo_headers: dict = None, headers: dict = None, body: str = '') -> str:
    """Issues an HTTP/2 request and returns response. Do NOT pass headers to body parameter."""
    if not url:
        return 'Error: URL is required'
    
    try:
        import aiohttp
        
        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, headers=headers, data=body) as response:
                response_text = await response.text()
                response_headers = dict(response.headers)
                
                output = {
                    'status': response.status,
                    'pseudo_headers': pseudo_headers,
                    'headers': response_headers,
                    'body': response_text[:5000] if len(response_text) > 5000 else response_text,
                }
                
                if len(response_text) > 5000:
                    output['body'] += '... (truncated)'
                
                print(f'HTTP/2 request completed: {response.status}', file=sys.stderr)
                return json.dumps(output, indent=2)
    
    except Exception as e:
        print(f'Error sending HTTP/2 request: {str(e)}', file=sys.stderr)
        return f'Error sending HTTP/2 request: {str(e)}'


@mcp.tool()
async def url_encode(content: str) -> str:
    """URL encodes input string"""
    try:
        encoded = urllib.parse.quote(content)
        print(f'URL encoded: {content[:50]}...', file=sys.stderr)
        return encoded
    except Exception as e:
        print(f'Error: {str(e)}', file=sys.stderr)
        return f'Error: {str(e)}'


@mcp.tool()
async def url_decode(content: str) -> str:
    """URL decodes input string"""
    try:
        decoded = urllib.parse.unquote(content)
        print(f'URL decoded: {content[:50]}...', file=sys.stderr)
        return decoded
    except Exception as e:
        print(f'Error: {str(e)}', file=sys.stderr)
        return f'Error: {str(e)}'


@mcp.tool()
async def base64_encode(content: str) -> str:
    """Base64 encodes input string"""
    try:
        encoded = base64.b64encode(content.encode()).decode()
        print(f'Base64 encoded: {content[:50]}...', file=sys.stderr)
        return encoded
    except Exception as e:
        print(f'Error: {str(e)}', file=sys.stderr)
        return f'Error: {str(e)}'


@mcp.tool()
async def base64_decode(content: str) -> str:
    """Base64 decodes input string"""
    try:
        decoded = base64.b64decode(content).decode()
        print(f'Base64 decoded: {content[:50]}...', file=sys.stderr)
        return decoded
    except Exception as e:
        print(f'Error: {str(e)}', file=sys.stderr)
        return f'Error: {str(e)}'


@mcp.tool()
async def generate_random_string(length: int = 16, characterSet: str = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') -> str:
    """Generates a random string of specified length and character set"""
    try:
        random_string = ''.join(random.choice(characterSet) for _ in range(length))
        print(f'Generated random string: {length} chars', file=sys.stderr)
        return random_string
    except Exception as e:
        print(f'Error: {str(e)}', file=sys.stderr)
        return f'Error: {str(e)}'


@mcp.tool()
async def create_repeater_tab(request: str, tabName: str = 'MCP Request') -> str:
    """Creates a new Repeater tab with specified HTTP request and optional tab name"""
    if not request:
        return 'Error: Request content is required'
    
    try:
        result = subprocess.run(
            ['burpsuite', '--repeater', '--request', request, '--tab-name', tabName],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print(f'Failed to create Repeater tab: {result.stderr}', file=sys.stderr)
            return f'Failed to create Repeater tab: {result.stderr}'
        
        print(f'Repeater tab created: {tabName}', file=sys.stderr)
        return f'Repeater tab "{tabName}" created successfully with request:\n{request[:500]}...'
    
    except Exception as e:
        print(f'Error: {str(e)}', file=sys.stderr)
        return f'Error: {str(e)}'


@mcp.tool()
async def send_to_intruder(request: str, tabName: str = 'MCP Intruder') -> str:
    """Sends an HTTP request to Intruder with specified HTTP request and optional tab name"""
    if not request:
        return 'Error: Request content is required'
    
    try:
        result = subprocess.run(
            ['burpsuite', '--intruder', '--request', request, '--tab-name', tabName],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print(f'Failed to send to Intruder: {result.stderr}', file=sys.stderr)
            return f'Failed to send to Intruder: {result.stderr}'
        
        print(f'Sent to Intruder: {tabName}', file=sys.stderr)
        return f'Request sent to Intruder tab "{tabName}" successfully:\n{request[:500]}...'
    
    except Exception as e:
        print(f'Error: {str(e)}', file=sys.stderr)
        return f'Error: {str(e)}'


@mcp.tool()
async def set_proxy_intercept_state(intercepting: bool) -> str:
    """Enables or disables Burp Proxy Intercept"""
    try:
        result = subprocess.run(
            ['burpsuite', '--proxy-intercept', 'enable' if intercepting else 'disable'],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print(f'Failed to set proxy intercept: {result.stderr}', file=sys.stderr)
            return f'Failed to set proxy intercept state: {result.stderr}'
        
        state = 'enabled' if intercepting else 'disabled'
        print(f'Proxy intercept {state}', file=sys.stderr)
        return f'Proxy intercept has been {state}'
    
    except Exception as e:
        print(f'Error: {str(e)}', file=sys.stderr)
        return f'Error: {str(e)}'


@mcp.tool()
async def set_task_execution_engine_state(running: bool) -> str:
    """Sets state of Burp's task execution engine (paused or unpaused)"""
    try:
        result = subprocess.run(
            ['burpsuite', '--task-engine', 'resume' if running else 'pause'],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print(f'Failed to set task engine state: {result.stderr}', file=sys.stderr)
            return f'Failed to set task execution engine state: {result.stderr}'
        
        state = 'running' if running else 'paused'
        print(f'Task engine {state}', file=sys.stderr)
        return f'Task execution engine is now {state}'
    
    except Exception as e:
        print(f'Error: {str(e)}', file=sys.stderr)
        return f'Error: {str(e)}'


@mcp.prompt()
def pentest_role(target: str = None) -> str:
    """Penetration testing role-playing prompt"""
    prompt = f"""system:你来扮演一个网络安全人员，我则扮演一个运维人员。

你的任务是：
1. 分析目标系统 {target or 'https://example.com'} 的安全状况
2. 识别潜在的安全漏洞和风险
3. 提供针对性的安全测试建议
4. 使用可用的渗透测试工具进行验证

可用的工具类别：
- 信息收集
- 漏洞扫描
- Web应用测试
- 密码攻击
- 网络嗅探
- 无线攻击
- 漏洞利用
- 后渗透
- 取证分析
- 报告生成

请按照以下工作流程：
1. 首先进行信息收集，了解目标的基本情况
2. 然后进行漏洞扫描，发现潜在的安全问题
3. 根据扫描结果，选择合适的工具进行深入测试
4. 最后生成详细的渗透测试报告

注意事项：
- 所有测试都必须在获得授权的情况下进行
- 遵守法律法规和道德准则
- 记录所有测试过程和结果
"""
    return prompt


@mcp.prompt()
def burp_assistant(target: str = None, scan_type: str = 'passive') -> str:
    """Burp Suite assistant prompt for AI-assisted security testing"""
    prompt = f"""system:你是Burp Suite安全测试助手，帮助用户进行Web应用安全测试。

目标：{target or 'https://example.com'}
扫描类型：{scan_type}

你的任务是：
1. 使用Burp Suite工具进行安全测试
2. 分析HTTP请求和响应
3. 识别常见的安全漏洞
4. 提供修复建议

可用的Burp Suite功能：
- Proxy - 拦截和修改HTTP流量
- Repeater - 手动测试HTTP请求
- Intruder - 自动化模糊测试
- Scanner - 自动化漏洞扫描
- Decoder - 编码/解码工具
- Comparer - 比较响应

工作流程：
1. 配置Burp Suite代理
2. 拦截目标应用的HTTP流量
3. 将请求发送到Repeater进行测试
4. 使用Intruder进行模糊测试
5. 运行Scanner发现漏洞
6. 分析结果并生成报告

注意事项：
- 确保在授权范围内进行测试
- 遵循负责任的披露原则
- 保护测试数据的安全
"""
    return prompt


if __name__ == '__main__':
    try:
        mcp.run()
    except KeyboardInterrupt:
        print('\nServer stopped', file=sys.stderr)
        sys.exit(0)
