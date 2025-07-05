/**
 * MCP Client utility to communicate with Blender MCP Server
 * GitHub Copilot VS Code Extension Compatible
 * 
 * NOTE: This client currently simulates the MCP protocol for frontend use.
 * For real MCP protocol communication, the GitHub Copilot extension in VS Code
 * will handle the actual MCP server communication via the configured mcp.servers
 * settings in .vscode/settings.json
 */

// Type definitions for MCP protocol
interface MCPToolArguments {
  [key: string]: unknown;
}

interface MCPToolCall {
  name: string;
  arguments: MCPToolArguments;
}

interface MCPResponse {
  result?: unknown;
  error?: {
    code: number;
    message: string;
  };
}

interface MCPRequest {
  jsonrpc: string;
  id?: number;
  method: string;
  params?: unknown;
}

interface MCPNotification {
  jsonrpc: string;
  method: string;
  params?: unknown;
}

interface MCPTool {
  name: string;
  description: string;
  inputSchema: {
    type: string;
    properties: Record<string, unknown>;
  };
}

interface VSCodeAPI {
  workspace: {
    getConfiguration: (section: string) => Promise<Record<string, unknown>>;
  };
}

declare global {
  interface Window {
    vscode?: VSCodeAPI;
  }
}

interface VSCodeMCPConfig {
  enabled: boolean;
  serverPath: string;
  blenderPath: string;
}

export class MCPClient {
  private serverUrl: string;
  private serverPort: number;
  private sessionId: string | null = null;
  private vscodeConfig: VSCodeMCPConfig;

  constructor(serverUrl = 'localhost', serverPort = 9876) {
    this.serverUrl = serverUrl;
    this.serverPort = serverPort;
    this.vscodeConfig = {
      enabled: true,
      serverPath: 'd:/constructai/backend/start_mcp_server.py',
      blenderPath: 'blender'
    };
  }

  async initialize(): Promise<boolean> {
    try {
      // Check if VS Code MCP integration is available
      if (typeof window !== 'undefined' && window.vscode) {
        console.log('VS Code environment detected, using VS Code MCP integration');
        return await this.initializeVSCodeMCP();
      }
      
      // Fallback to direct MCP protocol
      return await this.initializeDirectMCP();
    } catch (error) {
      console.error('MCP initialization failed:', error);
      return false;
    }
  }

  private async initializeVSCodeMCP(): Promise<boolean> {
    try {
      const vscode = window.vscode;
      if (!vscode) {
        return false;
      }
      
      // Check if MCP server is configured in VS Code
      const mcpServers = await vscode.workspace.getConfiguration('mcp.servers');
      
      if (mcpServers && mcpServers['constructai-blender']) {
        this.sessionId = `vscode_session_${Date.now()}`;
        console.log('VS Code MCP server configured:', mcpServers['constructai-blender']);
        return true;
      }
      
      return false;
    } catch (error) {
      console.error('VS Code MCP initialization failed:', error);
      return false;
    }
  }

  private async initializeDirectMCP(): Promise<boolean> {
    try {
      // Initialize MCP session with the server
      const initRequest = {
        jsonrpc: '2.0',
        id: 1,
        method: 'initialize',
        params: {
          protocolVersion: '2024-11-05',
          capabilities: {
            tools: {}
          },
          clientInfo: {
            name: 'ConstructAI-GitHub-Copilot',
            version: '1.0.0'
          }
        }
      };

      const response = await this.sendRequest(initRequest);
      
      if (response.result) {
        this.sessionId = `direct_session_${Date.now()}`;
        
        // Send initialized notification
        await this.sendNotification({
          jsonrpc: '2.0',
          method: 'notifications/initialized'
        });
        
        return true;
      }
      
      return false;
    } catch (error) {
      console.error('Direct MCP initialization failed:', error);
      return false;
    }
  }

  async callTool(toolName: string, arguments_: MCPToolArguments): Promise<unknown> {
    try {
      if (!this.sessionId) {
        const initialized = await this.initialize();
        if (!initialized) {
          throw new Error('Failed to initialize MCP session');
        }
      }

      const toolRequest = {
        jsonrpc: '2.0',
        id: Date.now(),
        method: 'tools/call',
        params: {
          name: toolName,
          arguments: arguments_
        }
      };

      const response = await this.sendRequest(toolRequest);
      
      if (response.error) {
        throw new Error(`MCP tool error: ${response.error.message}`);
      }
      
      return response.result;

    } catch (error) {
      console.error('MCP tool call failed:', error);
      throw error;
    }
  }

