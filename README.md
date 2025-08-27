# Chromium Commits Query Tool

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![MCP](https://img.shields.io/badge/MCP-Compatible-orange.svg)](https://modelcontextprotocol.io)
[![smithery badge](https://smithery.ai/badge/@hydavinci/chromium-commits)](https://smithery.ai/server/@hydavinci/chromium-commits)

A comprehensive tool to query the latest commit information for files in the Chromium repository. Supports CLI usage, Python API integration, and Model Context Protocol (MCP) server functionality.

## Features

- 🔍 **Query Latest Commits**: Get detailed information about the most recent commit that modified any file in the Chromium repository
- 📊 **Comprehensive Details**: Retrieve commit hash, author, timestamp, message, and complete list of modified files
- 🔧 **Multiple Interfaces**: Use via command line, Python API, or as an MCP server
- 📁 **Batch Processing**: Process multiple files at once with batch operations
- 🐳 **Docker Support**: Easy deployment with containerization
- 🌐 **MCP Integration**: Seamless integration with AI agents and tools

## Installation

### Using UV (Recommended)
```bash
git clone https://github.com/hydavinci/chromium-commits.git
cd chromium-commits
uv sync
```

### Using pip
```bash
git clone https://github.com/hydavinci/chromium-commits.git
cd chromium-commits
pip install -r requirements.txt
```

### Using Docker
```bash
docker build -t chromium-commits .
docker run --rm chromium-commits
```

## Usage

### 🖥️ Command Line Interface (CLI)

Navigate to the `src` directory and use the following commands:

```bash
cd src

# Basic usage - get latest commit for a single file
python get_chromium_commits.py "chrome/browser/ui/browser.cc"

# Save output to file
python get_chromium_commits.py -o result.txt "components/sync/service/data_type_manager.cc"

# Show detailed diff information
python get_chromium_commits.py --show-diff "chrome/browser/ui/browser.cc"

# Batch processing multiple files
python batch_get_commits.py files.txt
```

### 🐍 Python API

```python
from src.get_chromium_commits import ChromiumCommitFetcher

# Initialize the fetcher
fetcher = ChromiumCommitFetcher()

# Get basic commit info
basic_info = fetcher.get_file_latest_commit("chrome/browser/ui/browser.cc")

# Get detailed commit info with all modified files
detailed_info = fetcher.get_file_commit_info(
    "chrome/browser/ui/browser.cc", 
    detailed=True, 
    show_diff=True
)

print(detailed_info)
```

### 🔗 MCP Server

Start the MCP server for integration with AI agents:

```bash
cd src
python server.py
```

The server provides the `get_chromium_latest_commit` tool that can be used by MCP-compatible clients.

### 📖 Example Usage

See `src/example_usage.py` for a comprehensive demonstration of the Python API:

```bash
cd src
python example_usage.py
```

## 📋 Example Output

```
=============================================================
Latest Commit Information for: chrome/browser/ui/browser.cc
=============================================================

Commit Hash: a1b2c3d4e5f6789abcdef123456789abcdef1234
Author: developer@chromium.org
Author Email: developer@chromium.org
Commit Time: 2024-12-20 15:30:45 UTC
Commit Message: [Chrome] Improve browser window management and memory optimization

Files modified in this commit (Total: 15):
[MODIFIED] chrome/browser/ui/browser.cc
[MODIFIED] chrome/browser/ui/browser.h
[MODIFIED] chrome/browser/ui/views/frame/browser_view.cc
[MODIFIED] chrome/browser/memory/tab_manager.cc
[ADDED] chrome/browser/ui/browser_memory_coordinator.cc
[ADDED] chrome/browser/ui/browser_memory_coordinator.h
[MODIFIED] chrome/test/base/browser_test_base.cc
...

Diff Details:
--- a/chrome/browser/ui/browser.cc
+++ b/chrome/browser/ui/browser.cc
@@ -123,6 +123,10 @@ void Browser::CreateTabContents() {
   web_contents->SetDelegate(this);
+  
+  // Initialize memory coordinator for better resource management
+  memory_coordinator_ = std::make_unique<BrowserMemoryCoordinator>(this);
+  memory_coordinator_->Initialize();
 }
```

## 🗂️ Common File Paths

Here are some frequently queried file paths in the Chromium repository:

### Core Chrome Browser
```bash
cd src
python get_chromium_commits.py "chrome/browser/ui/browser.cc"
python get_chromium_commits.py "chrome/browser/chrome_browser_main.cc"
python get_chromium_commits.py "chrome/browser/profiles/profile_manager.cc"
```

### Blink Rendering Engine
```bash
python get_chromium_commits.py "third_party/blink/renderer/core/dom/document.cc"
python get_chromium_commits.py "third_party/blink/renderer/core/html/parser/html_parser.cc"
python get_chromium_commits.py "third_party/blink/renderer/core/css/css_parser.cc"
```

### Component Libraries
```bash
python get_chromium_commits.py "components/sync/service/data_type_manager.cc"
python get_chromium_commits.py "components/autofill/core/browser/autofill_manager.cc"
python get_chromium_commits.py "components/password_manager/core/browser/password_manager.cc"
```

### Build and Configuration
```bash
python get_chromium_commits.py "BUILD.gn"
python get_chromium_commits.py "DEPS"
python get_chromium_commits.py ".gn"
```

### Content/Web Platform
```bash
python get_chromium_commits.py "content/browser/renderer_host/render_process_host_impl.cc"
python get_chromium_commits.py "content/renderer/render_frame_impl.cc"
```

## 📁 Project Structure

```
chromium-commits/
├── src/
│   ├── get_chromium_commits.py    # Main CLI tool and ChromiumCommitFetcher class
│   ├── batch_get_commits.py       # Batch processing utility
│   ├── example_usage.py           # Usage examples and demonstrations
│   └── server.py                  # MCP server implementation
├── pyproject.toml                 # Project configuration and dependencies
├── uv.lock                        # Dependency lock file
├── Dockerfile                     # Docker container configuration
├── smithery.yaml                  # Smithery MCP server configuration
├── LICENSE                        # MIT license
└── README.md                      # This documentation
```

## ⚙️ Requirements

- **Python**: 3.10 or higher
- **Dependencies**:
  - `requests>=2.31.0` (HTTP requests to Chromium Gitiles API)
  - `mcp>=1.0.0` (Model Context Protocol server functionality)
- **Network**: Internet connection to access Chromium Gitiles API

## 🚀 API Reference

### ChromiumCommitFetcher Class

#### Methods

- `get_file_latest_commit(file_path: str) -> Optional[Dict]`
  - Returns basic commit information for the latest change to the specified file
  
- `get_commit_details(commit_hash: str) -> Optional[Dict]`
  - Returns detailed information about a specific commit including all modified files
  
- `get_file_commit_info(file_path: str, detailed: bool = False, show_diff: bool = False) -> Optional[str]`
  - Returns formatted commit information with optional details and diff

## 🔧 Configuration

The tool uses the Chromium Gitiles API and requires no authentication. All requests are made to:
```
https://chromium.googlesource.com/chromium/src
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and add tests
4. Commit your changes: `git commit -am 'Add some feature'`
5. Push to the branch: `git push origin feature-name`
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- [Chromium Source Code](https://chromium.googlesource.com/chromium/src)
- [Chromium Gitiles API Documentation](https://gerrit.googlesource.com/gitiles/+/master/Documentation/rest-api.md)
- [Model Context Protocol](https://modelcontextprotocol.io)
- [Smithery MCP Server Registry](https://smithery.ai/server/@hydavinci/chromium-commits)