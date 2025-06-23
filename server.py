from mcp.server.fastmcp import FastMCP
from get_chromium_commits import ChromiumCommitFetcher

mcp = FastMCP("Chromium Latest Commit")


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


if __name__ == "__main__":
    mcp.run()
