#!/usr/bin/env python3
"""
Generate the NRD AI / NotSquat GitHub Organization profile README.
Fetches recent commits and pull requests across ALL branches and repositories in nrd-ai.
"""

import os
import json
import urllib.request
import urllib.error
import subprocess
from datetime import datetime, timezone, timedelta

ORG = "nrd-ai"
REPOS = [
    "notsquat-mobile-app",
    "Not-Squat",
    "notsquat-marketing-site",
    "NotSquat-Data-Warehouse",
    "Not-Squat-Detector-v0",
    "org-discord"
]

REPO_METADATA = {
    "Not-Squat": {
        "badge": "[![Core Repo](https://img.shields.io/badge/repo-Not--Squat-10100F?style=flat-square&logo=github)](https://github.com/nrd-ai/Not-Squat)",
        "desc": "Central hub for product specifications, brand strategy, business readiness, and canonical screenshot archive."
    },
    "notsquat-mobile-app": {
        "badge": "[![Flutter Client](https://img.shields.io/badge/repo-mobile--app-02569B?style=flat-square&logo=flutter)](https://github.com/nrd-ai/notsquat-mobile-app)",
        "desc": "iOS and Android client featuring hands-free optical capture validation, on-device Google ML Kit pose estimation, and Gymtar RPG studio."
    },
    "notsquat-marketing-site": {
        "badge": "[![Partner Site](https://img.shields.io/badge/repo-marketing--site-FF5A36?style=flat-square&logo=cloudflare)](https://github.com/nrd-ai/notsquat-marketing-site)",
        "desc": "Founding gym design-partner one-pager, operator presentation deck, and official email signature studio."
    },
    "NotSquat-Data-Warehouse": {
        "badge": "[![Data Warehouse](https://img.shields.io/badge/repo-data--warehouse-FF6F00?style=flat-square&logo=googlebigquery)](https://github.com/nrd-ai/NotSquat-Data-Warehouse)",
        "desc": "BigQuery, dbt, and Cloud Storage pipelines for privacy-preserving station occupancy and utilization telemetry."
    },
    "Not-Squat-Detector-v0": {
        "badge": "[![CV Prototype](https://img.shields.io/badge/repo-detector--v0-3776AB?style=flat-square&logo=opencv)](https://github.com/nrd-ai/Not-Squat-Detector-v0)",
        "desc": "Experimental computer-vision pipeline for barbell tracking, joint kinematics, and rep cycle state machines."
    },
    "org-discord": {
        "badge": "[![Discord Agent](https://img.shields.io/badge/repo-org--discord-5865F2?style=flat-square&logo=discord)](https://github.com/nrd-ai/org-discord)",
        "desc": "Portable REST-only agent skill with allowlisted channels for founder Discord telemetry and announcements."
    },
    ".github": {
        "badge": "[![Org Profile](https://img.shields.io/badge/repo-.github-222220?style=flat-square&logo=github)](https://github.com/nrd-ai/.github)",
        "desc": "Organization profile workspace, dashboard automations, and shared workflow assets."
    }
}

AUTHOR_MAP = {
    "murderszn": "Josh",
    "josh.johnson": "Josh",
    "josh johnson": "Josh",
    "jahflyx": "Josh",
    "maurice": "Maurice",
    "mcadenhead": "Maurice",
    "maurice cadenhead": "Maurice",
    "cadenhead": "Maurice",
    "google-labs-jules[bot]": "Jules (AI)"
}

def format_author(name_or_login):
    if not name_or_login:
        return "Team"
    key = str(name_or_login).strip().lower()
    return AUTHOR_MAP.get(key, name_or_login)

def api_get(endpoint):
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not token:
        try:
            res = subprocess.run(["gh", "api", endpoint], capture_output=True, text=True, check=True)
            return json.loads(res.stdout)
        except Exception:
            pass
    
    url = f"https://api.github.com/{endpoint}"
    req = urllib.request.Request(url)
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "nrd-ai-profile-generator")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"HTTPError on {endpoint}: {e}")
        return []
    except Exception as e:
        print(f"Error on {endpoint}: {e}")
        return []

def parse_iso_time(iso_str):
    if not iso_str:
        return None
    dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
    cdt_tz = timezone(timedelta(hours=-5))
    return dt.astimezone(cdt_tz)

