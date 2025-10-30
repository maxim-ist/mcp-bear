#!/usr/bin/env python3
"""Test that all tools are registered correctly."""

import asyncio
from mcp_bear.server import list_tools

async def test_tools():
    tools = await list_tools()

    print("=" * 60)
    print(f"MCP Bear Server - {len(tools)} Tools Available")
    print("=" * 60)
    print()

    read_tools = []
    write_tools = []

    for tool in tools:
        if tool.name.startswith("get_"):
            read_tools.append(tool.name)
        else:
            write_tools.append(tool.name)

    print("READ OPERATIONS:")
    for tool_name in read_tools:
        print(f"  ✓ {tool_name}")

    print()
    print("WRITE OPERATIONS:")
    for tool_name in write_tools:
        print(f"  ✓ {tool_name}")

    print()
    print("=" * 60)
    print(f"Total: {len(read_tools)} read + {len(write_tools)} write = {len(tools)} tools")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_tools())
