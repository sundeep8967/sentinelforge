#!/usr/bin/env python3
import os
from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 1920, 1080
SLIDES_DIR = "/Users/apple/Desktop/sentinelforge/demo_video/slides"
os.makedirs(SLIDES_DIR, exist_ok=True)

def get_font(size, bold=False):
    font_paths = [
        "/System/Library/Fonts/SFProText-Bold.otf" if bold else "/System/Library/Fonts/SFProText-Regular.otf",
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

font_jira_logo = get_font(18, bold=True)
font_nav = get_font(14)
font_title = get_font(26, bold=True)
font_h2 = get_font(18, bold=True)
font_h3 = get_font(14, bold=True)
font_body = get_font(13)
font_small = get_font(11)
font_code = get_font(12)

def draw_jira_base(remediated=False):
    # Modern Jira Dark Mode Palette
    bg_color = (24, 28, 36)      # Slate dark background
    nav_bg = (15, 18, 24)        # Top bar
    card_bg = (32, 38, 48)       # Content card
    border_color = (45, 55, 72)
    accent_blue = (0, 101, 255)  # Atlassian blue

    img = Image.new("RGB", (WIDTH, HEIGHT), color=bg_color)
    draw = ImageDraw.Draw(img)

    # 1. Top Navigation Bar (Jira Cloud)
    draw.rectangle([0, 0, WIDTH, 56], fill=nav_bg)
    draw.line([(0, 56), (WIDTH, 56)], fill=border_color, width=1)

    # Jira App Logo
    draw.rounded_rectangle([24, 14, 52, 42], radius=4, fill=accent_blue)
    draw.text((62, 18), "Jira", font=font_jira_logo, fill=(255, 255, 255))
    draw.text((102, 20), "Service Management", font=font_nav, fill=(160, 174, 192))

    nav_items = ["Your work", "Projects", "Filters", "Dashboards", "Teams", "Plans", "Apps"]
    x = 280
    for item in nav_items:
        draw.text((x, 20), item, font=font_nav, fill=(203, 213, 225))
        x += 105

    # Top Search bar & Profile
    draw.rounded_rectangle([WIDTH - 360, 12, WIDTH - 120, 44], radius=6, fill=(30, 36, 48), outline=border_color)
    draw.text((WIDTH - 340, 19), "Search Jira...", font=font_body, fill=(120, 135, 155))
    draw.ellipse([WIDTH - 80, 14, WIDTH - 50, 44], fill=accent_blue)
    draw.text((WIDTH - 73, 20), "SK", font=font_h3, fill=(255, 255, 255))

    # 2. Breadcrumbs
    draw.text((40, 78), "Projects  /  Core Infrastructure SRE (CIS)  /  INC-4091", font=font_small, fill=(148, 163, 184))

    # 3. Main Ticket Column (Left ~1100px)
    draw.text((40, 108), "INC-4091: High Latency & Worker Resource Saturation Spike", font=font_title, fill=(248, 250, 252))

    # Action Toolbar
    toolbar_buttons = ["Attach", "Create subtask", "Link issue", "Assign to me"]
    tx = 40
    for btn in toolbar_buttons:
        draw.rounded_rectangle([tx, 150, tx + 110, 180], radius=4, fill=card_bg, outline=border_color)
        draw.text((tx + 14, 158), btn, font=font_small, fill=(226, 232, 240))
        tx += 120

    # Status Pill
    draw.rounded_rectangle([tx + 20, 150, tx + 140, 180], radius=4, fill=(234, 179, 8)) # Yellow In Progress
    draw.text((tx + 36, 158), "IN PROGRESS", font=font_small, fill=(15, 23, 42))

    # Description Section
    draw.text((40, 210), "Description", font=font_h2, fill=(226, 232, 240))
    desc_lines = [
        "Automated SRE alert: Core queue worker executor latency exceeded 4500ms baseline threshold.",
        "Observed 504 Gateway Timeouts across upstream public endpoints.",
        "Configuration drift detected between live queue streaming parameters and Confluence ADR-104."
    ]
    dy = 240
    for dl in desc_lines:
        draw.text((40, dy), dl, font=font_body, fill=(180, 190, 205))
        dy += 24

    # Activity Section
    draw.line([(40, 330), (1140, 330)], fill=border_color, width=1)
    draw.text((40, 350), "Activity & Incident Log", font=font_h2, fill=(226, 232, 240))

    # Comment 1: Alert
    draw.rounded_rectangle([40, 390, 1140, 480], radius=6, fill=card_bg, outline=border_color)
    draw.ellipse([55, 405, 85, 435], fill=(220, 38, 38))
    draw.text((63, 412), "SRE", font=font_small, fill=(255, 255, 255))
    draw.text((100, 405), "Automated Sentinel Monitor • Today at 00:32 AM", font=font_small, fill=(148, 163, 184))
    draw.text((100, 430), "Severity P1 Incident declared. Throttling thresholds violated across worker-executor-fleet.", font=font_body, fill=(226, 232, 240))

    if remediated:
        # Comment 2: Remediation Receipt
        draw.rounded_rectangle([40, 500, 1140, 610], radius=6, fill=(20, 35, 30), outline=(34, 197, 94))
        draw.ellipse([55, 515, 85, 545], fill=(34, 197, 94))
        draw.text((63, 522), "SF", font=font_small, fill=(255, 255, 255))
        draw.text((100, 515), "SentinelForge Autonomous Agent • Today at 00:34 AM", font=font_small, fill=(34, 197, 94))
        draw.text((100, 538), "[SentinelForge Incident Remediation Report]", font=font_h3, fill=(255, 255, 255))
        draw.text((100, 560), "Status: MITIGATED • Drift Score: 73% • Action: ACTION_APPLY_THROTTLE applied.", font=font_body, fill=(226, 232, 240))
        draw.text((100, 582), "Confluence Retrospective published: Incident Retrospective INC-4091 (/wiki/spaces/ENG/pages/page-INC-4091)", font=font_small, fill=(56, 189, 248))

    # 4. Right Column: Native SentinelForge UI Kit Panel (~700px)
    panel_x = 1180
    panel_y = 108
    panel_w = 700
    panel_h = 920

    # Main Panel Container
    draw.rounded_rectangle([panel_x, panel_y, panel_x + panel_w, panel_y + panel_h], radius=8, fill=card_bg, outline=border_color, width=1)

    # Panel Header
    draw.rounded_rectangle([panel_x, panel_y, panel_x + panel_w, panel_y + 60], radius=8, fill=(24, 30, 42))
    draw.text((panel_x + 20, panel_y + 18), "🛡️ SentinelForge Sentinel", font=font_h2, fill=(56, 189, 248))
    # Green status lozenge
    draw.rounded_rectangle([panel_x + panel_w - 230, panel_y + 16, panel_x + panel_w - 20, panel_y + 44], radius=4, fill=(16, 185, 129))
    draw.text((panel_x + panel_w - 220, panel_y + 22), "Teamwork Graph & MCP Active", font=font_small, fill=(255, 255, 255))

    py = panel_y + 75

    if remediated:
        # Green success banner
        draw.rounded_rectangle([panel_x + 20, py, panel_x + panel_w - 20, py + 65], radius=6, fill=(20, 45, 30), outline=(34, 197, 94))
        draw.text((panel_x + 35, py + 12), "✔ Automated Remediation Dispatched", font=font_h3, fill=(34, 197, 94))
        draw.text((panel_x + 35, py + 36), "Circuit breaker applied. Confluence post-mortem published.", font=font_small, fill=(226, 232, 240))
        py += 80

    # Drift Scorecard Box
    draw.rounded_rectangle([panel_x + 20, py, panel_x + panel_w - 20, py + 95], radius=6, fill=(24, 30, 42), outline=(239, 68, 68))
    draw.text((panel_x + 35, py + 14), "System Configuration Drift", font=font_h3, fill=(248, 250, 252))
    # Danger lozenge
    draw.rounded_rectangle([panel_x + panel_w - 180, py + 12, panel_x + panel_w - 35, py + 36], radius=4, fill=(220, 38, 38))
    draw.text((panel_x + panel_w - 170, py + 16), "HIGH RISK (73%)", font=font_small, fill=(255, 255, 255))

    # Progress bar
    draw.rounded_rectangle([panel_x + 35, py + 45, panel_x + panel_w - 35, py + 55], radius=4, fill=(45, 55, 72))
    draw.rounded_rectangle([panel_x + 35, py + 45, panel_x + 35 + int((panel_w - 70) * 0.73), py + 55], radius=4, fill=(239, 68, 68))

    draw.text((panel_x + 35, py + 68), "Root Cause: Commit 9f82c14 (feat(dynamodb): enable high throughput streaming)", font=font_small, fill=(148, 163, 184))
    py += 115

    # Connected Teamwork Graph Nodes
    draw.text((panel_x + 20, py), "Connected Teamwork Graph Nodes (3)", font=font_h3, fill=(226, 232, 240))
    py += 26

    # Tag 1: Confluence ADR
    draw.rounded_rectangle([panel_x + 20, py, panel_x + 440, py + 30], radius=4, fill=(30, 58, 138))
    draw.text((panel_x + 30, py + 7), "CONFLUENCE: ADR-104 Queue Event Processing Specs", font=font_small, fill=(191, 219, 254))
    py += 36

    # Tag 2: Git Commit
    draw.rounded_rectangle([panel_x + 20, py, panel_x + 380, py + 30], radius=4, fill=(88, 28, 135))
    draw.text((panel_x + 30, py + 7), "GIT_COMMIT: 9f82c14 (kestra-io/plugin-aws)", font=font_small, fill=(233, 213, 255))
    py += 36

    # Tag 3: Microservice
    draw.rounded_rectangle([panel_x + 20, py, panel_x + 360, py + 30], radius=4, fill=(6, 78, 59))
    draw.text((panel_x + 30, py + 7), "MICROSERVICE: worker-executor-fleet (Tier 1)", font=font_small, fill=(167, 243, 208))
    py += 46

    # Infrastructure Blast-Radius Matrix
    draw.text((panel_x + 20, py), "Infrastructure Blast Radius Matrix", font=font_h3, fill=(226, 232, 240))
    py += 26

    services = [
        ("worker-executor-fleet", "Tier 1 Core", "DEGRADED", (220, 38, 38), "Runtime Infra Team"),
        ("web-api-gateway", "Tier 1 Public", "MONITORING", (245, 158, 11), "Platform Eng Team"),
        ("event-indexer-worker", "Tier 2 Internal", "HEALTHY", (34, 197, 94), "Data Pipeline Team")
    ]

    for name, tier, status, col, owner in services:
        draw.rounded_rectangle([panel_x + 20, py, panel_x + panel_w - 20, py + 48], radius=6, fill=(24, 30, 42), outline=border_color)
        draw.text((panel_x + 32, py + 8), f"{name} ({tier})", font=font_small, fill=(248, 250, 252))
        draw.rounded_rectangle([panel_x + panel_w - 130, py + 8, panel_x + panel_w - 32, py + 28], radius=4, fill=col)
        draw.text((panel_x + panel_w - 120, py + 12), status, font=font_small, fill=(255, 255, 255))
        draw.text((panel_x + 32, py + 28), f"Owner: {owner}", font=font_small, fill=(148, 163, 184))
        py += 56

    py += 10
    # Remediation & Retrospective Controls
    draw.text((panel_x + 20, py), "Remediation & Retrospective Controls", font=font_h3, fill=(226, 232, 240))
    py += 28

    # Button 1: Apply Queue Circuit Breaker
    btn1_col = (75, 85, 99) if remediated else accent_blue
    draw.rounded_rectangle([panel_x + 20, py, panel_x + 320, py + 44], radius=6, fill=btn1_col)
    draw.text((panel_x + 40, py + 12), "Apply Queue Circuit Breaker", font=font_body, fill=(255, 255, 255))

    # Button 2: Generate Confluence Post-Mortem
    btn2_col = (16, 185, 129) if remediated else (45, 55, 72)
    draw.rounded_rectangle([panel_x + 335, py, panel_x + panel_w - 20, py + 44], radius=6, fill=btn2_col)
    draw.text((panel_x + 355, py + 12), "Confluence Post-Mortem", font=font_body, fill=(255, 255, 255))

    return img

# Generate both screens
img_normal = draw_jira_base(remediated=False)
img_normal.save(os.path.join(SLIDES_DIR, "jira_live_screen.png"))
print("Saved clean jira_live_screen.png")

img_remediated = draw_jira_base(remediated=True)
img_remediated.save(os.path.join(SLIDES_DIR, "jira_live_remediated.png"))
print("Saved clean jira_live_remediated.png")
