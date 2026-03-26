document.getElementById("autofill-btn").addEventListener("click", () => {
  const btn = document.getElementById("autofill-btn");
  const status = document.getElementById("status");
  
  btn.disabled = true;
  btn.textContent = "Processing...";
  status.textContent = "Scanning page for questions...";

  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    if (tabs[0]) {
      chrome.tabs.sendMessage(tabs[0].id, { type: "TRIGGER_AUTOFILL" }, (response) => {
        if (chrome.runtime.lastError) {
          status.textContent = "Error: Could not connect to page script.";
          btn.disabled = false;
          btn.textContent = "Auto fill your job application form";
          return;
        }

        if (response && response.success) {
          status.textContent = "Form successfully auto-filled!";
        } else {
          status.textContent = response ? response.error : "Unknown error";
        }
        
        setTimeout(() => {
          window.close();
        }, 3000);
      });
    }
  });
});
