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

USERNAME = "DevWithKaiju"

# Which visual theme to render. Both live under themes/ and are fully
# implemented - flip this one line (and push) to switch the whole profile:
#   "field_notes"  - lab-notebook / specimen-card cards
#   "broadsheet"   - bold display type, solid color blocks, newspaper stat grid
THEME = "field_notes"

if THEME == "broadsheet":
    from themes.broadsheet.stats import generate_stats_svg
    from themes.broadsheet.skills import generate_skills_svg
    from themes.broadsheet.kaiju import generate_kaiju_svg
    from themes.broadsheet.header import generate_header_svg
    from themes.broadsheet.certs import generate_certs_svg
    from themes.broadsheet.about import generate_about_svg
    from themes.broadsheet.links import generate_link_site_svg, generate_link_group_svg
else:
    from themes.field_notes.stats import generate_stats_svg
    from themes.field_notes.skills import generate_skills_svg
    from themes.field_notes.kaiju import generate_kaiju_svg
    from themes.field_notes.header import generate_header_svg
    from themes.field_notes.certs import generate_certs_svg
    from themes.field_notes.about import generate_about_svg
    from themes.field_notes.links import generate_link_site_svg, generate_link_group_svg


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
        "stats.svg": generate_stats_svg,
        "skills.svg": generate_skills_svg,
        "kaiju.svg": generate_kaiju_svg,
        "header.svg": generate_header_svg,
        "certifications.svg": generate_certs_svg,
        "about.svg": generate_about_svg,
        "link_site.svg": generate_link_site_svg,
        "link_group.svg": generate_link_group_svg,
    }

    for filename, gen_fn in generators.items():
        svg_content = gen_fn(data)
        out_path = images_dir / filename
        out_path.write_text(svg_content, encoding="utf-8")
        print(f"   Generated {out_path.relative_to(images_dir.parent)}")

    print("\nAll SVGs generated successfully!")


if __name__ == "__main__":
    main()
