// Function to handle form submission and AJAX request
function handleFormSubmit(formId, url, requestData) {
  var form = document.getElementById(formId);
  
  form.addEventListener("submit", function(event) {
    event.preventDefault();
    
    // Collect form data
    var formData = {};
    var formElements = form.elements;
    for (var i = 0; i < formElements.length; i++) {
      var element = formElements[i];
      if (element.tagName === "INPUT") {
        formData[element.id] = element.value;
      }
    }
    
    // Perform AJAX request
    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(formData),
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      console.log('Success:', data);
      // Handle success scenario (e.g., show success message)
      form.reset(); // Reset form after successful submission
    })
    .catch(error => {
      console.error('Error:', error);
      // Handle error scenario (e.g., show error message)
    });
  });
}

// Attach handlers for each form
handleFormSubmit("loginForm", "/login", {});
handleFormSubmit("signupForm", "/signup", {});
handleFormSubmit("forgetPasswordForm", "/forget-password", {});
