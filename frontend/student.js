const form = document.getElementById("ticket-form");
const message = document.getElementById("message");

form.addEventListener("submit", async function (event) {
  event.preventDefault();

  const name = document.getElementById("student_name").value.trim();
  const title = document.getElementById("title").value.trim();
  const category = document.getElementById("category").value;
  const description = document.getElementById("description").value.trim();

  if (name === "" || title === "" || description === "") {
    message.textContent = "Please fill in all the required fields.";
    message.className = "error";
    return;
  }

  const ticket = {
    student_name: name,
    title: title,
    category: category,
    description: description
  };

  try {
    const response = await fetch("http://127.0.0.1:8000/tickets", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(ticket)
    });

    if (response.ok) {
      const saved = await response.json();
      message.textContent = "Your ticket #" + saved.id + " was submitted successfully!";
      message.className = "success";
      form.reset();
    } else {
      message.textContent = "Something went wrong. Please try again.";
      message.className = "error";
    }
  } catch (error) {
    message.textContent = "Can't reach the server. Make sure it is running.";
    message.className = "error";
  }
});
