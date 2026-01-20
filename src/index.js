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
    version: '1.0.3',
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
      {
        name: 'burp_start',
        description: 'Start Burp Suite with specified options',
        inputSchema: {
          type: 'object',
          properties: {
            version: {
              type: 'string',
              description: 'Burp Suite version to start (professional or community)',
              enum: ['professional', 'community'],
              default: 'professional',
            },
            config: {
              type: 'string',
              description: 'Path to Burp Suite configuration file',
            },
            headless: {
              type: 'boolean',
              description: 'Start Burp Suite in headless mode',
              default: false,
            },
          },
        },
      },
      {
        name: 'burp_scan',
        description: 'Run a vulnerability scan with Burp Suite',
        inputSchema: {
          type: 'object',
          properties: {
            target: {
              type: 'string',
              description: 'Target URL to scan',
              required: true,
            },
            config: {
              type: 'string',
              description: 'Path to Burp Suite scan configuration file',
            },
            output: {
              type: 'string',
              description: 'Path to save scan results',
            },
            scope: {
              type: 'array',
              items: {
                type: 'string',
              },
              description: 'URLs to include in the scan scope',
            },
          },
        },
      },
      {
        name: 'burp_health_check',
        description: 'Check if Burp Suite is installed and accessible',
        inputSchema: {
          type: 'object',
          properties: {},
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
      case 'burp_health_check': {
        const { exec } = await import('child_process');
        
        return new Promise((resolve, reject) => {
          const command = 'which burpsuite';
          
          exec(command, { shell: '/bin/bash' }, (error, stdout, stderr) => {
            if (error) {
              resolve({
                content: [
                  {
                    type: 'text',
                    text: `Burp Suite is not installed or not in PATH. Error: ${error.message}`,
                  },
                ],
                isError: true,
              });
            } else {
              const burpPath = stdout.trim();
              resolve({
                content: [
                  {
                    type: 'text',
                    text: `Burp Suite is installed at: ${burpPath}`,
                  },
                ],
              });
            }
          });
        });
      }
      case 'burp_start': {
        const { exec } = await import('child_process');
        const { version = 'professional', config, headless = false } = args || {};
        
        return new Promise((resolve, reject) => {
          let command = 'burpsuite';
          
          if (version === 'community') {
            command = 'burpsuite-community';
          }
          
          if (config) {
            command += ` --config-file=${config}`;
          }
          
          if (headless) {
            command += ' --headless';
          }
          
          exec(command, { shell: '/bin/bash', detached: true, stdio: 'ignore' }, (error, stdout, stderr) => {
            if (error) {
              resolve({
                content: [
                  {
                    type: 'text',
                    text: `Failed to start Burp Suite: ${error.message}\nCommand: ${command}\nStderr: ${stderr}`,
                  },
                ],
                isError: true,
              });
            } else {
              resolve({
                content: [
                  {
                    type: 'text',
                    text: `Burp Suite ${version} started successfully with command: ${command}`,
                  },
                ],
              });
            }
          });
        });
      }
      case 'burp_scan': {
        const { exec } = await import('child_process');
        const { target, config, output, scope } = args || {};
        
        return new Promise((resolve, reject) => {
          if (!target) {
            resolve({
              content: [
                {
                  type: 'text',
                  text: 'Error: Target URL is required',
                },
              ],
              isError: true,
            });
            return;
          }
          
          let command = `burpsuite --headless --target=${target}`;
          
          if (config) {
            command += ` --config-file=${config}`;
          }
          
          if (output) {
            command += ` --report-output=${output}`;
          }
          
          if (scope && scope.length > 0) {
            const scopeStr = scope.join(',');
            command += ` --scope-include=${scopeStr}`;
          }
          
          exec(command, { shell: '/bin/bash' }, (error, stdout, stderr) => {
            if (error) {
              resolve({
                content: [
                  {
                    type: 'text',
                    text: `Burp Suite scan failed: ${error.message}\nCommand: ${command}\nStderr: ${stderr}`,
                  },
                ],
                isError: true,
              });
            } else {
              resolve({
                content: [
                  {
                    type: 'text',
                    text: `Burp Suite scan completed successfully. Output:\n${stdout}`,
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
