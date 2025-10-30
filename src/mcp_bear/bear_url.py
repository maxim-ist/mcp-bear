"""Bear URL scheme operations for creating and modifying notes."""

import subprocess
import urllib.parse
from typing import Optional


def _open_bear_url(url: str) -> dict[str, str]:
    """
    Open a Bear x-callback-url and return the result.

    Args:
        url: The Bear x-callback-url to open

    Returns:
        Dictionary with result information
    """
    try:
        # Use macOS 'open' command to trigger Bear's URL scheme
        subprocess.run(["open", url], check=True, capture_output=True)
        return {"success": True, "message": "Command sent to Bear successfully"}
    except subprocess.CalledProcessError as e:
        return {"success": False, "error": str(e)}
    except Exception as e:
        return {"success": False, "error": f"Failed to open Bear URL: {str(e)}"}


def create_note(
    title: Optional[str] = None,
    text: Optional[str] = None,
    tags: Optional[list[str]] = None,
    pin: bool = False,
    open_note: bool = False
) -> dict[str, str]:
    """
    Create a new note in Bear.

    Args:
        title: Note title
        text: Note content (supports Markdown)
        tags: List of tags to add (without # prefix)
        pin: Pin the note to the top of the list
        open_note: Open the note in Bear after creation

    Returns:
        Dictionary with operation result
    """
    params = {}

    if title:
        params["title"] = title
    if text:
        params["text"] = text
    if tags:
        # Join tags with commas
        params["tags"] = ",".join(tags)
    if pin:
        params["pin"] = "yes"
    if open_note:
        params["open_note"] = "yes"

    query_string = urllib.parse.urlencode(params)
    url = f"bear://x-callback-url/create?{query_string}"

    return _open_bear_url(url)


def add_text(
    note_id: str,
    text: str,
    mode: str = "append",
    open_note: bool = False
) -> dict[str, str]:
    """
    Add text to an existing note.

    Args:
        note_id: The unique identifier of the note (ZUNIQUEIDENTIFIER)
        text: Text to add
        mode: Where to add text - "append", "prepend", or "replace"
        open_note: Open the note in Bear after modification

    Returns:
        Dictionary with operation result
    """
    if mode not in ["append", "prepend", "replace"]:
        return {"success": False, "error": f"Invalid mode: {mode}. Use append, prepend, or replace"}

    params = {
        "id": note_id,
        "text": text,
        "mode": mode
    }

    if open_note:
        params["open_note"] = "yes"

    query_string = urllib.parse.urlencode(params)
    url = f"bear://x-callback-url/add-text?{query_string}"

    return _open_bear_url(url)


def add_tags_to_note(
    note_id: str,
    tags: list[str]
) -> dict[str, str]:
    """
    Add tags to an existing note.

    Args:
        note_id: The unique identifier of the note (ZUNIQUEIDENTIFIER)
        tags: List of tags to add (without # prefix)

    Returns:
        Dictionary with operation result
    """
    params = {
        "id": note_id,
        "tags": ",".join(tags)
    }

    query_string = urllib.parse.urlencode(params)
    url = f"bear://x-callback-url/add-tags?{query_string}"

    return _open_bear_url(url)


def trash_note(note_id: str) -> dict[str, str]:
    """
    Move a note to trash.

    Args:
        note_id: The unique identifier of the note (ZUNIQUEIDENTIFIER)

    Returns:
        Dictionary with operation result
    """
    params = {"id": note_id}

    query_string = urllib.parse.urlencode(params)
    url = f"bear://x-callback-url/trash?{query_string}"

    return _open_bear_url(url)


def open_note(note_id: str) -> dict[str, str]:
    """
    Open a specific note in Bear.

    Args:
        note_id: The unique identifier of the note (ZUNIQUEIDENTIFIER)

    Returns:
        Dictionary with operation result
    """
    params = {"id": note_id}

    query_string = urllib.parse.urlencode(params)
    url = f"bear://x-callback-url/open-note?{query_string}"

    return _open_bear_url(url)


def search_in_bear(term: str) -> dict[str, str]:
    """
    Open Bear and show search results for a term.

    Args:
        term: Search term

    Returns:
        Dictionary with operation result
    """
    params = {"term": term}

    query_string = urllib.parse.urlencode(params)
    url = f"bear://x-callback-url/search?{query_string}"

    return _open_bear_url(url)


def archive_note(note_id: str) -> dict[str, str]:
    """
    Archive a note.

    Args:
        note_id: The unique identifier of the note (ZUNIQUEIDENTIFIER)

    Returns:
        Dictionary with operation result
    """
    params = {"id": note_id}

    query_string = urllib.parse.urlencode(params)
    url = f"bear://x-callback-url/archive?{query_string}"

    return _open_bear_url(url)


def unarchive_note(note_id: str) -> dict[str, str]:
    """
    Unarchive a note.

    Args:
        note_id: The unique identifier of the note (ZUNIQUEIDENTIFIER)

    Returns:
        Dictionary with operation result
    """
    params = {"id": note_id}

    query_string = urllib.parse.urlencode(params)
    url = f"bear://x-callback-url/unarchive?{query_string}"

    return _open_bear_url(url)


def open_tag(tag: str) -> dict[str, str]:
    """
    Open Bear and show all notes with a specific tag.

    Args:
        tag: Tag name (without # prefix)

    Returns:
        Dictionary with operation result
    """
    params = {"name": tag}

    query_string = urllib.parse.urlencode(params)
    url = f"bear://x-callback-url/open-tag?{query_string}"

    return _open_bear_url(url)


def rename_tag(old_tag: str, new_tag: str) -> dict[str, str]:
    """
    Rename a tag across all notes.

    Args:
        old_tag: Current tag name (without # prefix)
        new_tag: New tag name (without # prefix)

    Returns:
        Dictionary with operation result
    """
    params = {
        "name": old_tag,
        "new_name": new_tag
    }

    query_string = urllib.parse.urlencode(params)
    url = f"bear://x-callback-url/rename-tag?{query_string}"

    return _open_bear_url(url)
