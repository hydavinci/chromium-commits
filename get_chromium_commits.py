#!/usr/bin/env python3
"""
Get the latest change information for specified files in the Chromium repository

Features:
- Input file relative path (e.g., components/sync/utils/edge_sync_state_utils.cc)
- Output complete commit information for the latest change to that file, including all modified files
- Support for displaying detailed diff code comparison
"""

import requests
import json
import sys
import argparse
import base64
from typing import Dict, List, Optional
from datetime import datetime


class ChromiumCommitFetcher:
    """Chromium repository commit information fetcher"""
    
    def __init__(self):
        # Chromium Gitiles API base URL
        self.base_url = "https://chromium.googlesource.com/chromium/src"
        
    def get_file_latest_commit(self, file_path: str) -> Optional[Dict]:
        """
        Get the latest commit information for the specified file
        
        Args:
            file_path: Relative path of the file, e.g. "components/sync/utils/edge_sync_state_utils.cc"
            
        Returns:
            Dictionary containing commit information, or None if not found
        """
        # Normalize path format (use forward slashes)
        normalized_path = file_path.replace('\\', '/')
          # Build API URL to get commit history for this file
        url = f"{self.base_url}/+log/HEAD/{normalized_path}?format=JSON&n=1"
        
        try:
            print(f"Querying file: {normalized_path}")
            print(f"Request URL: {url}")
            
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # Gitiles API returns JSON with a security prefix that needs to be removed
            content = response.text
            if content.startswith(")]}'"):
                content = content[4:]
            
            data = json.loads(content)
            
            if 'log' not in data or not data['log']:
                print(f"Error: No commit history found for file {normalized_path}")
                return None
                
            # Get the latest commit
            latest_commit = data['log'][0]
            return latest_commit
            
        except requests.exceptions.RequestException as e:
            print(f"Network request error: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            return None
        except Exception as e:
            print(f"Unknown error: {e}")
            return None
    
    def get_commit_details(self, commit_hash: str) -> Optional[Dict]:
        """
        Get detailed information for the specified commit, including all modified files
        
        Args:
            commit_hash: The commit hash value
            
        Returns:
            Dictionary containing detailed information, or None if not found
        """
        url = f"{self.base_url}/+/{commit_hash}?format=JSON"
        
        try:
            print(f"Getting commit details: {commit_hash}")
            
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # Remove security prefix
            content = response.text
            if content.startswith(")]}'"):
                content = content[4:]
            
            data = json.loads(content)
            return data
            
        except requests.exceptions.RequestException as e:
            print(f"Network error when getting commit details: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"JSON error when parsing commit details: {e}")
            return None
        except Exception as e:
            print(f"Unknown error when getting commit details: {e}")
            return None
    
    def get_commit_diff(self, commit_hash: str) -> Optional[str]:
        """
        Get complete diff information for the specified commit
        
        Args:
            commit_hash: The commit hash value
            
        Returns:
            Complete diff content, or None if not found
        """
        # Use formatted diff URL
        url = f"{self.base_url}/+/{commit_hash}%5E%21/?format=TEXT"
        
        try:
            print(f"Getting commit diff: {commit_hash}")
            response = requests.get(url, timeout=120)  # diff may be large, increase timeout
            if response.status_code == 404:
                return None
            response.raise_for_status()
            
            # If returned content is base64 encoded, need to decode
            content = response.text
            if content and not content.startswith('diff '):
                try:
                    content = base64.b64decode(content).decode('utf-8', errors='ignore')
                except:
                    pass
            
            return content
                
        except requests.exceptions.RequestException as e:
            print(f"Network error when getting diff: {e}")
            return None
        except Exception as e:
            print(f"Unknown error when getting diff: {e}")
            return None

    def format_commit_info(self, commit_info: Dict, commit_details: Optional[Dict] = None, 
                          show_diff: bool = False, commit_diff: Optional[str] = None) -> str:
        """
        Format commit information into a readable string
        
        Args:
            commit_info: Basic commit information
            commit_details: Detailed commit information (optional)
            show_diff: Whether to show diff content
            commit_diff: Commit diff content (optional)
            
        Returns:
            Formatted string
        """
        result = []
        result.append("=" * 80)
        result.append("CHROMIUM REPOSITORY FILE LATEST CHANGE INFORMATION")
        result.append("=" * 80)
        
        # Basic information
        result.append(f"Commit Hash: {commit_info.get('commit', 'N/A')}")
        
        author_info = commit_info.get('author', {})
        author_name = author_info.get('name', 'N/A')
        author_email = author_info.get('email', 'N/A')
        result.append(f"Author: {author_name} <{author_email}>")
        
        committer_info = commit_info.get('committer', {})
        committer_name = committer_info.get('name', 'N/A')
        committer_email = committer_info.get('email', 'N/A')
        result.append(f"Committer: {committer_name} <{committer_email}>")
        
        # Time information
        if 'committer' in commit_info and 'time' in commit_info['committer']:
            commit_time = commit_info['committer']['time']
            try:
                # Parse timestamp
                dt = datetime.fromisoformat(commit_time.replace('Z', '+00:00'))
                result.append(f"Commit Time: {dt.strftime('%Y-%m-%d %H:%M:%S UTC')}")
            except:
                result.append(f"Commit Time: {commit_time}")
        
        # Commit message
        message = commit_info.get('message', 'N/A').strip()
        result.append(f"\nCommit Message:")
        result.append("-" * 40)
        for line in message.split('\n'):
            result.append(f"  {line}")
        
        # If detailed information is available, show all modified files
        if commit_details and 'tree_diff' in commit_details:
            result.append(f"\nAll files modified in this commit:")
            result.append("-" * 40)
            
            for diff in commit_details['tree_diff']:
                old_path = diff.get('old_path', '')
                new_path = diff.get('new_path', '')
                change_type = diff.get('type', 'unknown')
                
                if change_type == 'add':
                    result.append(f"  [ADDED] {new_path}")
                elif change_type == 'delete':
                    result.append(f"  [DELETED] {old_path}")
                elif change_type == 'modify':
                    result.append(f"  [MODIFIED] {new_path}")
                elif change_type == 'rename':
                    result.append(f"  [RENAMED] {old_path} -> {new_path}")
                else:
                    path = new_path or old_path
                    result.append(f"  [{change_type}] {path}")
        
        # If diff content needs to be displayed
        if show_diff and commit_diff:
            result.append(f"\nCode Change Details (DIFF):")
            result.append("=" * 80)
              # Limit diff length to avoid overly long output
            diff_lines = commit_diff.split('\n')
            max_lines = 1000  # Show maximum 1000 lines of diff
            
            if len(diff_lines) > max_lines:
                result.append(f"Note: diff content is too long, showing only first {max_lines} lines")
                result.append("-" * 40)
                for line in diff_lines[:max_lines]:
                    result.append(line)
                result.append("-" * 40)
                result.append(f"... (omitted {len(diff_lines) - max_lines} lines)")
            else:
                for line in diff_lines:
                    result.append(line)
        
        result.append("=" * 80)
        return '\n'.join(result)
    
    def get_file_commit_info(self, file_path: str, detailed: bool = True, show_diff: bool = False) -> Optional[str]:
        """
        Get complete commit information for a file
        
        Args:
            file_path: File path
            detailed: Whether to get detailed information (including all modified files)
            show_diff: Whether to show diff code comparison
            
        Returns:
            Formatted commit information string
        """
        # Get the latest commit for the file
        commit_info = self.get_file_latest_commit(file_path)
        if not commit_info:
            return None

        commit_details = None
        commit_diff = None
        
        commit_hash = commit_info.get('commit')
        if commit_hash:
            if detailed:
                commit_details = self.get_commit_details(commit_hash)
            if show_diff:
                commit_diff = self.get_commit_diff(commit_hash)

        return self.format_commit_info(commit_info, commit_details, show_diff, commit_diff)


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Get latest change information for specified files in Chromium repository',
        epilog='Example: python get_chromium_commits.py "components/sync/utils/edge_sync_state_utils.cc"'
    )
    parser.add_argument('file_path', help='Relative path of the file')
    parser.add_argument('--output', '-o', help='Save output to specified file')
    
    args = parser.parse_args()    
    fetcher = ChromiumCommitFetcher()
    
    # Get commit information, show diff by default
    result = fetcher.get_file_commit_info(
        args.file_path, 
        detailed=True, 
        show_diff=True
    )
    
    if result:
        if args.output:
            try:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(result)
                print(f"Results saved to: {args.output}")
            except Exception as e:
                print(f"Error saving file: {e}")
                print("\n" + result)
        else:
            print("\n" + result)
    else:
        print("Unable to get commit information for the file")
        sys.exit(1)


if __name__ == "__main__":
    main()
