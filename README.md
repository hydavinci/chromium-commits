# Chromium Commits Query Tool

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![MCP](https://img.shields.io/badge/MCP-Compatible-orange.svg)](https://modelcontextprotocol.io)
[![smithery badge](https://smithery.ai/badge/@hydavinci/chromium-commits)](https://smithery.ai/server/@hydavinci/chromium-commits)

Query latest commit information for files in the Chromium repository via CLI, Python API, or MCP server.

## Installation

```bash
git clone <repository-url>
cd chromium-commits
pip install -r requirements.txt
```

## Usage

### CLI
```bash
# Basic usage
python get_chromium_commits.py "chrome/browser/ui/browser.cc"

# Save to file
python get_chromium_commits.py -o result.txt "components/sync/service/data_type_manager.cc"

# Batch processing
python batch_get_commits.py files.txt
```

### Python API
```python
from get_chromium_commits import ChromiumCommitFetcher

fetcher = ChromiumCommitFetcher()
result = fetcher.get_file_commit_info("chrome/browser/ui/browser.cc", detailed=True, show_diff=True)
print(result)
```

### MCP Server
```bash
# Start server
python server.py

# Docker
docker build -t chromium-commits .
docker run --rm chromium-commits
```

## Example Output

```
Commit Hash: abc123def456789abcdef123456789abcdef1234
Author: chromium-autoroll@skia-public.iam.gserviceaccount.com
Commit Time: 2024-12-20 15:30:45 UTC
Commit Message: Roll Chrome Win64 PGO Profile

Files modified in this commit:
[MODIFIED] chrome/build/pgo_profiles.json
[MODIFIED] tools/perf/core/perf_data_generator.py
```

## Common File Paths

```bash
# Core Chrome files
python get_chromium_commits.py "chrome/browser/ui/browser.cc"
python get_chromium_commits.py "chrome/browser/chrome_browser_main.cc"

# Blink rendering engine
python get_chromium_commits.py "third_party/blink/renderer/core/dom/document.cc"

# Components
python get_chromium_commits.py "components/sync/service/data_type_manager.cc"
python get_chromium_commits.py "components/autofill/core/browser/autofill_manager.cc"

# Build files
python get_chromium_commits.py "BUILD.gn"
python get_chromium_commits.py "DEPS"
```

## Requirements

- Python 3.8+
- `requests>=2.28.0`
- `mcp>=1.0.0` (for MCP server)
- Internet connection

## License

MIT License - see [LICENSE](LICENSE) file.