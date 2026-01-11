document.getElementById('export').addEventListener('click', async () => {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  if (!tab || !tab.url.includes('linkedin.com/my-items/saved-posts')) {
    document.getElementById('status').textContent = 'Please open your LinkedIn saved posts page.';
    return;
  }

  // Get post limit from input
  const postLimit = parseInt(document.getElementById('postLimit').value, 10) || 100;

  // Inject content script on demand
  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    files: ['content_script.js']
  }, () => {
    if (chrome.runtime.lastError) {
      document.getElementById('status').textContent = 'Error injecting content script: ' + chrome.runtime.lastError.message;
      return;
    }
    // Now send the message with the limit
    chrome.tabs.sendMessage(tab.id, { action: 'export_saved_posts', limit: postLimit }, (response) => {
      if (!response) {
        document.getElementById('status').textContent = 'No response from content script. Make sure you are on the saved posts page.';
        return;
      }
      const { data, error } = response;
      if (error) {
        document.getElementById('status').textContent = 'Error: ' + error;
        return;
      }
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      chrome.downloads.download({ url, filename: 'linkedin-saved-posts.json' }, () => {
        URL.revokeObjectURL(url);
        document.getElementById('status').textContent = 'Download started.';
      });
    });
  });
});
