# Chromium Commits Query Tool

A Python tool for getting the latest change information for specified files in the Chromium repository.

## Features

- Input file relative path (e.g., `components/sync/utils/edge_sync_state_utils.cc`)
- Output complete commit information for the latest change to that file, including:
  - Commit hash value
  - Author and committer information
  - Commit time
  - Commit message
  - List of all files modified in this commit

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
python get_chromium_commits.py "components/sync/utils/edge_sync_state_utils.cc"
```

### Command Line Options

- `--output <filename>` or `-o <filename>`: Save results to specified file

### Examples

1. Get complete change information for a file (including diff code comparison):
```bash
python get_chromium_commits.py "components/sync/utils/edge_sync_state_utils.cc"
```

2. Save results to a file:
```bash
python get_chromium_commits.py -o result.txt "components/sync/utils/edge_sync_state_utils.cc"
```

## Batch Processing

The tool also provides batch processing functionality to handle multiple files at once:

```bash
# Batch get file information (including diff)
python batch_get_commits.py files.txt

# Batch process and save results
python batch_get_commits.py -o batch_results.txt files.txt
```

File list format (one file path per line, lines starting with # are comments):
```
# Example file list
README.md
components/sync/model/model_type_sync_bridge.cc
components/autofill/core/browser/webdata/addresses/autofill_profile_sync_bridge.cc
```

## Output Format

The tool outputs information in the following format:

```
================================================================================
CHROMIUM REPOSITORY FILE LATEST CHANGE INFORMATION
================================================================================
Commit Hash: abc123def456...
Author: John Doe <john.doe@chromium.org>
Committer: John Doe <john.doe@chromium.org>
Commit Time: 2024-06-20 10:30:45 UTC

Commit Message:
----------------------------------------
  Fix edge sync state utils implementation
  
  This commit fixes several issues in the edge sync state utilities
  and improves error handling.

All files modified in this commit:
----------------------------------------
  [MODIFIED] components/sync/utils/edge_sync_state_utils.cc
  [MODIFIED] components/sync/utils/edge_sync_state_utils.h
  [ADDED] components/sync/utils/edge_sync_state_utils_unittest.cc

Code Change Details (DIFF):
================================================================================
diff --git a/components/sync/utils/edge_sync_state_utils.cc b/components/sync/utils/edge_sync_state_utils.cc
index 1234567..abcdefg 100644
--- a/components/sync/utils/edge_sync_state_utils.cc
+++ b/components/sync/utils/edge_sync_state_utils.cc
@@ -10,6 +10,10 @@
 
 namespace sync_utils {
 
+bool IsEdgeSyncEnabled() {
+  return base::FeatureList::IsEnabled(features::kEdgeSync);
+}
+
 void InitializeEdgeSyncState() {
   // Implementation details...
 }
================================================================================
```

## Notes

- Requires network connection to access Chromium's Git repository API
- File paths use paths relative to the Chromium source root directory
- Supports both Windows and Unix style path separators (automatically converted)
- Getting diff content may take a long time, especially for large commits
- Diff output is limited to 1000 lines to avoid excessively long output (full diff will be saved to file)
- **Default Feature**: The tool now shows detailed diff code comparison by default

## API Documentation

This tool uses Chromium's Gitiles API to get information:
- Base URL: `https://chromium.googlesource.com/chromium/src`
- Get file history: `/+log/<file_path>?format=JSON&n=1`
- Get commit details: `/+/<commit_hash>?format=JSON`