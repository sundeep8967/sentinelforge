# SentinelForge

Context-aware security, compliance, and orchestration agent built on **Atlassian Forge**, integrating the **Model Context Protocol (MCP)** and **Atlassian Teamwork Graph**.

---

## Overview

SentinelForge bridges cross-product intelligence between Jira, Confluence, and external code repositories. By querying the Atlassian Teamwork Graph, it continuously constructs contextual dependency graphs to isolate configuration drift, detect unverified commit side-effects, and automate remediation workflows directly inside Jira issue views and Atlassian Rovo chat.

---

## Architectural Highlights

- **Atlassian Forge Serverless Runtime**: Hosted natively within Atlassian's secure cloud boundary using Forge UI Kit 2 (`@forge/react`).
- **Teamwork Graph Traversal**: Automatically links Jira tickets to Confluence Architectural Decision Records (ADRs), pull requests, commits, and dependent microservices.
- **Atlassian Rovo Agent**: Exposes natural language action handlers (`audit-drift-action`, `remediate-incident-action`) to the Rovo AI assistant.
- **Model Context Protocol (MCP) Server**: Full JSON-RPC 2.0 stdio server enabling external agents (Claude Desktop, Antigravity, custom LLMs) to invoke SentinelForge tools.

---

## Project Structure

```
sentinelforge/
├── manifest.yml                    # Forge app declaration (UI Kit panel, Rovo agent, actions)
├── package.json                    # Project dependencies & test scripts
├── README.md                       # Architecture & setup documentation
├── src/
│   ├── index.js                    # UI Kit Resolver definitions (getIssueContext, executeRemediation)
│   ├── agent.js                    # Atlassian Rovo Agent Action handlers
│   ├── services/
│   │   ├── teamworkGraph.js        # Teamwork Graph GraphQL query and traversal engine
│   │   ├── jiraService.js          # Jira REST v3 issue & comment management
│   │   └── driftEngine.js          # Core intelligence engine: drift calculation & anomaly scoring
│   ├── mcp/
│   │   ├── server.js               # Model Context Protocol stdio server
│   │   └── tools.js                # MCP tools registry & execution handlers
│   └── frontend/
│       └── index.jsx               # Native UI Kit 2 Jira Issue Panel React interface
└── test/
    └── sentinelforge.test.js       # Node native unit tests
```

---

## Installation & Local Verification

### 1. Install Dependencies

```bash
git clone https://github.com/sundeep8967/sentinelforge.git
cd sentinelforge
npm install
```

### 2. Run Test Suite

```bash
npm test
```

### 3. Run the Model Context Protocol (MCP) Server

You can connect external MCP clients (e.g. Claude Desktop or Antigravity) to SentinelForge:

```json
{
  "mcpServers": {
    "sentinelforge": {
      "command": "node",
      "args": ["/path/to/sentinelforge/src/mcp/server.js"]
    }
  }
}
```

### 4. Deploy to Atlassian Forge Development Site

```bash
forge deploy
forge install
```

---

## License

Apache-2.0
