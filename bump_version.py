#!/usr/bin/env python3
# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "python-frontmatter>=1.3,<2",
#     "semver>=3,<4",
# ]
# ///
import argparse
from pathlib import Path

import frontmatter
import semver

def get_next_version(tag: str, strategy: str) -> str:
    version = semver.Version.parse(tag.removeprefix("v"))
    return str(version.next_version(strategy))

def set_version(text: str, version: str) -> str:
    if not frontmatter.checks(text):
        raise ValueError("SKILL.md must start with YAML frontmatter")
    post = frontmatter.loads(text)
    post["version"] = version
    return frontmatter.dumps(post, sort_keys=False)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("skill_md", type=Path, help="Path to the skill SKILL.md file")
    parser.add_argument("tag", help="The current tag")
    parser.add_argument("strategy", help="The package strategy")
    args = parser.parse_args()

    new_version = get_next_version(args.tag, args.strategy)
    args.skill_md.write_text(set_version(args.skill_md.read_text(), new_version))
    print(new_version)

if __name__ == "__main__":
    main()
