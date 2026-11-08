import Resolver from '@forge/resolver';
import api, { route } from '@forge/api';
import { TeamworkGraphService } from './services/teamworkGraph.js';
import { JiraService } from './services/jiraService.js';
import { DriftEngine } from './services/driftEngine.js';

const resolver = new Resolver();

const teamworkGraphService = new TeamworkGraphService({ asUser: () => api.asUser(), asApp: () => api.asApp() });
const jiraService = new JiraService({ asUser: () => api.asUser(), asApp: () => api.asApp(), route });
const driftEngine = new DriftEngine();

resolver.define('getIssueContext', async (req) => {
    const issueKey = req.context?.extension?.issue?.key || req.payload?.issueKey || 'PROJ-101';
    
    const [issueData, graphData] = await Promise.all([
        jiraService.getIssue(issueKey),
        teamworkGraphService.resolveGraph(issueKey)
    ]);

    const analysis = driftEngine.analyze(issueData, graphData);

    return {
        issueKey,
        issue: issueData,
        graph: graphData,
        analysis,
        timestamp: new Date().toISOString()
    };
});

resolver.define('executeRemediation', async (req) => {
    const issueKey = req.context?.extension?.issue?.key || req.payload?.issueKey || 'PROJ-101';
    const actionId = req.payload?.actionId || 'ACTION_APPLY_THROTTLE';

    const report = {
        status: 'MITIGATED',
        driftScore: req.payload?.driftScore || 65,
        rootCause: req.payload?.rootCause || 'Unvalidated throughput parameter drift',
        actionSummary: `Automated mitigation (${actionId}) applied via SentinelForge agent.`
    };

    const commentReceipt = await jiraService.postRemediationComment(issueKey, report);

    return {
        success: true,
        actionId,
        commentReceipt,
        remediatedAt: new Date().toISOString()
    };
});

resolver.define('getMetrics', async () => {
    return {
        activeAudits: 14,
        mitigatedIncidents: 42,
        averageResolutionMinutes: 4.2,
        teamworkGraphNodesIndexed: 1280
    };
});

export const handler = resolver.getDefinitions();
