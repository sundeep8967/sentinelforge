import os
from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 1920, 1080
SLIDES_DIR = "/Users/apple/Desktop/sentinelforge/demo_video/slides"

def get_font(size):
    font_paths = [
        "/System/Library/Fonts/SFProText-Regular.otf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/Library/Fonts/Arial.ttf"
    ]
    for p in font_paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()

font_title = get_font(38)
font_body = get_font(24)
font_code = get_font(20)

# Slide 1: Problem Intro in Jira
img1 = Image.new("RGB", (WIDTH, HEIGHT), color=(15, 23, 42))
jira_screen = Image.open(os.path.join(SLIDES_DIR, "jira_live_screen.png")).resize((1720, 920))
img1.paste(jira_screen, (100, 100))
draw1 = ImageDraw.Draw(img1)
draw1.rectangle([100, 20, 1820, 80], fill=(2, 132, 199))
draw1.text((120, 32), "Jira Service Management • Incident INC-4091: Payment Gateway Latency Surge", font=font_title, fill=(255, 255, 255))
img1.save(os.path.join(SLIDES_DIR, "usecase_1.png"))

# Slide 2: Anomaly & Drift isolated
img2 = Image.new("RGB", (WIDTH, HEIGHT), color=(15, 23, 42))
img2.paste(jira_screen, (100, 100))
draw2 = ImageDraw.Draw(img2)
draw2.rectangle([100, 20, 1820, 80], fill=(220, 38, 38))
draw2.text((120, 32), "SentinelForge Drift Engine: Traverses Teamwork Graph & Isolates 88/100 Anomaly", font=font_title, fill=(255, 255, 255))
img2.save(os.path.join(SLIDES_DIR, "usecase_2.png"))

# Slide 3: Remediated
img3 = Image.new("RGB", (WIDTH, HEIGHT), color=(15, 23, 42))
jira_remediated = Image.open(os.path.join(SLIDES_DIR, "jira_live_remediated.png")).resize((1720, 920))
img3.paste(jira_remediated, (100, 100))
draw3 = ImageDraw.Draw(img3)
draw3.rectangle([100, 20, 1820, 80], fill=(22, 163, 74))
draw3.text((120, 32), "1-Click Remediation Executed: Circuit Breaker Tripped & ADR Synced via MCP", font=font_title, fill=(255, 255, 255))
img3.save(os.path.join(SLIDES_DIR, "usecase_3.png"))

# Slide 4: Terminal MCP & Rovo execution
img4 = Image.new("RGB", (WIDTH, HEIGHT), color=(10, 15, 30))
draw4 = ImageDraw.Draw(img4)
draw4.rectangle([100, 20, 1820, 80], fill=(99, 102, 241))
draw4.text((120, 32), "Model Context Protocol (MCP) Stdio JSON-RPC 2.0 Server & Rovo Agent", font=font_title, fill=(255, 255, 255))

# Draw terminal window
draw4.rounded_rectangle([100, 110, 1820, 1020], radius=12, fill=(2, 6, 23), outline=(51, 65, 85), width=2)
# Terminal header bar
draw4.rounded_rectangle([100, 110, 1820, 160], radius=12, fill=(30, 41, 59))
draw4.ellipse([120, 128, 140, 148], fill=(239, 68, 68))
draw4.ellipse([150, 128, 170, 148], fill=(245, 158, 11))
draw4.ellipse([180, 128, 200, 148], fill=(34, 197, 94))
draw4.text((220, 126), "sentinelforge -- stdio mcp server & rovo daemon", font=font_body, fill=(148, 163, 184))

terminal_text = [
    "$ node src/mcp/server.js",
    "[MCP Server] SentinelForge MCP stdio server initialized (JSON-RPC 2.0 protocol)",
    "[MCP Registry] Registered tools: query_teamwork_graph, detect_drift, remediate_drift",
    "",
    "> Client -> {\"jsonrpc\": \"2.0\", \"id\": 1, \"method\": \"tools/call\", \"params\": {\"name\": \"query_teamwork_graph\", \"arguments\": {\"issueKey\": \"KAN-1\"}}}",
    "< Server <- {\"jsonrpc\": \"2.0\", \"id\": 1, \"result\": {\"content\": [{\"type\": \"text\", \"text\": \"Resolved 3 connected graph nodes: ADR-104, commit 6c87776, payment-gateway\"}]}}",
    "",
    "> Client -> {\"jsonrpc\": \"2.0\", \"id\": 2, \"method\": \"tools/call\", \"params\": {\"name\": \"detect_drift\", \"arguments\": {\"issueKey\": \"KAN-1\"}}}",
    "< Server <- {\"jsonrpc\": \"2.0\", \"id\": 2, \"result\": {\"riskScore\": 88, \"anomaly\": \"CRITICAL_TIMEOUT_DRIFT\", \"recommendation\": \"TRIP_CIRCUIT_BREAKER\"}}",
    "",
    "> Client -> {\"jsonrpc\": \"2.0\", \"id\": 3, \"method\": \"tools/call\", \"params\": {\"name\": \"remediate_drift\", \"arguments\": {\"issueKey\": \"KAN-1\", \"action\": \"TRIP_CIRCUIT_BREAKER\"}}}",
    "< Server <- {\"jsonrpc\": \"2.0\", \"id\": 3, \"result\": {\"status\": \"SUCCESS\", \"mitigation\": \"Circuit breaker tripped, Jira comment updated, ADR synchronized\"}}",
    "",
    "✔ 4/4 automated test suites passing: Graph resolver, Jira API service, Drift engine, MCP tool registry"
]

ty = 180
for line in terminal_text:
    color = (56, 189, 248) if line.startswith(">") else ((34, 197, 94) if line.startswith("<") or "✔" in line else ((250, 204, 21) if line.startswith("$") else (226, 232, 240)))
    draw4.text((130, ty), line, font=font_code, fill=color)
    ty += 34

img4.save(os.path.join(SLIDES_DIR, "usecase_4.png"))
print("Generated all 4 live use-case frames")

