# SentinelForge

Context-aware security, compliance, and orchestration agent built on **Atlassian Forge**, integrating the **Model Context Protocol (MCP)** and **Atlassian Teamwork Graph**.

## Overview
SentinelForge bridges cross-product organizational intelligence between Jira, Confluence, and external DevOps environments. Using Teamwork Graph, it continuously constructs contextual dependency graphs to identify drift, detect cross-team bottlenecks, and automate policy enforcement directly inside Jira and Rovo.

## Architecture
- **Forge App Runtime**: Serverless Forge Functions executing securely within the Atlassian cloud trust boundary.
- **Teamwork Graph**: Graph traversals across projects, goals, repositories, and incident tickets.
- **Model Context Protocol (MCP)**: Dynamic tool binding enabling AI agents (including Atlassian Rovo) to query live infrastructure and CI/CD pipelines safely.

## Setup & Local Testing
1. Clone the repository:
   ```bash
   git clone https://github.com/sundeep8967/sentinelforge.git
   cd sentinelforge
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Deploy to your Forge development environment:
   ```bash
   forge deploy
   forge install
   ```

## License
Apache-2.0
