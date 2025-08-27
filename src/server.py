#!/usr/bin/env python3
"""
Chromium Commits MCP Server

A Model Context Protocol (MCP) server that provides access to the latest
commit information for files in the Chromium repository. Supports both
HTTP and stdio transport modes.

Features:
- Get latest commit information for any file in Chromium repository
- Includes commit hash, author, timestamp, message, and modified files
- Optional diff content display
- MCP-compatible for AI agent integration
"""

import os
import uvicorn
from mcp.server.fastmcp import FastMCP
from starlette.middleware.cors import CORSMiddleware
from typing import Optional
from middleware import SmitheryConfigMiddleware
from get_chromium_commits import ChromiumCommitFetcher

mcp = FastMCP("Chromium Latest Commit")


def handle_config(config: dict):
    """Handle configuration from Smithery - for backwards compatibility with stdio mode."""
    global _server_token
    if server_token := config.get("serverToken"):
        _server_token = server_token
    # You can handle other session config fields here


# Store server token only for stdio mode (backwards compatibility)
_server_token: Optional[str] = None


def get_request_config() -> dict:
    """Get full config from current request context."""
    try:
        # Access the current request context from FastMCP
        import contextvars

        # Try to get from request context if available
        request = contextvars.copy_context().get("request")
        if hasattr(request, "scope") and request.scope:
            return request.scope.get("smithery_config", {})
    except:
        pass


def get_config_value(key: str, default=None):
    """Get a specific config value from current request."""
    config = get_request_config()
    return config.get(key, default)


def validate_server_access(server_token: Optional[str]) -> bool:
    """Validate server token - accepts any string including empty ones for demo."""
    # In a real app, you'd validate against your server's auth system
    # For demo purposes, we accept any non-empty token
    return (
        server_token is not None and len(server_token.strip()) > 0
        if server_token
        else True
    )


@mcp.tool("get_chromium_latest_commit")
async def get_chromium_latest_commit(file_path: str):
    """
    MCP handler to get the latest commit information for a specified file in Chromium repository

    Args:
        file_path (str): Relative path of the file in Chromium repository (e.g., "components/sync/service/data_type_manager.cc")

    Returns:
        str: Formatted commit information including hash, author, message, modified files list, and diff details
    """
    fetcher = ChromiumCommitFetcher()
    return fetcher.get_file_commit_info(file_path, detailed=True, show_diff=True)


def main():
    transport_mode = os.getenv("TRANSPORT", "stdio")

    if transport_mode == "http":
        # HTTP mode with config extraction from URL parameters
        print("Chromium Commits MCP Server starting in HTTP mode...")

        # Setup Starlette app with CORS for cross-origin requests
        app = mcp.streamable_http_app()

        # IMPORTANT: add CORS middleware for browser based clients
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["GET", "POST", "OPTIONS"],
            allow_headers=["*"],
            expose_headers=["mcp-session-id", "mcp-protocol-version"],
            max_age=86400,
        )

        # Apply custom middleware for config extraction (per-request API key handling)
        app = SmitheryConfigMiddleware(app)

        # Use Smithery-required PORT environment variable
        port = int(os.environ.get("PORT", 8081))
        print(f"Listening on port {port}")

        uvicorn.run(app, host="0.0.0.0", port=port, log_level="debug")

    else:
        # Optional: add stdio transport for backwards compatibility
        # You can publish this to uv for users to run locally
        print("Chromium Commits MCP Server starting in stdio mode...")

        server_token = os.getenv("SERVER_TOKEN")
        # Set the server token for stdio mode (can be None)
        handle_config({"serverToken": server_token})

        # Run with stdio transport (default)
        mcp.run()


if __name__ == "__main__":
    main()
