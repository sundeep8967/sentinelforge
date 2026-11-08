import os
from PIL import Image, ImageDraw, ImageFont

SLIDES_DIR = "/Users/apple/Desktop/sentinelforge/demo_video/slides"
os.makedirs(SLIDES_DIR, exist_ok=True)

WIDTH, HEIGHT = 1920, 1080

def get_font(size):
    font_paths = [
        "/System/Library/Fonts/SFProText-Regular.otf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf"
    ]
    for p in font_paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()

font_title = get_font(68)
font_subtitle = get_font(38)
font_body = get_font(30)
font_code = get_font(26)

slides_data = [
    {
        "filename": "slide_1.png",
        "tag": "CODEGEIST 2026 SUBMISSION",
        "title": "SentinelForge",
        "subtitle": "Autonomous Incident Mitigation & Context Engine",
        "points": [
            "• Built on Atlassian Forge, Teamwork Graph & Model Context Protocol (MCP)",
            "• Tracks Entered: Apps for Software Teams | Best Teamwork Graph | Best Atlassian MCP",
            "• Eliminates context fragmentation between Jira, Confluence, and Production"
        ]
    },
    {
        "filename": "slide_2.png",
        "tag": "THE CORE PROBLEM",
        "title": "Scattered Incident Context & Architecture Drift",
        "subtitle": "Why modern incident management fails during critical escalations",
        "points": [
            "• Confluence Architectural Decision Records (ADRs) get decoupled from Jira backlogs",
            "• Engineers spend up to 40% of incident triage locating related PRs, services, and owners",
            "• Manual context assembly delays root cause isolation and mean time to resolution (MTTR)"
        ]
    },
    {
        "filename": "slide_3.png",
        "tag": "THE ARCHITECTURE",
        "title": "Full-Stack Atlassian Forge App",
        "subtitle": "Native integration across Jira, Rovo, and external AI agents",
        "points": [
            "• Forge UI Kit 2: Live incident panel embedded directly inside Jira issue views",
            "• Atlassian Teamwork Graph: Cross-product GraphQL dependency traversal",
            "• Drift Detection Engine: Real-time contract mismatch and anomaly calculation",
            "• Model Context Protocol (MCP): JSON-RPC stdio server for universal tool integration"
        ]
    },
    {
        "filename": "slide_4.png",
        "tag": "IN ACTION: JIRA & ROVO",
        "title": "Native Jira Panel & Rovo Agent",
        "subtitle": "From automated detection to one-click mitigation",
        "points": [
            "• Real-time Anomaly Tagging: Highlights circuit breaker and schema mismatches",
            "• Rovo Custom Actions: Natural language audit and remediation directly inside Rovo chat",
            "• One-Click Remediation: Trigger circuit breaking, queue throttling, and ADR syncing"
        ]
    },
    {
        "filename": "slide_5.png",
        "tag": "DEVELOPER ARTIFACTS",
        "title": "Production-Ready Codebase & Testing",
        "subtitle": "Open source, zero third-party hosting, strictly within Atlassian trust boundary",
        "points": [
            "• 100% Passing Automated Unit Test Suite (Graph, Jira, Drift Engine, MCP Registry)",
            "• Open Source on GitHub: github.com/sundeep8967/sentinelforge",
            "• Thank you, Codegeist 2026 Evaluation Committee"
        ]
    }
]

for slide in slides_data:
    img = Image.new("RGB", (WIDTH, HEIGHT), color=(15, 23, 42)) # Slate 900
    draw = ImageDraw.Draw(img)

    # Gradient top bar
    for x in range(WIDTH):
        r = int(0 + (0 * (x / WIDTH)))
        g = int(82 + (170 * (x / WIDTH)))
        b = int(204 + (51 * (x / WIDTH)))
        draw.line([(x, 0), (x, 10)], fill=(r, g, b))

    # Badge / Tag
    draw.rectangle([100, 80, 520, 125], fill=(30, 41, 59))
    draw.text((120, 90), slide["tag"], font=font_body, fill=(56, 189, 248))

    # Title & Subtitle
    draw.text((100, 170), slide["title"], font=font_title, fill=(248, 250, 252))
    draw.text((100, 260), slide["subtitle"], font=font_subtitle, fill=(148, 163, 184))

    # Divider line
    draw.line([(100, 330), (WIDTH - 100, 330)], fill=(51, 65, 85), width=2)

    # Bullet points box
    y = 390
    for pt in slide["points"]:
        # Card background for each point
        draw.rounded_rectangle([100, y, WIDTH - 100, y + 100], radius=12, fill=(30, 41, 59))
        draw.text((130, y + 30), pt, font=font_body, fill=(226, 232, 240))
        y += 130

    # Footer
    draw.line([(100, HEIGHT - 100), (WIDTH - 100, HEIGHT - 100)], fill=(51, 65, 85), width=1)
    draw.text((100, HEIGHT - 75), "SentinelForge | Atlassian Forge + Teamwork Graph + MCP", font=font_code, fill=(100, 116, 139))
    draw.text((WIDTH - 450, HEIGHT - 75), "github.com/sundeep8967/sentinelforge", font=font_code, fill=(56, 189, 248))

    out_path = os.path.join(SLIDES_DIR, slide["filename"])
    img.save(out_path)
    print("Generated slide:", out_path)

