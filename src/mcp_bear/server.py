#!/usr/bin/env python3
"""MCP Bear - Main server implementation."""

import asyncio
import logging
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Tool,
    TextContent,
    INTERNAL_ERROR,
)

from .database import (
    get_notes,
    get_notes_like,
    get_tags,
    get_note_by_id,
    get_notes_by_tag,
    get_archived_notes,
)
from .bear_url import (
    create_note,
    add_text,
    add_tags_to_note,
    trash_note,
    open_note,
    search_in_bear,
    archive_note,
    unarchive_note,
    open_tag,
    rename_tag,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create server instance
app = Server("mcp-bear")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available MCP tools."""
    return [
        Tool(
            name="get_notes",
            description="Get all notes from Bear",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="get_tags",
            description="Get all note tags. You can search notes by tags with get_notes_like",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="get_notes_like",
            description="Get notes that include a specific text string",
            inputSchema={
                "type": "object",
                "properties": {
                    "like": {
                        "type": "string",
                        "description": "Find notes that have this text",
                    },
                },
                "required": ["like"],
            },
        ),
        Tool(
            name="create_note",
            description="Create a new note in Bear",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Note title",
                    },
                    "text": {
                        "type": "string",
                        "description": "Note content (supports Markdown)",
                    },
                    "tags": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of tags to add (without # prefix)",
                    },
                    "pin": {
                        "type": "boolean",
                        "description": "Pin the note to the top",
                        "default": False,
                    },
                    "open_note": {
                        "type": "boolean",
                        "description": "Open the note in Bear after creation",
                        "default": False,
                    },
                },
            },
        ),
        Tool(
            name="add_text",
            description="Add text to an existing note",
            inputSchema={
                "type": "object",
                "properties": {
                    "note_id": {
                        "type": "string",
                        "description": "The unique identifier of the note (ZUNIQUEIDENTIFIER)",
                    },
                    "text": {
                        "type": "string",
                        "description": "Text to add",
                    },
                    "mode": {
                        "type": "string",
                        "enum": ["append", "prepend", "replace"],
                        "description": "Where to add text",
                        "default": "append",
                    },
                    "open_note": {
                        "type": "boolean",
                        "description": "Open the note in Bear after modification",
                        "default": False,
                    },
                },
                "required": ["note_id", "text"],
            },
        ),
        Tool(
            name="add_tags",
            description="Add tags to an existing note",
            inputSchema={
                "type": "object",
                "properties": {
                    "note_id": {
                        "type": "string",
                        "description": "The unique identifier of the note (ZUNIQUEIDENTIFIER)",
                    },
                    "tags": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of tags to add (without # prefix)",
                    },
                },
                "required": ["note_id", "tags"],
            },
        ),
        Tool(
            name="trash_note",
            description="Move a note to trash",
            inputSchema={
                "type": "object",
                "properties": {
                    "note_id": {
                        "type": "string",
                        "description": "The unique identifier of the note (ZUNIQUEIDENTIFIER)",
                    },
                },
                "required": ["note_id"],
            },
        ),
        Tool(
            name="open_note",
            description="Open a specific note in Bear",
            inputSchema={
                "type": "object",
                "properties": {
                    "note_id": {
                        "type": "string",
                        "description": "The unique identifier of the note (ZUNIQUEIDENTIFIER)",
                    },
                },
                "required": ["note_id"],
            },
        ),
        Tool(
            name="search_bear",
            description="Open Bear and show search results for a term",
            inputSchema={
                "type": "object",
                "properties": {
                    "term": {
                        "type": "string",
                        "description": "Search term",
                    },
                },
                "required": ["term"],
            },
        ),
        Tool(
            name="get_note_by_id",
            description="Get a specific note by its unique identifier",
            inputSchema={
                "type": "object",
                "properties": {
                    "note_id": {
                        "type": "string",
                        "description": "The unique identifier of the note (ZUNIQUEIDENTIFIER)",
                    },
                },
                "required": ["note_id"],
            },
        ),
        Tool(
            name="get_notes_by_tag",
            description="Get all notes with a specific tag",
            inputSchema={
                "type": "object",
                "properties": {
                    "tag": {
                        "type": "string",
                        "description": "Tag name (without # prefix)",
                    },
                },
                "required": ["tag"],
            },
        ),
        Tool(
            name="get_archived_notes",
            description="Get all archived notes",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="archive_note",
            description="Archive a note",
            inputSchema={
                "type": "object",
                "properties": {
                    "note_id": {
                        "type": "string",
                        "description": "The unique identifier of the note (ZUNIQUEIDENTIFIER)",
                    },
                },
                "required": ["note_id"],
            },
        ),
        Tool(
            name="unarchive_note",
            description="Unarchive a note",
            inputSchema={
                "type": "object",
                "properties": {
                    "note_id": {
                        "type": "string",
                        "description": "The unique identifier of the note (ZUNIQUEIDENTIFIER)",
                    },
                },
                "required": ["note_id"],
            },
        ),
        Tool(
            name="open_tag",
            description="Open Bear and show all notes with a specific tag",
            inputSchema={
                "type": "object",
                "properties": {
                    "tag": {
                        "type": "string",
                        "description": "Tag name (without # prefix)",
                    },
                },
                "required": ["tag"],
            },
        ),
        Tool(
            name="rename_tag",
            description="Rename a tag across all notes",
            inputSchema={
                "type": "object",
                "properties": {
                    "old_tag": {
                        "type": "string",
                        "description": "Current tag name (without # prefix)",
                    },
                    "new_tag": {
                        "type": "string",
                        "description": "New tag name (without # prefix)",
                    },
                },
                "required": ["old_tag", "new_tag"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls."""
    try:
        if name == "get_notes":
            notes = get_notes()
            return [TextContent(type="text", text=str({"notes": notes}))]

        elif name == "get_tags":
            tags = get_tags()
            return [TextContent(type="text", text=str({"tags": tags}))]

        elif name == "get_notes_like":
            if not isinstance(arguments, dict) or "like" not in arguments:
                raise ValueError("Missing required argument: like")

            search_text = arguments["like"]
            notes = get_notes_like(search_text)
            return [TextContent(type="text", text=str({"notes": notes}))]

        elif name == "create_note":
            if not isinstance(arguments, dict):
                raise ValueError("Invalid arguments")

            result = create_note(
                title=arguments.get("title"),
                text=arguments.get("text"),
                tags=arguments.get("tags"),
                pin=arguments.get("pin", False),
                open_note=arguments.get("open_note", False)
            )
            return [TextContent(type="text", text=str(result))]

        elif name == "add_text":
            if not isinstance(arguments, dict) or "note_id" not in arguments or "text" not in arguments:
                raise ValueError("Missing required arguments: note_id and text")

            result = add_text(
                note_id=arguments["note_id"],
                text=arguments["text"],
                mode=arguments.get("mode", "append"),
                open_note=arguments.get("open_note", False)
            )
            return [TextContent(type="text", text=str(result))]

        elif name == "add_tags":
            if not isinstance(arguments, dict) or "note_id" not in arguments or "tags" not in arguments:
                raise ValueError("Missing required arguments: note_id and tags")

            result = add_tags_to_note(
                note_id=arguments["note_id"],
                tags=arguments["tags"]
            )
            return [TextContent(type="text", text=str(result))]

        elif name == "trash_note":
            if not isinstance(arguments, dict) or "note_id" not in arguments:
                raise ValueError("Missing required argument: note_id")

            result = trash_note(note_id=arguments["note_id"])
            return [TextContent(type="text", text=str(result))]

        elif name == "open_note":
            if not isinstance(arguments, dict) or "note_id" not in arguments:
                raise ValueError("Missing required argument: note_id")

            result = open_note(note_id=arguments["note_id"])
            return [TextContent(type="text", text=str(result))]

        elif name == "search_bear":
            if not isinstance(arguments, dict) or "term" not in arguments:
                raise ValueError("Missing required argument: term")

            result = search_in_bear(term=arguments["term"])
            return [TextContent(type="text", text=str(result))]

        elif name == "get_note_by_id":
            if not isinstance(arguments, dict) or "note_id" not in arguments:
                raise ValueError("Missing required argument: note_id")

            note = get_note_by_id(note_id=arguments["note_id"])
            if note:
                return [TextContent(type="text", text=str({"note": note}))]
            else:
                return [TextContent(type="text", text=str({"error": "Note not found"}))]

        elif name == "get_notes_by_tag":
            if not isinstance(arguments, dict) or "tag" not in arguments:
                raise ValueError("Missing required argument: tag")

            notes = get_notes_by_tag(tag=arguments["tag"])
            return [TextContent(type="text", text=str({"notes": notes, "count": len(notes)}))]

        elif name == "get_archived_notes":
            notes = get_archived_notes()
            return [TextContent(type="text", text=str({"notes": notes, "count": len(notes)}))]

        elif name == "archive_note":
            if not isinstance(arguments, dict) or "note_id" not in arguments:
                raise ValueError("Missing required argument: note_id")

            result = archive_note(note_id=arguments["note_id"])
            return [TextContent(type="text", text=str(result))]

        elif name == "unarchive_note":
            if not isinstance(arguments, dict) or "note_id" not in arguments:
                raise ValueError("Missing required argument: note_id")

            result = unarchive_note(note_id=arguments["note_id"])
            return [TextContent(type="text", text=str(result))]

        elif name == "open_tag":
            if not isinstance(arguments, dict) or "tag" not in arguments:
                raise ValueError("Missing required argument: tag")

            result = open_tag(tag=arguments["tag"])
            return [TextContent(type="text", text=str(result))]

        elif name == "rename_tag":
            if not isinstance(arguments, dict) or "old_tag" not in arguments or "new_tag" not in arguments:
                raise ValueError("Missing required arguments: old_tag and new_tag")

            result = rename_tag(old_tag=arguments["old_tag"], new_tag=arguments["new_tag"])
            return [TextContent(type="text", text=str(result))]

        else:
            raise ValueError(f"Unknown tool: {name}")

    except Exception as e:
        logger.error(f"Error executing tool {name}: {e}", exc_info=True)
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def run_server():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options(),
        )


def main():
    """Main entry point."""
    asyncio.run(run_server())


if __name__ == "__main__":
    main()
