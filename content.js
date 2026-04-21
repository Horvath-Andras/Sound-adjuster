// content.js - csak értesíti a background-ot
console.log("🎯 Content script elindult:", window.location.href);

// Küldjük a background-nak az URL-t
chrome.runtime.sendMessage({ 
    action: "sendUrlToServer", 
    url: window.location.href 
});