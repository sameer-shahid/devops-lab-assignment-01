// ==========================================================================
// Cloud Web Application - Frontend Form Validation & Dynamic Updates
// ==========================================================================

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('registrationForm');
  const btnClear = document.getElementById('btnClear');
  const alertSuccess = document.getElementById('alertSuccess');
  const alertError = document.getElementById('alertError');
  const studentsTableBody = document.getElementById('studentsTableBody');
  const totalStudentsCount = document.getElementById('totalStudentsCount');

  if (form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();

      // Hide previous alerts
      hideAlert(alertSuccess);
      hideAlert(alertError);

      const fullName = document.getElementById('fullName').value.trim();
      const studentEmail = document.getElementById('studentEmail').value.trim();
      const rollNumber = document.getElementById('rollNumber').value.trim();
      const ageInput = document.getElementById('age').value.trim();
      const password = document.getElementById('password').value;
      const department = document.getElementById('department').value;

      // 1. Mandatory Validation: Empty-field validation (text inputs)
      if (!fullName || !studentEmail || !rollNumber || !ageInput || !password) {
        showError("Validation Error: All fields are mandatory. Please fill in all required fields.");
        return;
      }

      // 2. Mandatory Validation: Required dropdown selection
      if (!department || department === "default" || department === "") {
        showError("Validation Error: Please select a valid academic department from the dropdown list.");
        return;
      }

      // 2. Mandatory Validation: Invalid email validation
      const emailRegex = /^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$/;
      if (!emailRegex.test(studentEmail)) {
        showError("Validation Error: Please enter a valid email address (e.g. name@cuilahore.edu.pk).");
        return;
      }

      // 3. Mandatory Validation: Password-length validation (at least 8 chars)
      if (password.length < 8) {
        showError("Validation Error: Password must be at least 8 characters long.");
        return;
      }

      // 4. Mandatory Validation: Invalid numeric input (Age between 16 and 60)
      const age = Number(ageInput);
      if (isNaN(age) || !Number.isInteger(age) || age < 16 || age > 60) {
        showError("Validation Error: Age must be a valid whole number between 16 and 60.");
        return;
      }

      // 5. Mandatory Validation: Required dropdown selection
      if (!department || department === "default" || department === "") {
        showError("Validation Error: Please select a valid academic department from the dropdown list.");
        return;
      }

      // Form payload
      const payload = {
        fullName,
        studentEmail,
        rollNumber,
        age,
        password,
        department
      };

      try {
        const response = await fetch('/api/register', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(payload)
        });

        const result = await response.json();

        if (response.ok && result.success) {
          showSuccess(result.message || "Student registered successfully!");
          
          // Append student to records table
          appendStudentRecord(result.student);
          
          // Update stats counter
          if (totalStudentsCount && result.total) {
            totalStudentsCount.textContent = result.total;
          }

          // Clear the form
          form.reset();
        } else {
          showError(result.message || "Failed to register student.");
        }
      } catch (err) {
        showError("Network Error: Could not connect to the server. Please check your cloud connection.");
      }
    });
  }

  // Clear button logic
  if (btnClear && form) {
    btnClear.addEventListener('click', () => {
      form.reset();
      hideAlert(alertSuccess);
      hideAlert(alertError);
    });
  }

  function showError(msg) {
    if (alertError) {
      alertError.textContent = msg;
      alertError.classList.remove('hidden');
    }
  }

  function showSuccess(msg) {
    if (alertSuccess) {
      alertSuccess.textContent = msg;
      alertSuccess.classList.remove('hidden');
    }
  }

  function hideAlert(el) {
    if (el) {
      el.classList.add('hidden');
      el.textContent = '';
    }
  }

  function appendStudentRecord(student) {
    if (!studentsTableBody) return;
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td><strong>${escapeHtml(student.fullName)}</strong></td>
      <td>${escapeHtml(student.rollNumber)}</td>
      <td>${escapeHtml(student.studentEmail)}</td>
      <td><span class="badge-dept">${escapeHtml(student.department)}</span></td>
      <td>${escapeHtml(String(student.age))}</td>
    `;
    studentsTableBody.appendChild(tr);
  }

  function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }
});
