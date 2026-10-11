---
name: release-notes
description: >
  Draft release notes from merged pull requests or a list of commits. Use when
  asked for release notes, a changelog entry or a summary of what shipped.
---

# Release notes

1. List the merged pull requests or commits in the range you were given. If no range
   was given, ask for one; do not guess.
2. Group the changes under three headings: New, Changed, Fixed.
3. Write one line per change in plain words a delivery lead can read: what changed for
   the user, not how the code changed.
4. Link each line to its pull request or commit.
5. End with "How it was checked": the tests or checks named in the pull requests.
6. Do not invent changes. If a pull request has no description, say so.
