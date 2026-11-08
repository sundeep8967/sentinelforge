import test from 'node:test';
import assert from 'node:assert/strict';
import { TeamworkGraphService } from '../src/services/teamworkGraph.js';
import { JiraService } from '../src/services/jiraService.js';
import { DriftEngine } from '../src/services/driftEngine.js';
import { MCP_TOOLS, handleToolCall } from '../src/mcp/tools.js';

test('TeamworkGraphService resolves synthesized graph in offline mode', async () => {
    const service = new TeamworkGraphService();
    const graph = await service.resolveGraph('PROJ-101');

    assert.equal(graph.rootNode.key, 'PROJ-101');
    assert.equal(graph.status, 'SYNCHRONIZED');
    assert.ok(graph.connectedNodes.length >= 3);
    
    const types = graph.connectedNodes.map(n => n.type);
    assert.ok(types.includes('CONFLUENCE_PAGE'));
    assert.ok(types.includes('GIT_COMMIT'));
    assert.ok(types.includes('MICROSERVICE'));
});

test('JiraService handles issue lookup and comment authoring', async () => {
    const service = new JiraService();
    const issue = await service.getIssue('PROJ-101');
    assert.equal(issue.key, 'PROJ-101');
    assert.ok(issue.fields.summary.includes('PROJ-101'));

    const report = {
        status: 'MITIGATED',
        driftScore: 78,
        rootCause: 'Throughput spike',
        actionSummary: 'Applied queue throttle'
    };
    const receipt = await service.postRemediationComment('PROJ-101', report);
    assert.equal(receipt.receipt, 'POSTED_AUTOMATED_AUDIT');
    assert.equal(receipt.issueKey, 'PROJ-101');
});

test('DriftEngine calculates risk scores and flags anomalies', () => {
    const engine = new DriftEngine();
    const issue = { key: 'PROJ-101' };
    const graph = {
        connectedNodes: [
            {
                id: 'commit-1',
                type: 'GIT_COMMIT',
                sha: 'abc1234',
                repository: 'kestra-io/kestra',
                message: 'refactor: memory buffer adjustment'
            },
            {
                id: 'svc-1',
                type: 'MICROSERVICE',
                name: 'executor-master'
            }
        ]
    };

    const analysis = engine.analyze(issue, graph);
    assert.ok(analysis.driftScore > 50);
    assert.ok(analysis.anomalies.length >= 2);
    assert.ok(analysis.recommendedActions.length >= 2);
    assert.match(analysis.rootCause, /abc1234/);
});

test('MCP Tools Registry exposes compliant tools and handlers', async () => {
    assert.equal(MCP_TOOLS.length, 3);
    const toolNames = MCP_TOOLS.map(t => t.name);
    assert.ok(toolNames.includes('sentinel_query_teamwork_graph'));
    assert.ok(toolNames.includes('sentinel_audit_drift'));
    assert.ok(toolNames.includes('sentinel_execute_mitigation'));

    const graphRes = await handleToolCall('sentinel_query_teamwork_graph', { issueKey: 'PROJ-200' });
    assert.ok(graphRes.content[0].text.includes('PROJ-200'));

    const auditRes = await handleToolCall('sentinel_audit_drift', { issueKey: 'PROJ-200' });
    const parsedAudit = JSON.parse(auditRes.content[0].text);
    assert.ok(parsedAudit.driftScore > 0);

    const mitRes = await handleToolCall('sentinel_execute_mitigation', { issueKey: 'PROJ-200', actionId: 'ACTION_APPLY_THROTTLE' });
    const parsedMit = JSON.parse(mitRes.content[0].text);
    assert.equal(parsedMit.success, true);
});
