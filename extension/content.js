// content.js - Job Autofiller Content Script

// ─── Utilities ────────────────────────────────────────────────────────────────

function cleanLabel(text) {
  if (!text) return "";
  return text
    .replace(/\*/g, "")
    .replace(/\bRequired\b/gi, "")
    .replace(/\bOptional\b/gi, "")
    .replace(/[\r\n\t]+/g, " ")
    .replace(/\s{2,}/g, " ")
    .trim();
}

// ─── Label Detection ──────────────────────────────────────────────────────────

function getLabelForInput(input) {
  let text = "";

  // 1. aria-label attribute
  if (input.getAttribute("aria-label")) {
    text = cleanLabel(input.getAttribute("aria-label"));
    if (text) return text;
  }

  // 2. aria-labelledby (space-separated list of element IDs)
  if (input.getAttribute("aria-labelledby")) {
    const ids = input.getAttribute("aria-labelledby").split(/\s+/);
    const parts = ids
      .map(id => document.getElementById(id))
      .filter(Boolean)
      .map(el => el.innerText);
    text = cleanLabel(parts.join(" "));
    if (text) return text;
  }

  // 3. Native label association via input.labels HTMLCollection
  if (input.labels && input.labels.length > 0) {
    text = cleanLabel(input.labels[0].innerText);
    if (text) return text;
  }

  // 4. label[for="id"] DOM query
  if (input.id) {
    const label = document.querySelector(`label[for="${CSS.escape(input.id)}"]`);
    if (label) {
      text = cleanLabel(label.innerText);
      if (text) return text;
    }
  }

  // 5. Walk DOM tree up to 8 ancestor levels, checking preceding siblings at each level.
  //    This is the key strategy for Google Forms and other form builders where the
  //    question title is a sibling/ancestor, not a direct <label> element.
  let ancestor = input.parentElement;
  for (let depth = 0; depth < 8 && ancestor; depth++) {
    let sibling = ancestor.previousElementSibling;
    while (sibling) {
      // Skip siblings that contain other inputs — they belong to a different question
      if (sibling.querySelector("input, select, textarea")) {
        sibling = sibling.previousElementSibling;
        continue;
      }
      const siblingText = cleanLabel(sibling.innerText);
      if (siblingText && siblingText.length < 200) {
        return siblingText;
      }
      sibling = sibling.previousElementSibling;
    }
    ancestor = ancestor.parentElement;
  }

  // 6. placeholder attribute (last resort — functional hint, not a true label)
  if (input.placeholder) {
    text = cleanLabel(input.placeholder);
    if (text) return text;
  }

  return "";
}

// ─── Scraping ─────────────────────────────────────────────────────────────────

function scrapeQuestions() {
  const fields = [];
  const seenLabels = new Set();

  // Text-like inputs and selects
  const inputSelector = [
    'input[type="text"]',
    'input[type="email"]',
    'input[type="tel"]',
    'input[type="number"]',
    'input[type="url"]',
    'input[type="date"]',
    'input:not([type])',
    'textarea',
    'select',
  ].join(", ");

  document.querySelectorAll(inputSelector).forEach(input => {
    const labelText = getLabelForInput(input);
    if (!labelText || seenLabels.has(labelText)) return;
    seenLabels.add(labelText);
    fields.push({ element: input, question: labelText, type: "text" });
  });

  // Radio groups: one entry per named group
  const radioGroups = new Map();
  document.querySelectorAll('input[type="radio"]').forEach(radio => {
    if (radio.name && !radioGroups.has(radio.name)) {
      radioGroups.set(radio.name, radio);
    }
  });
  radioGroups.forEach((firstRadio, groupName) => {
    const labelText = getLabelForInput(firstRadio);
    if (!labelText || seenLabels.has(labelText)) return;
    seenLabels.add(labelText);
    const allRadios = Array.from(
      document.querySelectorAll(`input[type="radio"][name="${CSS.escape(groupName)}"]`)
    );
    fields.push({ element: firstRadio, allRadios, question: labelText, type: "radio" });
  });

  // ARIA radio groups (e.g., Google Forms) — these have no native input[type="radio"].
  // Each group is a div[role="radiogroup"] with aria-labelledby for the question title,
  // and div[role="radio"] children with aria-label for each option.
  document.querySelectorAll('[role="radiogroup"]').forEach(group => {
    const labelText = getLabelForInput(group);
    if (!labelText || seenLabels.has(labelText)) return;
    seenLabels.add(labelText);
    const allOptions = Array.from(group.querySelectorAll('[role="radio"]'));
    fields.push({ element: group, allOptions, question: labelText, type: "ariaRadio" });
  });

  // Checkboxes: one entry per checkbox (not grouped by name)
  document.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
    const labelText = getLabelForInput(checkbox);
    if (!labelText || seenLabels.has(labelText)) return;
    seenLabels.add(labelText);
    fields.push({ element: checkbox, question: labelText, type: "checkbox" });
  });

  return fields;
}

