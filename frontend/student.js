const API_URL = "http://127.0.0.1:8000/tickets";

const form = document.getElementById("ticket-form");
const button = document.getElementById("submit-btn");
const message = document.getElementById("message");

const requiredFields = ["student_name", "title", "description"];

function showMessage(text, type) {
  message.textContent = text;
  message.className = "message " + type;
}

function checkRequiredFields() {
  let allGood = true;

  requiredFields.forEach(function (id) {
    const input = document.getElementById(id);
    const error = document.getElementById(id + "-error");

    if (input.value.trim() === "") {
      input.classList.add("invalid");
      error.textContent = "This field is required.";
      allGood = false;
    } else {
      input.classList.remove("invalid");
      error.textContent = "";
    }
  });

  return allGood;
}

form.addEventListener("submit", async function (event) {
  event.preventDefault();
  message.className = "message hidden";

  if (!checkRequiredFields()) {
    return;
  }

  const ticket = {
    student_name: document.getElementById("student_name").value.trim(),
    title: document.getElementById("title").value.trim(),
    category: document.getElementById("category").value,
    description: document.getElementById("description").value.trim()
  };

  button.disabled = true;
  button.textContent = "Sending...";

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(ticket)
    });

    if (!response.ok) {
      throw new Error("Server answered with status " + response.status);
    }

    const saved = await response.json();
    showMessage("Thanks " + saved.student_name + "! Your ticket #" + saved.id + " was submitted. Status: " + saved.status + ".", "success");
    form.reset();
  } catch (error) {
    showMessage("Sorry, we couldn't send your ticket. Make sure the server is running and try again.", "failure");
  } finally {
    button.disabled = false;
    button.textContent = "Submit ticket";
  }
});
