import os
import subprocess

VIDEO_DIR = "/Users/apple/Desktop/sentinelforge/demo_video"
SLIDES_DIR = os.path.join(VIDEO_DIR, "slides")

sections = [
    (
        "slide_1",
        "Welcome to SentinelForge, an autonomous incident mitigation and context engine built for Codegeist 2026. SentinelForge integrates Atlassian Forge, the Teamwork Graph, and the Model Context Protocol to eliminate context fragmentation across modern software engineering workflows."
    ),
    (
        "slide_2",
        "During critical production incidents, context is scattered across disparate Jira backlogs, Confluence specifications, and Git commits. Engineers lose valuable time discovering dependencies and identifying root causes, delaying resolution."
    ),
    (
        "slide_3",
        "SentinelForge solves this with a full-stack Atlassian Forge architecture. It features a native UI Kit 2 Jira panel, a Teamwork Graph GraphQL traversal engine, an automated architectural drift detector, and a full Model Context Protocol stdio server."
    ),
    (
        "slide_4",
        "Inside Jira and Atlassian Rovo chat, SentinelForge dynamically surfaces connected architecture nodes and provides one-click automated mitigations such as circuit breaking, queue throttling, and Confluence decision record synchronization."
    ),
    (
        "slide_5",
        "SentinelForge is completely open source on GitHub with a comprehensive automated test suite. Thank you to the Atlassian Codegeist 2026 judging panel."
    )
]

clip_files = []

for idx, (name, text) in enumerate(sections, 1):
    aiff_path = os.path.join(VIDEO_DIR, f"{name}.aiff")
    m4a_path = os.path.join(VIDEO_DIR, f"{name}.m4a")
    png_path = os.path.join(SLIDES_DIR, f"{name}.png")
    clip_mp4 = os.path.join(VIDEO_DIR, f"clip_{idx}.mp4")

    # Generate speech audio with macOS say
    subprocess.run(["say", "-v", "Samantha", "-r", "175", "-o", aiff_path, text], check=True)
    subprocess.run(["ffmpeg", "-y", "-i", aiff_path, "-c:a", "aac", "-b:a", "192k", m4a_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    # Get audio duration
    probe = subprocess.run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", m4a_path
    ], capture_output=True, text=True, check=True)
    duration = float(probe.stdout.strip()) + 1.0 # padding

    # Merge image and audio into individual clip
    subprocess.run([
        "ffmpeg", "-y", "-loop", "1", "-i", png_path, "-i", m4a_path,
        "-c:v", "libx264", "-tune", "stillimage", "-c:a", "aac", "-b:a", "192k",
        "-pix_fmt", "yuv420p", "-t", str(duration), "-shortest", clip_mp4
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"Generated clip {idx}: {clip_mp4} ({duration:.2f}s)")
    clip_files.append(clip_mp4)

# Create concat list
concat_list_path = os.path.join(VIDEO_DIR, "concat_list.txt")
with open(concat_list_path, "w") as f:
    for clip in clip_files:
        f.write(f"file '{clip}'\n")

# Combine all clips
final_mp4 = "/Users/apple/Desktop/sentinelforge/demo_video/SentinelForge_Demo_Video.mp4"
subprocess.run([
    "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_list_path,
    "-c", "copy", final_mp4
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

print("Demo video generated successfully:", final_mp4)

