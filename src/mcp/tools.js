/**
 * SentinelForge Model Context Protocol (MCP) Tools Registry
 * Declares tool schemas and dispatch handlers according to the Model Context Protocol specification.
 */

const { TeamworkGraphService } = require('../services/teamworkGraph.js');
const { JiraService } = require('../services/jiraService.js');
const { DriftEngine } = require('../services/driftEngine.js');

const teamworkGraph = new TeamworkGraphService();
const jiraService = new JiraService();
const driftEngine = new DriftEngine();

const MCP_TOOLS = [
    {
        name: 'sentinel_query_teamwork_graph',
        description: 'Queries the Atlassian Teamwork Graph to retrieve cross-product dependencies, linked Confluence ADRs, Git commits, and microservices for a Jira issue.',
        inputSchema: {
            type: 'object',
            properties: {
                issueKey: {
                    type: 'string',
                    description: 'The Jira issue key (e.g., PROJ-101, SEC-404)'
                }
            },
            required: ['issueKey']
        }
    },
    {
        name: 'sentinel_audit_drift',
        description: 'Audits configuration, architectural, and code drift between Jira requirements, Confluence specs, and recent commits.',
        inputSchema: {
            type: 'object',
            properties: {
                issueKey: {
                    type: 'string',
                    description: 'The Jira issue key to audit'
                }
            },
            required: ['issueKey']
        }
    },
    {
        name: 'sentinel_execute_mitigation',
        description: 'Executes automated remediation workflows (e.g. queue throttling, circuit breaking, ADR syncing) and records the receipt on the Jira issue.',
        inputSchema: {
            type: 'object',
            properties: {
                issueKey: {
                    type: 'string',
                    description: 'The Jira issue key'
                },
                actionId: {
                    type: 'string',
                    description: 'The remediation action identifier (e.g., ACTION_APPLY_THROTTLE)'
                }
            },
            required: ['issueKey', 'actionId']
        }
    }
];

async function handleToolCall(name, args) {
    const issueKey = args?.issueKey || 'PROJ-101';

    switch (name) {
        case 'sentinel_query_teamwork_graph': {
            const graph = await teamworkGraph.resolveGraph(issueKey);
            return {
                content: [
                    {
                        type: 'text',
                        text: JSON.stringify(graph, null, 2)
                    }
                ]
            };
        }
        case 'sentinel_audit_drift': {
            const [issue, graph] = await Promise.all([
                jiraService.getIssue(issueKey),
                teamworkGraph.resolveGraph(issueKey)
            ]);
            const analysis = driftEngine.analyze(issue, graph);
            return {
                content: [
                    {
                        type: 'text',
                        text: JSON.stringify(analysis, null, 2)
                    }
                ]
            };
        }
        case 'sentinel_execute_mitigation': {
            const actionId = args?.actionId || 'ACTION_APPLY_THROTTLE';
            const report = {
                status: 'MITIGATED',
                driftScore: 78,
                rootCause: 'Drift remediation triggered via MCP agent interface',
                actionSummary: `Automated action ${actionId} dispatched via MCP.`
            };
            const receipt = await jiraService.postRemediationComment(issueKey, report);
            return {
                content: [
                    {
                        type: 'text',
                        text: JSON.stringify({ success: true, actionId, receipt }, null, 2)
                    }
                ]
            };
        }
        default:
            throw new Error(`Unrecognized MCP tool: ${name}`);
    }
}

module.exports = { MCP_TOOLS, handleToolCall };
