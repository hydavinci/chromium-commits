#!/usr/bin/env python3
"""
Example script: Demonstrates how to use ChromiumCommitFetcher class in code
"""

from get_chromium_commits import ChromiumCommitFetcher


def demonstrate_chromium_commit_fetcher():
    """Demonstrate usage of ChromiumCommitFetcher with example files"""
    commit_fetcher = ChromiumCommitFetcher()

    # Example file paths list
    example_file_paths = [
        "README.md",
        "components/sync/model/data_type_sync_bridge.cc",
        "components/autofill/core/browser/webdata/addresses/autofill_profile_sync_bridge.cc",
    ]

    for file_path in example_file_paths:
        print(f"\n{'='*60}")
        print(f"Checking file: {file_path}")
        print("=" * 60)

        # Get the latest commit info for the file (basic info)
        latest_commit_info = commit_fetcher.get_file_latest_commit(file_path)

        if latest_commit_info:
            commit_hash = latest_commit_info.get("commit", "N/A")
            author_name = latest_commit_info.get("author", {}).get("name", "N/A")
            commit_message = (
                latest_commit_info.get("message", "N/A").strip().split("\n")[0]
            )  # Only take the first line

            print(f"✓ Found latest commit:")
            print(f"  Hash: {commit_hash}")
            print(f"  Author: {author_name}")
            print(f"  Message: {commit_message}")

            # Get detailed info (including all modified files)
            commit_details = commit_fetcher.get_commit_details(commit_hash)
            if commit_details and "tree_diff" in commit_details:
                modified_file_count = len(commit_details["tree_diff"])
                print(f"  This commit modified {modified_file_count} files")

            # Demonstrate complete formatted output
            print("\n  Complete info preview:")
            formatted_commit_info = commit_fetcher.get_file_commit_info(
                file_path, detailed=True, show_diff=False
            )
            if formatted_commit_info:
                # Only show first few lines as preview
                preview_lines = formatted_commit_info.split("\n")[:10]
                for line in preview_lines:
                    print(f"  {line}")
                print("  ...")
        else:
            print(f"✗ Could not find commit info for file {file_path}")


if __name__ == "__main__":
    demonstrate_chromium_commit_fetcher()
