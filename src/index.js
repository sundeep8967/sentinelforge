import api, { route } from '@forge/api';

export async function run(event, context) {
    const issueKey = event.issue?.key;
    return {
        status: "active",
        agent: "SentinelForge",
        issue: issueKey,
        context: "Teamwork Graph & MCP Connected"
    };
}