// ─── Fill ─────────────────────────────────────────────────────────────────────

function fillField(field, answerText) {
  if (field.type === "radio") {
    // Leave radio group untouched when answer is N/A
    if (answerText === "N/A") return;
    const matched = field.allRadios.find(radio => {
      if (radio.value.toLowerCase() === answerText.toLowerCase()) return true;
      return getLabelForInput(radio).toLowerCase() === answerText.toLowerCase();
    });
    if (matched) {
      matched.checked = true;
      matched.dispatchEvent(new Event("change", { bubbles: true }));
    }
  } else if (field.type === "ariaRadio") {
    // Google Forms style: div[role="radio"] options with aria-label, clicked via .click()
    if (answerText === "N/A") return;
    const matched = field.allOptions.find(opt =>
      (opt.getAttribute("aria-label") || "").toLowerCase() === answerText.toLowerCase()
    );
    if (matched) matched.click();
  } else if (field.type === "checkbox") {
    const affirmative = ["yes", "true", "1", "checked"].includes(answerText.toLowerCase());
    field.element.checked = affirmative;
    field.element.dispatchEvent(new Event("change", { bubbles: true }));
  } else {
    field.element.value = answerText;
    field.element.dispatchEvent(new Event("input", { bubbles: true }));
    field.element.dispatchEvent(new Event("change", { bubbles: true }));
  }
}

// ─── Message Handler ──────────────────────────────────────────────────────────

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.type === "TRIGGER_AUTOFILL") {

    const fields = scrapeQuestions();
    if (fields.length === 0) {
      alert("No form questions found to auto-fill.");
      sendResponse({ success: false, error: "No questions found" });
      return true;
    }

    const questions = fields.map(f => f.question);

    chrome.storage.local.get(["resume_id", "job_id"], (data) => {
      if (!data.resume_id || !data.job_id) {
        alert("Missing resume_id or job_id. Please click 'Apply' from the job search app first.");
        sendResponse({ success: false, error: "Missing resume or job ID" });
        return;
      }

      const payload = {
        type: "GENERATE_ANSWERS",
        resume_id: data.resume_id,
        job_id: data.job_id,
        questions: questions
      };

      console.log("=== Job Autofiller API Request ===");
      console.log(JSON.stringify(payload, null, 2));

      chrome.runtime.sendMessage(payload, (response) => {
        console.log("=== Job Autofiller API Response ===");
        console.log(JSON.stringify(response, null, 2));

        if (response && response.success) {
          // Build O(1) lookup map; iterate fields (not answers) to ensure N/A fallback
          const answerMap = new Map(response.answers.map(a => [a.question, a.answer]));

          fields.forEach(field => {
            const answerText = answerMap.get(field.question) || "N/A";
            fillField(field, answerText);
          });

          sendResponse({ success: true });
        } else {
          alert("Error generating answers: " + (response ? response.error : "Unknown error"));
          sendResponse({ success: false, error: response ? response.error : "Unknown error" });
        }
      });
    });

    return true; // Keep channel open for async processing
  }
});
