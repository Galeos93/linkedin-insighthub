// Content script to scrape saved posts from the LinkedIn saved posts page.
// It looks for result items and extracts author, profile link, timestamp, text, images, and post link.

function extractText(node) {
  if (!node) return '';
  return node.innerText ? node.innerText.trim() : '';
}

function querySelectorSafe(parent, selector) {
  return parent ? parent.querySelector(selector) : null;
}

function extractPostFromResult(li) {
  try {
    const post = {};
    // Author/profile extraction (saved-post template)
    // Prefer anchors that contain the visible author name (span[aria-hidden="true"]).
    const candidateSelector = '.entity-result__content-image a[data-test-app-aware-link], .entity-result__content-actor a[data-test-app-aware-link], a[data-test-app-aware-link], a[href*="/in/"], a[href*="/company/"]';
    const authorCandidates = Array.from(li.querySelectorAll(candidateSelector));
    let authorAnchor = null;
    for (const a of authorCandidates) {
      const ah = a.querySelector('span[aria-hidden="true"]');
      if (ah && ah.textContent && ah.textContent.trim()) { authorAnchor = a; break; }
    }
    if (!authorAnchor) {
      // fallback: choose the first anchor whose visible text after removing visually-hidden
      for (const a of authorCandidates) {
        try {
          const clone = a.cloneNode(true);
          const vs = clone.querySelectorAll('.visually-hidden');
          vs.forEach(n => n.remove());
          const txt = (clone.innerText || clone.textContent || '').trim();
          if (txt && !/Estado:\s*sin\s*conexi[oó]n/i.test(txt)) { authorAnchor = a; break; }
        } catch (e) {}
      }
    }
    if (authorAnchor) {
      post.profileUrl = authorAnchor.href || '';
      const ariaHidden = authorAnchor.querySelector('span[aria-hidden="true"]');
      if (ariaHidden && ariaHidden.textContent && ariaHidden.textContent.trim()) {
        post.author = ariaHidden.textContent.trim();
      } else {
        const clone = authorAnchor.cloneNode(true);
        const vs = clone.querySelectorAll('.visually-hidden');
        vs.forEach(n => n.remove());
        post.author = (clone.innerText || clone.textContent || '').trim();
      }
      // If author extraction failed, attach debug info to help troubleshooting
      if (!post.author) {
        try {
          const ariaHiddenText = (authorAnchor.querySelector('span[aria-hidden="true"]') || {}).textContent || '';
          const clone = authorAnchor.cloneNode(true);
          const vs2 = clone.querySelectorAll('.visually-hidden');
          vs2.forEach(n => n.remove());
          const cloneText = (clone.innerText || clone.textContent || '').trim();
          const anchorText = (authorAnchor.innerText || authorAnchor.textContent || '').trim();
          post._debug = {
            anchorOuterHTML: (authorAnchor.outerHTML || '').slice(0, 1000),
            ariaHiddenText: ariaHiddenText.trim(),
            cloneText,
            anchorText
          };
        } catch (e) {
          post._debug = { error: 'debug-failed' };
        }
      }
    } else {
      post.profileUrl = '';
      post.author = '';
    }

    // Author image (profile)
    const authorImg = li.querySelector('.entity-result__content-image img, .presence-entity__image');
    post.authorImage = authorImg ? authorImg.src : '';

    // Author headline — try several stable/semantic selectors within the actor/linked-area
    const headlineSelectors = [
      '.entity-result__content-actor .t-14.t-black.t-normal',
      '.linked-area .t-14.t-black.t-normal',
      '.entity-result__content-actor .t-14.t-normal',
      '.linked-area .t-14.t-normal',
      '.entity-result__content-actor .entity-result__summary',
      '.linked-area .entity-result__summary',
      '.entity-result__content-image + .entity-result__content-actor .t-14',
      '.display-flex .t-16'
    ];
    post.authorHeadline = '';
    for (const sel of headlineSelectors) {
      try {
        const el = li.querySelector(sel);
        if (el && el.innerText && el.innerText.trim()) {
          post.authorHeadline = el.innerText.trim();
          break;
        }
      } catch (e) {}
    }

    // Timestamp
    const timeEl = li.querySelector('p.t-black--light span[aria-hidden="true"]');
    post.timestamp = timeEl ? timeEl.textContent.replace(/•.*/, '').trim() : '';

    // Post text: prefer full DOM textContent (includes hidden text) by cloning node
    let textEl = li.querySelector('.entity-result__content-summary, .entity-result__content-summary--3-lines');
    if (textEl) {
      // Clone to avoid modifying live DOM; remove any 'show more' button from clone
      try {
        const clone = textEl.cloneNode(true);
        const btn = clone.querySelector('button');
        if (btn) btn.remove();
        // Use textContent to capture hidden/truncated parts present in the DOM
        let full = (clone.textContent || '').trim();
        // If clone's text is very short, try clicking the real 'show more' and re-reading
        if (full.length < 50) {
          const moreBtn = textEl.querySelector('button.reusable-search-show-more-link');
          if (moreBtn) {
            try { moreBtn.click(); } catch (e) {}
            // small delay to allow DOM update
            // synchronous wait via Date loop (avoid async here since content script runs in page)
            const end = Date.now() + 300;
            while (Date.now() < end) {}
            full = (textEl.textContent || textEl.innerText || '').trim();
            // remove button text if present at end
            full = full.replace(/\u2026\s*ver más$/i, '').replace(/\.\.\.\s*ver más$/i, '').replace(/\u2026\s*see more$/i, '').replace(/\.\.\.\s*see more$/i, '');
          }
        }
        // final cleanup of trailing ellipses
        full = full.replace(/\u2026$/, '').replace(/\.\.\.$/, '').trim();
        post.text = full;
      } catch (e) {
        post.text = textEl.innerText ? textEl.innerText.trim() : '';
      }
    } else {
      post.text = '';
    }

    // Post image and URL (prefer the embedded-object image in the right-side container)
    let postImgEl = null;
    let postUrl = '';
    // Find the embedded-object / right container that usually holds the post preview image
    const embeddedContainer = li.querySelector('.entity-result__embedded-object, .entity-result__content-inner-container--right-padding, .GmZibUECJodTHEKEnEDawXASgixXMjghjuHxhk, .entity-result__embedded-object-image, .entity-result__content-embedded-object');
    if (embeddedContainer) {
      // Prefer specific class used for embedded images
      postImgEl = embeddedContainer.querySelector('img.entity-result__embedded-object-image, img.ivm-view-attr__img--centered, img.ivm-view-attr__img--aspect-fill, img[alt*="Vista previa"]');
      const anchorInEmbedded = embeddedContainer.querySelector('a[href*="/feed/update/"], a[href*="/posts/"], a[href*="/activity/"]');
      if (anchorInEmbedded) postUrl = anchorInEmbedded.href || '';
    }
    // Fallback: look for a post anchor anywhere in the item and take its image, but avoid picking the author's avatar
    if (!postImgEl) {
      const postAnchor = li.querySelector('a[href*="/feed/update/"], a[href*="/posts/"], a[href*="/activity/"]');
      if (postAnchor) {
        const img = postAnchor.querySelector('img');
        if (img && img.src) {
          // ignore if image matches authorImage (avatar)
          if (img.src !== post.authorImage) {
            postImgEl = img;
            postUrl = postAnchor.href || postUrl;
          }
        }
      }
    }
    post.postImage = postImgEl ? (postImgEl.src || '') : '';
    post.postUrl = postUrl;

    // urn or data attributes
    post.meta = {};
    const dataUrn = li.querySelector('[data-chameleon-result-urn]');
    if (dataUrn) post.meta.urn = dataUrn.getAttribute('data-chameleon-result-urn');

    return post;
  } catch (e) {
    return null;
  }
}

