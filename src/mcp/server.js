#!/usr/bin/env node
/**
 * SentinelForge Model Context Protocol (MCP) Server
 * Stdio JSON-RPC 2.0 server enabling external AI agents to access SentinelForge tools.
 */

import readline from 'readline';
import { fileURLToPath } from 'url';
import { MCP_TOOLS, handleToolCall } from './tools.js';

const SERVER_INFO = {
    name: 'sentinelforge-mcp-server',
    version: '1.0.0',
    capabilities: {
        tools: {}
    }
};

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
    terminal: false
});

function sendResponse(id, result, error = null) {
    const payload = {
        jsonrpc: '2.0',
        id
    };

    if (error) {
        payload.error = error;
    } else {
        payload.result = result;
    }

    process.stdout.write(JSON.stringify(payload) + '\n');
}

rl.on('line', async (line) => {
    const trimmed = line.trim();
    if (!trimmed) return;

    try {
        const req = JSON.parse(trimmed);
        const { id, method, params } = req;

        switch (method) {
            case 'initialize':
                sendResponse(id, {
                    protocolVersion: '2024-11-05',
                    serverInfo: SERVER_INFO,
                    capabilities: {
                        tools: {
                            listChanged: false
                        }
                    }
                });
                break;

            case 'notifications/initialized':
                // Client confirmed initialization
                break;

            case 'tools/list':
                sendResponse(id, {
                    tools: MCP_TOOLS
                });
                break;

            case 'tools/call':
                try {
                    const toolResult = await handleToolCall(params?.name, params?.arguments);
                    sendResponse(id, toolResult);
                } catch (toolErr) {
                    sendResponse(id, null, {
                        code: -32603,
                        message: toolErr.message || 'Tool execution failure'
                    });
                }
                break;

            case 'ping':
                sendResponse(id, {});
                break;

            default:
                sendResponse(id, null, {
                    code: -32601,
                    message: `Method not found: ${method}`
                });
                break;
        }
    } catch (parseErr) {
        sendResponse(null, null, {
            code: -32700,
            message: 'Parse error: invalid JSON payload'
        });
    }
});

const isMain = process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1];
if (isMain) {
    process.stderr.write('SentinelForge MCP Server active on stdio\n');
}
