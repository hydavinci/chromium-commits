# Chromium Commits Query Tool

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![MCP](https://img.shields.io/badge/MCP-Compatible-orange.svg)](https://modelcontextprotocol.io)

A powerful tool to query the latest commit information for files in the Chromium repository. Get detailed commit data including hash, author, timestamp, commit message, modified files, and diff information through CLI, Python API, or MCP server.

## Features

- 🔍 Query latest commit information for any file in the Chromium repository
- 📊 Detailed output including commit hash, author, timestamp, and message
- 📝 View modified files and code diffs
- 🔧 Multiple interfaces: CLI, Python API, and MCP server
- 📦 Batch processing capabilities
- 🐳 Docker support for easy deployment
- 🌐 RESTful API through MCP (Model Context Protocol)

## Installation

### Prerequisites
- Python 3.8 or higher
- Internet connection (for accessing Chromium's Gitiles API)

### Quick Install

```bash
# Clone the repository
git clone <repository-url>
cd chromium-commits

# Install dependencies
pip install -r requirements.txt
```

### Docker Installation

```bash
# Build the Docker image
docker build -t chromium-commits .

# Run the container
docker run chromium-commits
```

## Usage

### Quick Start

```bash
# Basic usage - get latest commit for a file
python get_chromium_commits.py "components/sync/service/data_type_manager.cc"
```

### Command Line Interface

```bash
# Basic query
python get_chromium_commits.py "path/to/file.cc"

# Save output to file
python get_chromium_commits.py -o result.txt "path/to/file.cc"

# Batch processing multiple files
python batch_get_commits.py files.txt

# Show help
python get_chromium_commits.py --help
```

### MCP Server

Start the MCP server to enable integration with MCP-compatible tools:

```bash
# Start the server
python server.py

# Or use Docker
docker run chromium-commits
```

The MCP server provides the `get_chromium_latest_commit` tool that can be used by MCP clients to query commit information.

### Python API

Use the `ChromiumCommitFetcher` class in your Python projects:

```python
from get_chromium_commits import ChromiumCommitFetcher

# Initialize the fetcher
fetcher = ChromiumCommitFetcher()

# Get basic commit info
result = fetcher.get_file_commit_info("README.md")

# Get detailed info with diff
result = fetcher.get_file_commit_info(
    "components/sync/service/data_type_manager.cc", 
    detailed=True, 
    show_diff=True
)

print(result)
```

### Example Usage

See `example_usage.py` for comprehensive examples of how to use the ChromiumCommitFetcher class with various file paths and options.

## Project Structure

```
chromium-commits/
├── get_chromium_commits.py    # Main CLI tool and ChromiumCommitFetcher class
├── batch_get_commits.py       # Batch processing utility
├── server.py                  # MCP server implementation
├── example_usage.py           # Usage examples and demonstrations
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker configuration
├── smithery.yaml             # Smithery MCP configuration
├── LICENSE                   # MIT license
└── README.md                 # This file
```

## Output Format

The tool returns comprehensive commit information in a structured format:

```
Commit Hash: abc123def456789...
Author: John Doe <john.doe@chromium.org>
Commit Time: 2024-06-20 10:30:45 UTC
Commit Message: Fix data type manager implementation

Files modified in this commit:
[MODIFIED] components/sync/service/data_type_manager.cc
[MODIFIED] components/sync/service/data_type_manager.h
[ADDED] components/sync/service/test_helpers.cc

--- a/components/sync/service/data_type_manager.cc
+++ b/components/sync/service/data_type_manager.cc
@@ -15,6 +15,10 @@
 void DataTypeManager::Start() {
+  // Initialize sync state
+  if (!sync_state_) {
+    sync_state_ = std::make_unique<SyncState>();
+  }
   // existing implementation...
 }
```

## API Reference

### ChromiumCommitFetcher Class

#### Methods

- **`get_file_commit_info(file_path, detailed=False, show_diff=False)`**
  - `file_path` (str): Relative path to the file in Chromium repository
  - `detailed` (bool): Include detailed commit information
  - `show_diff` (bool): Include code diff in the output
  - Returns: Formatted string with commit information

- **`get_file_latest_commit(file_path)`**
  - Returns raw commit data as dictionary

## MCP Integration

This tool is compatible with the Model Context Protocol (MCP), allowing integration with MCP-enabled applications. The MCP server exposes the following tools:

- **`get_chromium_latest_commit`**: Query latest commit information for a file

## Requirements

- **Python**: 3.8 or higher
- **Dependencies**: `requests>=2.28.0` (see `requirements.txt`)
- **Network**: Internet connection to access Chromium's Gitiles API
- **Optional**: Docker for containerized deployment

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Troubleshooting

### Common Issues

- **Network connectivity**: Ensure you have internet access to reach `chromium.googlesource.com`
- **File not found**: Verify the file path exists in the Chromium repository
- **API rate limits**: The tool respects Gitiles API rate limits automatically

### Support

- Check the `example_usage.py` file for usage examples
- Review error messages for specific guidance
- Ensure all dependencies are installed correctly

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built using the Chromium Gitiles API
- Compatible with the Model Context Protocol (MCP)
- Thanks to the Chromium project for providing public API access

[![smithery badge](https://smithery.ai/badge/@hydavinci/chromium-commits)](https://smithery.ai/server/@hydavinci/chromium-commits)