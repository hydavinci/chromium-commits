#!/usr/bin/env python3
"""
Batch get latest change information for multiple files in Chromium repository
"""

import argparse
import sys
from get_chromium_commits import ChromiumCommitFetcher


def main():
    """Batch process multiple files"""
    parser = argparse.ArgumentParser(
        description='Batch get latest change information for multiple files in Chromium repository',
        epilog='Example: python batch_get_commits.py files.txt'
    )
    parser.add_argument('file_list', help='Text file containing list of file paths (one file path per line)')
    parser.add_argument('--output', '-o', help='Save output to specified file')
    
    args = parser.parse_args()    
    # Read file list
    try:
        with open(args.file_list, 'r', encoding='utf-8') as f:
            file_paths = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    except FileNotFoundError:
        print(f"Error: File {args.file_list} does not exist")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file list: {e}")
        sys.exit(1)
    
    if not file_paths:
        print("Error: File list is empty")
        sys.exit(1)
    
    fetcher = ChromiumCommitFetcher()
    results = []
    
    print(f"Starting to process {len(file_paths)} files...")
    print("-" * 80)
    
    for i, file_path in enumerate(file_paths, 1):
        print(f"[{i}/{len(file_paths)}] Processing file: {file_path}")
        
        # Show detailed information and diff by default
        result = fetcher.get_file_commit_info(
            file_path, 
            detailed=True, 
            show_diff=True
        )
        if result:
            results.append(result)
        else:
            error_msg = f"File {file_path} commit information not found"
            print(f"  ✗ {error_msg}")
            results.append(f"Error: {error_msg}")
        
        print()
    
    # Output results
    final_output = "\n\n".join(results)
    
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(final_output)
            print(f"Batch processing completed, results saved to: {args.output}")
        except Exception as e:
            print(f"Error saving file: {e}")
            print("\n" + final_output)
    else:
        print("Batch processing completed\n")
        print("=" * 80)
        print("Summary Results")
        print("=" * 80)
        print(final_output)


if __name__ == "__main__":
    main()
