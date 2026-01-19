#!/usr/bin/env node

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  ListPromptsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';

const server = new Server(
  {
    name: 'kali-mcp-server',
    version: '1.0.1',
  },
  {
    capabilities: {
      tools: {},
      prompts: {},
    },
  }
);

server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: 'list_kali_tools',
        description: 'List available Kali Linux security and penetration testing tools installed on system',
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

server.setRequestHandler(ListPromptsRequestSchema, async () => {
  return {
    prompts: [
      {
        name: 'pentest-role',
        description: 'Penetration testing role-playing prompt',
        arguments: {
          type: 'object',
          properties: {
            target: {
              type: 'string',
              description: 'Target website for testing',
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
          let command;
          
          if (category) {
            command = `dpkg -l | grep -i "${category}" | grep "^ii" | awk '{print $2}'`;
          } else {
            command = 'dpkg -l | grep "^ii" | awk \'{print $2}\'';
          }
          
          exec(command, { shell: '/bin/bash' }, (error, stdout, stderr) => {
            if (error) {
              console.error(`Command failed: ${command}`);
              console.error(`Error: ${error.message}`);
              console.error(`Stderr: ${stderr}`);
              resolve({
                content: [
                  {
                    type: 'text',
                    text: `Error listing Kali tools: ${error.message}\nCommand: ${command}\nStderr: ${stderr}`,
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
              
              console.error(`Successfully listed ${tools.length} tools`);
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
    console.error(`Handler error: ${error.message}`);
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
  try {
    const transport = new StdioServerTransport();
    await server.connect(transport);
    console.error('Kali MCP Server running on stdio');
  } catch (error) {
    console.error('Failed to start server:', error);
    process.exit(1);
  }
}

main().catch((error) => {
  console.error('Server error:', error);
  process.exit(1);
});
