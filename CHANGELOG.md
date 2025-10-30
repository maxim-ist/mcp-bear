# MCP Bear Changelog

## Version 1.1.0 - Priority 1 Features (2025-10-30)

### New Features

#### Archive Management
- `archive_note` - Archive notes to remove from main list while keeping searchable
- `unarchive_note` - Restore archived notes to active list
- `get_archived_notes` - Retrieve all archived notes from database

#### Tag Management
- `get_notes_by_tag` - Get all notes with a specific tag (database search)
- `open_tag` - Open Bear showing notes with specific tag (UI integration)
- `rename_tag` - Rename tags across all notes globally

#### Advanced Search
- `get_note_by_id` - Get specific note by unique identifier
- Enhanced search capabilities for better note discovery

### Summary

Added 7 new Priority 1 tools, bringing total from 9 to 16 tools:
- **6 read operations** (was 3)
- **10 write operations** (was 6)

These features make MCP Bear production-ready for serious Bear users who need:
- Organized note management with archiving
- Powerful tag-based workflows
- Precise note retrieval by ID

### Technical Details

- All new write operations use Bear's official x-callback-url scheme
- Read operations query SQLite directly for performance
- Parameterized queries prevent SQL injection
- Full backward compatibility maintained

## Version 1.0.0 - Initial Release

### Core Features

- Read all notes from Bear
- Search notes by text content
- List all tags
- Create new notes
- Add text to notes (append/prepend/replace)
- Add tags to notes
- Trash notes
- Open notes in Bear
- Search within Bear

Initial implementation with 9 tools (3 read + 6 write).