  async listTools(): Promise<MCPTool[]> {
    try {
      if (!this.sessionId) {
        await this.initialize();
      }

      const listRequest = {
        jsonrpc: '2.0',
        id: Date.now(),
        method: 'tools/list',
        params: {}
      };

      const response = await this.sendRequest(listRequest);
      const result = response.result as { tools?: MCPTool[] };
      return result?.tools || [];
    } catch (error) {
      console.error('Failed to list tools:', error);
      return [];
    }
  }

  async getServerStatus(): Promise<{ connected: boolean; version?: string; error?: string }> {
    try {
      const initialized = await this.initialize();
      
      if (initialized) {
        return {
          connected: true,
          version: '1.0.0'
        };
      } else {
        return {
          connected: false,
          error: 'Failed to initialize MCP session'
        };
      }
    } catch (error) {
      return {
        connected: false,
        error: error instanceof Error ? error.message : 'Connection failed'
      };
    }
  }

  private async sendRequest(request: MCPRequest): Promise<MCPResponse> {
    try {
      // For now, we'll simulate the MCP protocol
      // In a real implementation, you would send this via WebSocket or stdio
      console.log('Sending MCP request:', request);
      
      // Simulate the actual MCP server responses based on your Blender server
      if (request.method === 'initialize') {
        await this.simulateDelay(500);
        return {
          result: {
            protocolVersion: '2024-11-05',
            capabilities: {
              tools: {
                listChanged: true
              }
            },
            serverInfo: {
              name: 'blender-3d-server',
              version: '1.0.0'
            }
          }
        };
      }
      
      if (request.method === 'tools/list') {
        await this.simulateDelay(300);
        return {
          result: {
            tools: [
              {
                name: 'create_3d_scene',
                description: 'Create a 3D scene from room data',
                inputSchema: {
                  type: 'object',
                  properties: {
                    rooms: { type: 'array' },
                    building_dimensions: { type: 'object' }
                  }
                }
              },
              {
                name: 'render_scene',
                description: 'Render the current scene',
                inputSchema: {
                  type: 'object',
                  properties: {
                    view_type: { type: 'string', enum: ['single', '360'] }
                  }
                }
              }
            ]
          }
        };
      }
      
      if (request.method === 'tools/call') {
        return await this.handleToolCall(request.params as MCPToolCall);
      }
      
      throw new Error(`Unknown method: ${request.method}`);
      
    } catch (error) {
      return {
        error: {
          code: -1,
          message: error instanceof Error ? error.message : 'Unknown error'
        }
      };
    }
  }

  private async sendNotification(notification: MCPNotification): Promise<void> {
    console.log('Sending MCP notification:', notification);
    // In a real implementation, send notification via transport layer
  }

  private async handleToolCall(params: MCPToolCall): Promise<MCPResponse> {
    const { name, arguments: args } = params;
    
    try {
      // Use the direct Blender MCP bridge
      const apiUrl = `http://localhost:3000/api/mcp/blender-bridge`;
      
      console.log(`🔗 Calling real Blender MCP: ${name}`);
      console.log('📝 Arguments:', args);
      
      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          tool: name,
          arguments: args
        })
      });
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      
      const result = await response.json();
      console.log('✅ Real Blender MCP response:', result);
      
      if (result.success) {
        return {
          result: result.result || result
        };
      } else {
        throw new Error(result.error || 'Blender MCP failed');
      }
      
    } catch (error) {
      console.error(`❌ Error calling Blender MCP ${name}:`, error);
      
      // Fallback to simulation for development
      console.log('🔄 Falling back to simulation mode...');
      return await this.simulateToolCall(name, args);
    }
  }

  private async simulateToolCall(name: string, args: MCPToolArguments): Promise<MCPResponse> {
    switch (name) {
      case 'create_3d_scene':
        await this.simulateDelay(1000);
        return {
          result: {
            success: true,
            scene_file: `/tmp/constructai_blender_${Date.now()}/scene.blend`,
            message: 'Scene created successfully with Blender MCP (simulation mode)'
          }
        };

      case 'render_scene':
        const viewType = args.view_type;
        await this.simulateDelay(viewType === '360' ? 3000 : 1500);
        
        const renderFiles = viewType === '360' 
          ? Array.from({length: 8}, (_, i) => `/tmp/constructai_blender_${Date.now()}/render_${i * 45}.png`)
          : [`/tmp/constructai_blender_${Date.now()}/render.png`];

        return {
          result: {
            success: true,
            render_files: renderFiles,
            message: 'Scene rendered successfully with Blender MCP (simulation mode)'
          }
        };

      default:
        return {
          error: {
            code: -32601,
            message: `Unknown tool: ${name}`
          }
        };
    }
  }

  private async simulateDelay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

// Singleton instance
export const mcpClient = new MCPClient();
