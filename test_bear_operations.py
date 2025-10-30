#!/usr/bin/env python3
"""Test script for Bear MCP operations."""

import time
from mcp_bear.bear_url import (
    create_note,
    add_text,
    add_tags_to_note,
    open_note,
    search_in_bear,
    trash_note,
)
from mcp_bear.database import get_notes_like

print("=" * 60)
print("Testing MCP Bear Operations")
print("=" * 60)
print()

# Test 1: Create a new note
print("Test 1: Creating a new note with title and tags...")
result = create_note(
    title="MCP Bear Test Note",
    text="This is a test note created by the MCP Bear server.\n\n## Features\n- Read operations\n- Write operations\n- x-callback-url integration",
    tags=["mcp", "test", "automation"],
    open_note=True
)
print(f"Result: {result}")
print()

# Wait a bit for Bear to create the note
time.sleep(2)

# Test 2: Search for the note we just created
print("Test 2: Searching for the note we just created...")
notes = get_notes_like("MCP Bear Test Note")
if notes:
    test_note = notes[0]
    note_id = test_note["ZUNIQUEIDENTIFIER"]
    print(f"Found note! ID: {note_id}")
    print(f"Title: {test_note['ZTITLE']}")
    print()

    # Test 3: Append text to the note
    print("Test 3: Appending text to the note...")
    result = add_text(
        note_id=note_id,
        text="\n\n## Test Results\nSuccessfully appended text to note!",
        mode="append"
    )
    print(f"Result: {result}")
    print()

    # Test 4: Add more tags
    print("Test 4: Adding additional tags...")
    result = add_tags_to_note(
        note_id=note_id,
        tags=["python", "successful"]
    )
    print(f"Result: {result}")
    print()

    # Test 5: Open the note
    print("Test 5: Opening the note in Bear...")
    result = open_note(note_id=note_id)
    print(f"Result: {result}")
    print()

    # Wait to see the changes
    time.sleep(2)

    # Test 6: Search in Bear
    print("Test 6: Opening Bear search...")
    result = search_in_bear(term="mcp")
    print(f"Result: {result}")
    print()

    # Test 7: Trash the note (cleanup)
    input("Press Enter to trash the test note (or Ctrl+C to keep it)...")
    print("Test 7: Moving note to trash...")
    result = trash_note(note_id=note_id)
    print(f"Result: {result}")
    print()
else:
    print("Could not find the test note. Make sure Bear is running!")
    print()

print("=" * 60)
print("All tests completed!")
print("=" * 60)
