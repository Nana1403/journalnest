"""Shared choice lists and starter page templates for notebooks.

The Pydantic schemas in ``schemas.py`` mirror these values, so keep the two
files in sync when adding a colour, pattern, font, or notebook type.
"""

# Cover colours. Values are used as CSS modifier suffixes (e.g. .cover--sage)
# and are kept stable; only the display labels track the current theme.
COLOR_CHOICES = [
    ("cream", "Cream"),
    ("blush", "Bubblegum"),
    ("sage", "Seafoam"),
    ("lavender", "Honey"),
    ("sky", "Deep Teal"),
    ("burgundy", "Deep Sea"),
]

# Cover patterns, rendered purely with CSS backgrounds.
PATTERN_CHOICES = [
    ("plain", "Plain"),
    ("dots", "Dots"),
    ("stripes", "Stripes"),
    ("grid", "Grid"),
    ("floral", "Floral"),
]

# Handwritten-style label fonts. Values map to CSS custom properties defined
# in base.html (--font-<value>).
FONT_CHOICES = [
    ("caveat", "Caveat"),
    ("patrick_hand", "Patrick Hand"),
    ("shadows", "Shadows Into Light"),
    ("gaegu", "Gaegu"),
]

# Notebook types. Each maps to a starter page template below.
TYPE_CHOICES = [
    ("class", "Class notebook"),
    ("journal", "Journal"),
    ("project", "Project notebook"),
    ("idea", "Idea book"),
    ("blank", "Blank"),
]

# Editable starter prompts inserted into a new note's body. They are only a
# starting point — users can rewrite or clear them.
PAGE_TEMPLATES: dict[str, str] = {
    "class": "Topic:\n\nKey concepts:\n\nExamples:\n\nQuestions:\n",
    "journal": "Date:\n\nThoughts:\n\nFeelings:\n\nReflections:\n",
    "project": "Goal:\n\nTasks:\n\nProgress:\n\nNext steps:\n",
    "idea": "Idea:\n\nInspiration:\n\nPossibilities:\n\nFirst step:\n",
    "blank": "",
}


def values(choices) -> list[str]:
    """Return just the stored values from a Django-style choices list."""
    return [value for value, _label in choices]
