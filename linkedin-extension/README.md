LinkedIn Saved Posts Exporter

Install
1. Open chrome://extensions/ and enable Developer mode.
2. Click "Load unpacked" and select this folder.

Usage
1. Open LinkedIn and navigate to Saved posts (https://www.linkedin.com/my-items/saved-posts/).
2. Click the extension icon and press Export.
3. A file named linkedin-saved-posts.json will be downloaded containing an array of saved posts.

Notes
- LinkedIn's DOM may change; selectors are written to be somewhat resilient but may need updates.
- This extension only scrapes the posts currently loaded in the page (infinite scroll requires scrolling to load more posts).
