import os
import subprocess

VIDEO_DIR = "/Users/apple/Desktop/sentinelforge/demo_video"
SLIDES_DIR = os.path.join(VIDEO_DIR, "slides")

sections = [
    (
        "usecase_1",
        "Here is a live demonstration of SentinelForge running on an active incident ticket inside Jira Service Management. Ticket KAN-1 represents a critical production latency surge on the payment gateway service."
    ),
    (
        "usecase_2",
        "The SentinelForge Forge UI Kit 2 panel automatically queries the Atlassian Teamwork Graph, connecting the incident to Confluence ADR-104, recent Bitbucket commits, and production telemetry. The Drift Engine computes a critical risk score of 88 out of 100, isolating an undeclared timeout change."
    ),
    (
        "usecase_3",
        "With one click, the engineer triggers automated mitigation. SentinelForge trips the payment circuit breaker, updates Jira incident status, and initiates an asynchronous Confluence decision record synchronization."
    ),
    (
        "usecase_4",
        "SentinelForge also exposes a full Model Context Protocol stdio server. External autonomous agents and Atlassian Rovo can discover tools, query the Teamwork Graph, and execute remediations via standard JSON-RPC 2.0."
    )
]

clip_files = []

for idx, (name, text) in enumerate(sections, 1):
    aiff_path = os.path.join(VIDEO_DIR, f"{name}.aiff")
    m4a_path = os.path.join(VIDEO_DIR, f"{name}.m4a")
    png_path = os.path.join(SLIDES_DIR, f"{name}.png")
    clip_mp4 = os.path.join(VIDEO_DIR, f"usecase_clip_{idx}.mp4")

    subprocess.run(["say", "-v", "Samantha", "-r", "175", "-o", aiff_path, text], check=True)
    subprocess.run(["ffmpeg", "-y", "-i", aiff_path, "-c:a", "aac", "-b:a", "192k", m4a_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    probe = subprocess.run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", m4a_path
    ], capture_output=True, text=True, check=True)
    duration = float(probe.stdout.strip()) + 1.0

    subprocess.run([
        "ffmpeg", "-y", "-loop", "1", "-i", png_path, "-i", m4a_path,
        "-c:v", "libx264", "-tune", "stillimage", "-c:a", "aac", "-b:a", "192k",
        "-pix_fmt", "yuv420p", "-t", str(duration), "-shortest", clip_mp4
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"Generated use-case clip {idx}: {clip_mp4} ({duration:.2f}s)")
    clip_files.append(clip_mp4)

concat_list_path = os.path.join(VIDEO_DIR, "usecase_concat_list.txt")
with open(concat_list_path, "w") as f:
    for clip in clip_files:
        f.write(f"file '{clip}'\n")

final_mp4 = "/Users/apple/Desktop/sentinelforge/demo_video/SentinelForge_Live_Usecase_Demo.mp4"
subprocess.run([
    "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_list_path,
    "-c", "copy", final_mp4
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

print("Live use-case demo video generated successfully:", final_mp4)

