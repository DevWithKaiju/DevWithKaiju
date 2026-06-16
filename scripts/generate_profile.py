"""
Main entry point for generating GitHub profile SVGs.
Fetches data from GitHub API and generates all SVG files.
"""

import os
import sys
from pathlib import Path

# Ensure scripts/ is on the import path
sys.path.insert(0, str(Path(__file__).parent))

from github_api import fetch_github_data
from svg_achievements import generate_achievements_svg
from svg_stats import generate_stats_svg
from svg_skills import generate_skills_svg
from svg_kaiju import generate_kaiju_svg


USERNAME = "DevWithKaiju"


def main():
    token = os.environ.get("GITHUB_TOKEN", "")

    # Output directory
    images_dir = Path(__file__).resolve().parent.parent / "images"
    images_dir.mkdir(exist_ok=True)

    # ── Fetch data ──
    print(f"Fetching data for {USERNAME}...")
    data = fetch_github_data(USERNAME, token)

    print(f"   Commits: {data['total_commits']}")
    print(f"   Stars:   {data['total_stars']}")
    print(f"   Repos:   {data['total_repos']}")
    print(f"   PRs:     {data['total_prs']}")
    print(f"   Langs:   {len(data['languages'])}")

    # ── Generate SVGs ──
    generators = {
        "achievements.svg": generate_achievements_svg,
        "stats.svg": generate_stats_svg,
        "skills.svg": generate_skills_svg,
        "kaiju.svg": generate_kaiju_svg,
    }

    for filename, gen_fn in generators.items():
        svg_content = gen_fn(data)
        out_path = images_dir / filename
        out_path.write_text(svg_content, encoding="utf-8")
        print(f"   Generated {out_path.relative_to(images_dir.parent)}")

    print("\nAll SVGs generated successfully!")


if __name__ == "__main__":
    main()