def fetch_recent_activity():
    activities = []
    
    for repo in REPOS:
        # 1. Fetch Pull Requests
        pulls = api_get(f"repos/{ORG}/{repo}/pulls?state=all&sort=updated&direction=desc&per_page=10")
        if isinstance(pulls, list):
            for pr in pulls:
                created_dt = parse_iso_time(pr.get("created_at"))
                merged_dt = parse_iso_time(pr.get("merged_at"))
                effective_dt = merged_dt if merged_dt else created_dt
                if not effective_dt:
                    continue
                author = format_author(pr.get("user", {}).get("login"))
                branch_name = pr.get("head", {}).get("ref", "main")
                pr_num = pr.get("number")
                pr_title = pr.get("title")
                state = pr.get("state")
                prefix = "Merged PR" if merged_dt else f"Open PR"
                activities.append({
                    "dt": effective_dt,
                    "repo": repo,
                    "branch": branch_name,
                    "author": author,
                    "desc": f"{prefix} #{pr_num} — {pr_title}",
                    "url": pr.get("html_url")
                })
        
        # 2. Fetch all branches and commits for each branch
        branches = api_get(f"repos/{ORG}/{repo}/branches")
        if isinstance(branches, list):
            for b in branches:
                bname = b.get("name")
                if not bname:
                    continue
                commits = api_get(f"repos/{ORG}/{repo}/commits?sha={bname}&per_page=10")
                if isinstance(commits, list):
                    for c in commits:
                        commit_info = c.get("commit", {})
                        author_name = commit_info.get("author", {}).get("name")
                        author = format_author(author_name)
                        commit_dt = parse_iso_time(commit_info.get("author", {}).get("date"))
                        if not commit_dt:
                            continue
                        sha7 = c.get("sha", "")[:7]
                        first_line = commit_info.get("message", "").split("\n")[0]
                        # Skip auto-generated bot commits from flooding
                        if "auto-update organization activity" in first_line:
                            continue
                        activities.append({
                            "dt": commit_dt,
                            "repo": repo,
                            "branch": bname,
                            "author": author,
                            "desc": f"`{sha7}` — {first_line}",
                            "url": c.get("html_url")
                        })

    # Sort descending by timestamp
    activities.sort(key=lambda x: x["dt"], reverse=True)
    
    # Deduplicate
    seen = set()
    deduped = []
    for a in activities:
        key = (a["repo"], a["branch"], a["desc"][:25])
        if key not in seen:
            seen.add(key)
            deduped.append(a)
            if len(deduped) >= 30:
                break
                
    return deduped

