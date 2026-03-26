// This runs on http://localhost:3000 to sync localStorage to extension storage
function syncStorage() {
  const resume_id = localStorage.getItem("resume_id");
  const job_id = localStorage.getItem("job_id");

  if (resume_id || job_id) {
    const data = {};
    if (resume_id) data.resume_id = parseInt(resume_id, 10);
    if (job_id) data.job_id = parseInt(job_id, 10);
    chrome.storage.local.set(data);
  }
}

// Sync on load
syncStorage();

// Sync when storage changes
window.addEventListener("storage", syncStorage);

// Poll to catch local changes seamlessly since "storage" doesn't trigger in same tab
setInterval(syncStorage, 1000);
