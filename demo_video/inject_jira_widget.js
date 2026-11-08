(() => {
  if (document.getElementById("sentinelforge-live-panel")) return "Already injected";

  const target = document.querySelector("h1");
  if (!target) return "Issue title h1 not found";

  const widget = document.createElement("div");
  widget.id = "sentinelforge-live-panel";
  widget.style.margin = "20px 0";
  widget.style.padding = "20px";
  widget.style.borderRadius = "12px";
  widget.style.background = "linear-gradient(135deg, #0f172a 0%, #1e293b 100%)";
  widget.style.border = "2px solid #38bdf8";
  widget.style.boxShadow = "0 10px 25px -5px rgba(0, 0, 0, 0.4)";
  widget.style.fontFamily = "-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif";
  widget.style.color = "#f8fafc";
  widget.style.position = "relative";
  widget.style.maxWidth = "800px";

  widget.innerHTML = `
    <div style="display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #334155; padding-bottom: 12px; margin-bottom: 16px;">
      <div style="display: flex; align-items: center; gap: 10px;">
        <span style="font-size: 24px;">🛡️</span>
        <div>
          <strong style="font-size: 18px; color: #38bdf8;">SentinelForge AI Context & Drift Sentinel</strong>
          <div style="font-size: 12px; color: #94a3b8;">Atlassian Forge Native Extension • Teamwork Graph Traversal Active</div>
        </div>
      </div>
      <span style="background: #0284c7; color: #fff; font-size: 11px; font-weight: bold; padding: 4px 10px; border-radius: 6px; text-transform: uppercase;">UI Kit 2</span>
    </div>

    <!-- Risk Gauge -->
    <div style="background: #0f172a; padding: 14px; border-radius: 8px; border: 1px solid #ef4444; margin-bottom: 16px;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
        <span style="font-size: 13px; color: #94a3b8; font-weight: 600; text-transform: uppercase;">Architectural Drift & Anomaly Score</span>
        <span style="font-size: 16px; font-weight: 800; color: #ef4444;">88 / 100 (CRITICAL DRIFT)</span>
      </div>
      <div style="width: 100%; height: 10px; background: #334155; border-radius: 5px; overflow: hidden;">
        <div style="width: 88%; height: 100%; background: linear-gradient(90deg, #f59e0b, #ef4444); border-radius: 5px;"></div>
      </div>
    </div>

    <!-- Teamwork Graph Traversal -->
    <div style="margin-bottom: 16px;">
      <div style="font-size: 12px; text-transform: uppercase; color: #64748b; font-weight: bold; margin-bottom: 8px;">Connected Atlassian Teamwork Graph Entities</div>
      <div style="display: flex; flex-direction: column; gap: 8px;">
        <div style="display: flex; align-items: center; gap: 10px; font-size: 13px; background: #1e293b; padding: 10px 14px; border-radius: 8px; border: 1px solid #334155;">
          <span>📄</span>
          <span><strong>Confluence:</strong> ADR-104 (Payment Gateway Resiliency & Circuit Breakers)</span>
          <span style="margin-left: auto; color: #f87171; font-size: 11px; font-weight: bold; background: #450a0a; padding: 2px 8px; border-radius: 4px;">TIMEOUT DRIFT</span>
        </div>
        <div style="display: flex; align-items: center; gap: 10px; font-size: 13px; background: #1e293b; padding: 10px 14px; border-radius: 8px; border: 1px solid #334155;">
          <span>🐙</span>
          <span><strong>Bitbucket:</strong> Commit <code>6c87776</code> (feat: async http payment client)</span>
          <span style="margin-left: auto; color: #94a3b8; font-size: 11px;">2 hours ago</span>
        </div>
        <div style="display: flex; align-items: center; gap: 10px; font-size: 13px; background: #1e293b; padding: 10px 14px; border-radius: 8px; border: 1px solid #334155;">
          <span>⚙️</span>
          <span><strong>Model Context Protocol (MCP):</strong> payment-gateway.production</span>
          <span style="margin-left: auto; color: #38bdf8; font-size: 11px; font-weight: bold;">STDIO ACTIVE</span>
        </div>
      </div>
    </div>

    <!-- Root Cause Analysis -->
    <div style="background: rgba(245, 158, 11, 0.1); border: 1px solid rgba(245, 158, 11, 0.4); padding: 12px 14px; border-radius: 8px; font-size: 13px; line-height: 1.5; color: #fde68a; margin-bottom: 16px;">
      <strong>Root Cause Isolated:</strong> Downstream gateway timeout increased to 5000ms in recent deployment, violating declared contract of 150ms in ADR-104.
    </div>

    <!-- Remediation Button -->
    <button id="sentinelforge-mitigate-btn" style="width: 100%; padding: 12px; background: #0284c7; color: white; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 8px; font-size: 14px; transition: background 0.2s;">
      <span>⚡</span>
      <span id="sentinelforge-btn-text">Execute 1-Click Remediation (Trip Circuit Breaker & Sync ADR)</span>
    </button>
  `;

  target.parentNode.insertBefore(widget, target.nextSibling);

  const btn = widget.querySelector("#sentinelforge-mitigate-btn");
  btn.onclick = () => {
    btn.style.background = "#16a34a";
    document.getElementById("sentinelforge-btn-text").innerText = "✔ Remediated: Circuit Breaker Tripped & ADR Synced via MCP";
  };

  return "Injected SentinelForge widget below h1 in Jira issue KAN-1";
})();
