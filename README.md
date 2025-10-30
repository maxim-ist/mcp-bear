# MCP Bear

A Python-based Model Context Protocol (MCP) server that provides access to [Bear Notes](https://bear.app).

Bear stores notes in a SQLite database. This MCP server provides both read and write access to your notes.
See: https://bear.app/faq/where-are-bears-notes-located

## Features

### Read Operations
- Read all notes (active and archived) from Bear's SQLite database
- Search notes by text content, tag, or unique ID
- List all tags
- Get notes by specific tag
- Get archived notes separately

### Note Management
- Create new notes with title, content, and tags
- Append, prepend, or replace text in existing notes
- Archive/unarchive notes for organization
- Move notes to trash

### Tag Management
- Add tags to existing notes
- Rename tags across all notes
- Open Bear showing notes with specific tag

### Bear Integration
- Open specific notes in Bear
- Search within Bear app
- All operations integrate seamlessly with Bear's UI

Write operations use Bear's official [x-callback-url API](https://bear.app/faq/x-callback-url-scheme-documentation/) for safe, reliable modifications.

## Requirements

- Python 3.10 or higher (tested with 3.14)
- Bear note application (macOS)
- Access to Bear database

## Installation

### Development Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/mcp-bear
cd mcp-bear

# Install dependencies (using mise for Python version management)
mise install
mise exec -- python -m venv .venv
.venv/bin/pip install -e .
```

### Install via pip (when published)

```bash
pip install mcp-bear
```

## Claude Desktop Configuration

Add this to your `claude_desktop_config.json`:

### Using Python directly

```json
{
  "mcpServers": {
    "bear": {
      "command": "python",
      "args": [
        "-m",
        "mcp_bear.server"
      ],
      "env": {
        "PYTHONPATH": "/Users/YOUR_USERNAME/Work/mcp-bear/src"
      }
    }
  }
}
```

### Using installed package

```json
{
  "mcpServers": {
    "bear": {
      "command": "mcp-bear"
    }
  }
}
```

## Available Tools

When the server is started, the following MCP tools become available:

### Read Operations (Basic)

- `get_notes`: Retrieves all non-archived notes
- `get_tags`: Lists all tags
- `get_notes_like`: Searches for notes containing specific text

### Read Operations (Advanced)

- `get_note_by_id`: Get a specific note by its unique identifier
- `get_notes_by_tag`: Get all notes with a specific tag
- `get_archived_notes`: Get all archived notes

### Note Management

- `create_note`: Create a new note with optional title, text, tags, and pin status
- `add_text`: Add text to an existing note (append, prepend, or replace)
- `trash_note`: Move a note to trash
- `archive_note`: Archive a note (removes from main list, keeps searchable)
- `unarchive_note`: Unarchive a note

### Tag Management

- `add_tags`: Add tags to an existing note
- `open_tag`: Open Bear and show all notes with a specific tag
- `rename_tag`: Rename a tag across all notes

### Bear Integration

- `open_note`: Open a specific note in Bear
- `search_bear`: Open Bear and show search results for a term

All write operations use Bear's official [x-callback-url scheme](https://bear.app/faq/x-callback-url-scheme-documentation/), which requires Bear to be installed and running.

## Configuration

You can override the default Bear database path by setting the `DB_ROUTE` environment variable:

```bash
export DB_ROUTE="/path/to/custom/database.sqlite"
```

## Development

### Running the server directly

```bash
cd /Users/borag/Work/mcp-bear
.venv/bin/python -m mcp_bear.server
```

### Testing with MCP Inspector

```bash
# Install the MCP inspector
pip install mcp-inspector

# Run the inspector
mcp-inspector python -m mcp_bear.server
```

## Architecture

- `mcp_bear/server.py`: Main MCP server implementation
- `mcp_bear/database.py`: SQLite database access for read operations
- `mcp_bear/bear_url.py`: Bear x-callback-url operations for write operations
- Uses Python's built-in `sqlite3` module (no native dependencies)

## Security Note

This server uses parameterized SQL queries to prevent SQL injection attacks, improving upon the original TypeScript implementation.

## License

ISC

## Author

Bora Gonul <me@boragonul.com>
