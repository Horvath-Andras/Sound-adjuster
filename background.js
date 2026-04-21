// background.js

// Üzenetkezelő a content script-től
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "sendUrlToServer") {
        console.log("📤 URL küldése a Python szervernek:", message.url);
        
        // Itt a background-ban nincs mixed content probléma!
        fetch('http://127.0.0.1:8888/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: message.url })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.text();
        })
        .then(data => {
            console.log("✅ Szerver válasz:", data);
        })
        .catch(err => {
            console.error("❌ Fetch hiba a background-ban:", err);
        });
        
        sendResponse({ status: "processing" });
        return true; // Aszinkron válasz
    }
});

// A többi kód marad (tab kezelés, badge stb.)
function inspectServer(tabId) {
    // ... eredeti kód ...
}

chrome.tabs.onActivated.addListener((activeInfo) => {
    console.log("Tab váltás:", activeInfo.tabId);
    chrome.tabs.get(activeInfo.tabId, (tab) => {
        if (tab.url) {
            // Küldjük a background-on keresztül
            fetch('http://127.0.0.1:8888/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url: tab.url })
            }).catch(err => console.log("Hiba:", err));
        }
    });
});

chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if (changeInfo.status === 'complete' && tab.url && tab.url.startsWith('http')) {
        console.log("Oldal betöltve:", tab.url);
        fetch('http://127.0.0.1:8888/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: tab.url })
        }).catch(err => console.log("Hiba:", err));
    }
});