"""Database access functions for Bear Notes."""

import sqlite3
import os
from pathlib import Path
from typing import Any
from dotenv import load_dotenv

load_dotenv()


def get_bear_db_path() -> str:
    """Get the path to Bear's SQLite database."""
    db_route = os.getenv("DB_ROUTE")
    if db_route:
        return db_route

    # Default path for Bear notes on macOS
    home = Path.home()
    return str(
        home / "Library" / "Group Containers" /
        "9K33E3U3T4.net.shinyfrog.bear" / "Application Data" / "database.sqlite"
    )


def get_notes() -> list[dict[str, Any]]:
    """Retrieve all non-archived notes from Bear."""
    db_path = get_bear_db_path()
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM ZSFNOTE WHERE ZARCHIVED=0;")
        rows = cursor.fetchall()

        notes = []
        for row in rows:
            notes.append({
                "ZCREATIONDATE": row["ZCREATIONDATE"],
                "ZSUBTITLE": row["ZSUBTITLE"],
                "ZTEXT": row["ZTEXT"],
                "ZTITLE": row["ZTITLE"],
                "ZUNIQUEIDENTIFIER": row["ZUNIQUEIDENTIFIER"],
            })

        return notes
    finally:
        conn.close()


def get_notes_like(search_text: str) -> list[dict[str, Any]]:
    """Search for notes containing specific text in title or body."""
    db_path = get_bear_db_path()
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        # Use parameterized query to prevent SQL injection
        query = """
            SELECT * FROM ZSFNOTE
            WHERE ZARCHIVED=0
            AND (ZTEXT LIKE ? OR ZTITLE LIKE ?);
        """
        search_pattern = f"%{search_text}%"
        cursor.execute(query, (search_pattern, search_pattern))
        rows = cursor.fetchall()

        notes = []
        for row in rows:
            notes.append({
                "ZCREATIONDATE": row["ZCREATIONDATE"],
                "ZSUBTITLE": row["ZSUBTITLE"],
                "ZTEXT": row["ZTEXT"],
                "ZTITLE": row["ZTITLE"],
                "ZUNIQUEIDENTIFIER": row["ZUNIQUEIDENTIFIER"],
            })

        return notes
    finally:
        conn.close()


def get_tags() -> list[str]:
    """Retrieve all tags from Bear notes."""
    db_path = get_bear_db_path()
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM ZSFNOTETAG;")
        rows = cursor.fetchall()

        tags = [row["ZTITLE"] for row in rows]
        return tags
    finally:
        conn.close()


def get_note_by_id(note_id: str) -> dict[str, Any] | None:
    """
    Get a specific note by its unique identifier.

    Args:
        note_id: The unique identifier of the note (ZUNIQUEIDENTIFIER)

    Returns:
        Note dictionary or None if not found
    """
    db_path = get_bear_db_path()
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT * FROM ZSFNOTE WHERE ZUNIQUEIDENTIFIER=?;",
            (note_id,)
        )
        row = cursor.fetchone()

        if row:
            return {
                "ZCREATIONDATE": row["ZCREATIONDATE"],
                "ZMODIFICATIONDATE": row["ZMODIFICATIONDATE"],
                "ZARCHIVED": row["ZARCHIVED"],
                "ZSUBTITLE": row["ZSUBTITLE"],
                "ZTEXT": row["ZTEXT"],
                "ZTITLE": row["ZTITLE"],
                "ZUNIQUEIDENTIFIER": row["ZUNIQUEIDENTIFIER"],
            }
        return None
    finally:
        conn.close()


def get_notes_by_tag(tag: str) -> list[dict[str, Any]]:
    """
    Get all notes with a specific tag.

    Args:
        tag: Tag name (without # prefix)

    Returns:
        List of notes with the specified tag
    """
    db_path = get_bear_db_path()
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        # Search for the tag in note text (Bear stores tags inline as #tag)
        search_pattern = f"%#{tag}%"
        cursor.execute(
            """
            SELECT * FROM ZSFNOTE
            WHERE ZARCHIVED=0
            AND ZTEXT LIKE ?;
            """,
            (search_pattern,)
        )
        rows = cursor.fetchall()

        notes = []
        for row in rows:
            notes.append({
                "ZCREATIONDATE": row["ZCREATIONDATE"],
                "ZSUBTITLE": row["ZSUBTITLE"],
                "ZTEXT": row["ZTEXT"],
                "ZTITLE": row["ZTITLE"],
                "ZUNIQUEIDENTIFIER": row["ZUNIQUEIDENTIFIER"],
            })

        return notes
    finally:
        conn.close()


def get_archived_notes() -> list[dict[str, Any]]:
    """
    Retrieve all archived notes from Bear.

    Returns:
        List of archived notes
    """
    db_path = get_bear_db_path()
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM ZSFNOTE WHERE ZARCHIVED=1;")
        rows = cursor.fetchall()

        notes = []
        for row in rows:
            notes.append({
                "ZCREATIONDATE": row["ZCREATIONDATE"],
                "ZSUBTITLE": row["ZSUBTITLE"],
                "ZTEXT": row["ZTEXT"],
                "ZTITLE": row["ZTITLE"],
                "ZUNIQUEIDENTIFIER": row["ZUNIQUEIDENTIFIER"],
            })

        return notes
    finally:
        conn.close()
