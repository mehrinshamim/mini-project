chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.type === "GENERATE_ANSWERS") {
    // Forward the request to our backend
    fetch("http://localhost:8000/extension/answers", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_id: 1, // Fixed per requirements
        job_id: request.job_id,
        resume_id: request.resume_id,
        questions: request.questions
      })
    })
      .then(res => res.json())
      .then(data => sendResponse({ success: true, answers: data.answers }))
      .catch(error => sendResponse({ success: false, error: error.message }));

    return true; // Keep the message channel open for async response
  }
});
