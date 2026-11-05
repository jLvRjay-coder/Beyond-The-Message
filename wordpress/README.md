# WordPress page source

These files are complete Gutenberg code-editor page-content replacements for BeyondTheMessage.org. The published pages are stored in WordPress; this repository previously contained the separate Streamlit app. Adding these files creates a versioned copy of the prepared website changes. It does not establish a live WordPress publishing connection.

## Included changes

- Home: add The Belief Files to the existing hero buttons, add a permanent navy-and-gold introduction immediately below the hero, and add a footer link.
- About: add The Belief Files as the fourth resource in a balanced two-column grid, retain the existing single-column mobile layout, and add desktop/mobile navigation and footer links.
- Every new destination is https://beyondthemessage.org/the-belief-files/.
- The new elements exist in the page HTML in their intended positions. They require no positioning script. Existing video, sharing, menu and carousel scripts are retained.

## Publishing status

This change is source-only. Committing or merging it will not update Home or About in WordPress. No WordPress deployment workflow was found in the connected Beyond the Message repositories. No publishing credentials are stored here.

For direct publishing from GitHub, a one-time authenticated WordPress publishing connection must first be configured. Keep credentials outside repository files and use a publisher that verifies page identity and detects intervening edits before writing. Refresh the current WordPress content before deployment; the public rendered baseline dates are recorded in pages.json.

The existing manual route remains available: WordPress Pages → edit Home (Front Page, ID 165) or About (ID 948) → Code editor → replace the whole page-content field with the matching pages/*.html file → Preview → Save/Update. Replacing the complete content also removes any unsaved or previously appended automatic-placement block. Keep the page title in its separate title field. WordPress revisions provide the recovery path.

## Validation

Verified before submission: each file has unique element IDs; all prior link destinations and inline scripts are preserved; each Belief Files link targets the published page; desktop and phone previews are inspected. The snapshots were derived from WordPress's public rendered page content, not an authenticated raw-content export, so a real WordPress preview is still needed before publication.
