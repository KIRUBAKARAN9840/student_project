document.addEventListener("DOMContentLoaded", function () {
  const addBtn = document.getElementById("addBtn");
  const popup = document.getElementById("popupForm");
  const cancelBtn = document.getElementById("cancelBtn");
  const studentForm = document.getElementById("studentForm");
  const studentBody = document.getElementById("studentBody");

  let editingId = null;

  fetch('/students/get-students/')
    .then(res => res.json())
    .then(data => {
      data.forEach(student => appendRow(student));
    });

  addBtn.addEventListener("click", () => {
    popup.style.display = "block";
    studentForm.reset();
    editingId = null;
  });

  cancelBtn.addEventListener("click", () => {
    popup.style.display = "none";
  });

  studentForm.addEventListener("submit", function (e) {
    e.preventDefault();
    const name = document.getElementById("name").value;
    const subject = document.getElementById("subject").value;
    const mark = document.getElementById("mark").value;

    const payload = {
      id: editingId,
      name,
      subject,
      mark
    };

    fetch('/students/save-student/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCSRFToken() },
      body: JSON.stringify(payload)
    })
      .then(res => res.json())
      .then(() => location.reload());
  });

  window.editStudent = function (id) {
    fetch('/students/get-students/')
      .then(res => res.json())
      .then(data => {
        const student = data.find(s => s.id === id);
        if (student) {
          document.getElementById("name").value = student.name;
          document.getElementById("subject").value = student.subject;
          document.getElementById("mark").value = student.mark;
          editingId = student.id;
          popup.style.display = "block";
        }
      });
  };

  window.deleteStudent = function (id) {
    fetch('/students/delete-student/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCSRFToken() },
      body: JSON.stringify({ id })
    })
      .then(res => res.json())
      .then(() => location.reload());
  };

  function appendRow(student) {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${student.name}</td>
      <td>${student.subject}</td>
      <td>${student.mark}</td>
      <td>
        <button onclick="editStudent(${student.id})">Edit</button>
        <button onclick="deleteStudent(${student.id})">Delete</button>
      </td>
    `;
    studentBody.appendChild(row);
  }

  function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
  }
});
