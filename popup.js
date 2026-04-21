// popup.js
async function getCurrentTab() {
  let queryOptions = { active: true, lastFocusedWindow: true };
  let [tab] = await chrome.tabs.query(queryOptions);
  return tab;
}

async function showServerInfo() {
  const tab = await getCurrentTab();
  // Kérdezd meg a backgroundot, hogy mit tud az adott tabról
  // Ehhez a background.js-ben is kell egy üzenetkezelő
  // (ezt a bonyolultságot most nem részletezzük)
}

showServerInfo();