def build_markdown(activities):
    lines = []
    lines.append('<div align="center">\n')
    lines.append('<img src="https://raw.githubusercontent.com/nrd-ai/.github/main/profile/assets/icon-192.png" width="96" height="96" alt="NotSquat" />\n')
    lines.append('# NotSquat · NRD AI\n')
    lines.append('**Equipment-utilization software & biomechanical movement intelligence for strength gyms.**\n')
    lines.append('[![Status: Private Beta](https://img.shields.io/badge/Stage-Private%20Beta-FF5A36?style=for-the-badge&logo=apple&logoColor=white)](https://notsquat.org)')
    lines.append('[![Mobile: Flutter](https://img.shields.io/badge/Client-Flutter%203.x-02569B?style=for-the-badge&logo=flutter&logoColor=white)](https://github.com/nrd-ai/notsquat-mobile-app)')
    lines.append('[![Core: Python](https://img.shields.io/badge/Engine-Python%203.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://github.com/nrd-ai/Not-Squat)')
    lines.append('[![Warehouse: BigQuery](https://img.shields.io/badge/Data-BigQuery%20%7C%20dbt-FF6F00?style=for-the-badge&logo=googlecloud&logoColor=white)](https://github.com/nrd-ai/NotSquat-Data-Warehouse)')
    lines.append('[![Discord: Bot CLI](https://img.shields.io/badge/Ops-org--discord-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://github.com/nrd-ai/org-discord)\n')
    lines.append('> *"See how your equipment is really being used."*\n')
    lines.append('</div>\n')
    lines.append('---\n')
    lines.append('## 🧭 Repository Radar\n')
    lines.append('| Repository | Status & Tech | Focus & Description | Link |')
    lines.append('|---|---|---|---|')
    radar_repos = ["Not-Squat", "notsquat-mobile-app", "notsquat-marketing-site", "NotSquat-Data-Warehouse", "Not-Squat-Detector-v0", "org-discord"]
    for repo in radar_repos:
        meta = REPO_METADATA.get(repo, {})
        lines.append(f'| [**`{repo}`**](https://github.com/{ORG}/{repo}) | {meta.get("badge", "")} | {meta.get("desc", "")} | [View Repo ➔](https://github.com/{ORG}/{repo}) |')
    
    lines.append('\n---\n')
    lines.append('## ⚡ Recent Member Updates (All Branches · Josh & Maurice)\n')
    lines.append('| Date & Time (CDT) | Repository | Branch | Author | Commit / Change Description | Link |')
    lines.append('|---|---|---|---|---|---|')
    for a in activities:
        time_str = a["dt"].strftime("%Y-%m-%d %H:%M")
        repo_link = f'[`{a["repo"]}`](https://github.com/{ORG}/{a["repo"]})'
        branch_str = f'`{a["branch"]}`'
        author_str = f'**{a["author"]}**'
        link_str = f'[Link ➔]({a["url"]})'
        desc_str = a["desc"].replace("|", "\\|")
        lines.append(f'| **{time_str}** | {repo_link} | {branch_str} | {author_str} | {desc_str} | {link_str} |')
        
    lines.append('\n---\n')
    lines.append('## 📱 Mobile App Experience Showcase\n')
    lines.append('<div align="center">')
    lines.append('<table>')
    lines.append('  <tr>')
    lines.append('    <td align="center" width="33%">')
    lines.append('      <img src="https://raw.githubusercontent.com/nrd-ai/.github/main/profile/assets/notsquat_home_dark.png" width="230" alt="Home Dashboard" /><br />')
    lines.append('      <b>01 / Capture Validation</b><br />')
    lines.append('      <sub>Hands-free scanning with Circle feed</sub>')
    lines.append('    </td>')
    lines.append('    <td align="center" width="33%">')
    lines.append('      <img src="https://raw.githubusercontent.com/nrd-ai/.github/main/profile/assets/notsquat_gymtar_dark.png" width="230" alt="Gymtar Studio" /><br />')
    lines.append('      <b>02 / Gymtar Avatar Studio</b><br />')
    lines.append('      <sub>16-bit RPG progression & attribute balance</sub>')
    lines.append('    </td>')
    lines.append('    <td align="center" width="33%">')
    lines.append('      <img src="https://raw.githubusercontent.com/nrd-ai/.github/main/profile/assets/notsquat_history_progress_dark.png" width="230" alt="Progress & History" /><br />')
    lines.append('      <b>03 / Progress & Raids</b><br />')
    lines.append('      <sub>Campaign boss drops & volume analytics</sub>')
    lines.append('    </td>')
    lines.append('  </tr>')
    lines.append('</table>')
    lines.append('</div>\n')
    lines.append('---\n')
    lines.append('## 🛡️ Core Brand & Engineering Rules\n')
    lines.append('- **Brand Source of Truth:** Consult [`docs/BRAND_STRATEGY.md`](https://github.com/nrd-ai/Not-Squat/blob/main/docs/BRAND_STRATEGY.md) and [`docs/BUSINESS_READINESS.md`](https://github.com/nrd-ai/Not-Squat/blob/main/docs/BUSINESS_READINESS.md).')
    lines.append('- **Privacy Architecture:** Focus on aggregate, station-centered metrics. Never claim unverified privacy behavior or store raw camera feeds without explicit founder agreement.')
    lines.append('- **Claims Guardrail:** Clearly separate working components from validated end-to-end results. No fabricated metrics, testimonials, or ROI claims.\n')
    lines.append('---\n')
    lines.append('## 👥 Member Shortcuts\n')
    lines.append('- 📋 [Not-Squat Issue Tracker](https://github.com/nrd-ai/Not-Squat/issues)')
    lines.append('- 🚀 [Mobile App Pull Requests](https://github.com/nrd-ai/notsquat-mobile-app/pulls)')
    lines.append('- 🎨 [Brand Guidelines](https://github.com/nrd-ai/Not-Squat/blob/main/docs/BRAND_STRATEGY.md)')
    lines.append('- 💬 [Company Discord](https://github.com/nrd-ai/org-discord)\n')
    
    return "\n".join(lines)

def main():
    print("Fetching recent organization activity across all branches and repos...")
    activities = fetch_recent_activity()
    print(f"Found {len(activities)} recent updates across all branches.")
    content = build_markdown(activities)
    
    with open("profile/README.md", "w") as f:
        f.write(content)
    with open("README.md", "w") as f:
        f.write(content)
    print("Successfully generated profile/README.md and README.md.")

if __name__ == "__main__":
    main()
