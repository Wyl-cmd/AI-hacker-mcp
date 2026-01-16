#!/usr/bin/env node

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';

const server = new Server(
  {
    name: 'kali-mcp-server',
    version: '1.0.0',
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: 'list_kali_tools',
        description: 'List available Kali Linux security and penetration testing tools installed on the system',
        inputSchema: {
          type: 'object',
          properties: {
            category: {
              type: 'string',
              description: 'Filter tools by category (e.g., information-gathering, vulnerability-analysis, web-applications, password-attacks, exploitation, etc.)',
            },
          },
        },
      },
    ],
  };
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    switch (name) {
      case 'list_kali_tools': {
        const { exec } = await import('child_process');
        const { category } = args || {};
        
        return new Promise((resolve, reject) => {
          let command = 'dpkg -l | grep -E "kali|metasploit|nmap|burpsuite|sqlmap|nikto|hydra|john|aircrack|wireshark|tcpdump|netcat|socat|gobuster|dirb|ffuf|wpscan|nikto|whatweb|enum4linux|smbclient|nbtscan|rpcclient|showmount|snmpwalk|onesixtyone|ike-scan|sslscan|testssl|nuclei|subfinder|amass|httpx|ffuf|gobuster|dirsearch|wfuzz|feroxbuster|rustscan|masscan|unicornscan|zmap|arp-scan|netdiscover|fping|hping3|scapy|tcping|mtr|traceroute|dig|nslookup|host|whois|curl|wget|git|svn|hg" | grep -E "^ii" | awk \'{print $2}\'';
          
          if (category) {
            command = `dpkg -l | grep -E "kali|${category}" | grep -E "^ii" | awk '{print $2}'`;
          }
          
          exec(command, { shell: '/bin/bash' }, (error, stdout, stderr) => {
            if (error) {
              resolve({
                content: [
                  {
                    type: 'text',
                    text: `Error listing Kali tools: ${error.message}\nStderr: ${stderr}`,
                  },
                ],
                isError: true,
              });
            } else {
              const tools = stdout.trim().split('\n').filter(tool => tool.length > 0);
              const result = {
                total: tools.length,
                tools: tools,
                message: `Found ${tools.length} Kali security tools installed on this system. You can use these tools through terminal via iflow-cli.`
              };
              
              resolve({
                content: [
                  {
                    type: 'text',
                    text: JSON.stringify(result, null, 2),
                  },
                ],
              });
            }
          });
        });
      }

      default:
        throw new Error(`Unknown tool: ${name}`);
    }
  } catch (error) {
    return {
      content: [
        {
          type: 'text',
          text: `Error: ${error.message}`,
        },
      ],
      isError: true,
    };
  }
});

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('Kali MCP Server running on stdio');
}

main().catch((error) => {
  console.error('Server error:', error);
  process.exit(1);
});