async function autoLoadAllPosts(limit) {
  let lastCount = 0;
  let tries = 0;
  while (true) {
    const posts = document.querySelectorAll('ul[role="list"] > li, ul.PvCuAmdZPNnIYDyuZWAUVSiMSoXqhwug > li');
    if (posts.length >= limit) break;
    const loadMoreBtn = document.querySelector('button.scaffold-finite-scroll__load-button');
    if (!loadMoreBtn || loadMoreBtn.disabled) break;
    loadMoreBtn.click();
    // Wait for new posts to load (up to 2s)
    await new Promise(res => setTimeout(res, 1200));
    // If no new posts loaded, break to avoid infinite loop
    if (posts.length === lastCount) {
      tries++;
      if (tries > 2) break;
    } else {
      lastCount = posts.length;
      tries = 0;
    }
  }
}

function collectSavedPosts(limit) {
  const list = document.querySelector('ul[role="list"], ul.PvCuAmdZPNnIYDyuZWAUVSiMSoXqhwug');
  if (!list) return null;
  const allItems = Array.from(list.querySelectorAll('li'));
  // Filter only saved-post templates (activity urns / content-b-template / summary 3-lines)
  const filtered = allItems.filter(li => {
    const urnEl = li.querySelector('[data-chameleon-result-urn]');
    if (urnEl) {
      const urn = urnEl.getAttribute('data-chameleon-result-urn') || '';
      if (urn.includes('activity')) return true;
    }
    const viewNameEl = li.querySelector('[data-view-name]');
    if (viewNameEl) {
      const vn = viewNameEl.getAttribute('data-view-name') || '';
      if (vn.includes('content-b-template')) return true;
    }
    if (li.querySelector('.entity-result__content-summary--3-lines')) return true;
    return false;
  }).slice(0, limit);

  const posts = filtered.map(extractPostFromResult).filter(Boolean).map(p => {
    // strip trailing "ver más" / "see more" ellipses if present
    if (p && p.text) {
      p.text = p.text.replace(/\u2026\s*ver más$/i, '').replace(/\.\.\.\s*ver más$/i, '').replace(/\u2026\s*see more$/i, '').replace(/\.\.\.\s*see more$/i, '');
      p.text = p.text.replace(/\u2026$/, '').replace(/\.\.\.$/, '').trim();
    }
    return p;
  });
  return posts;
}

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.action === 'export_saved_posts') {
    (async () => {
      try {
        const limit = typeof msg.limit === 'number' ? msg.limit : 100;
        await autoLoadAllPosts(limit);
        const data = collectSavedPosts(limit);
        if (!data) {
          sendResponse({ error: 'Could not find saved posts list on this page.' });
          return;
        }
        sendResponse({ data });
      } catch (e) {
        sendResponse({ error: e.message });
      }
    })();
    return true;
  }
  return false;
});
