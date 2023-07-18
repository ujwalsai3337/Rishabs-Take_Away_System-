// Login Form Submit Handler
document.getElementById("loginForm").addEventListener("submit", function(event) {
    event.preventDefault();
    
    // Get the form values
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    
    // Perform login logic (e.g., validate credentials with API)
    // You can make an AJAX request to the Flask API here
    
    // Reset the form
    this.reset();
  });
  
  // Sign Up Form Submit Handler
  document.getElementById("signupForm").addEventListener("submit", function(event) {
    event.preventDefault();
    
    // Get the form values
    var username = document.getElementById("username").value;
    var email = document.getElementById("email").value;
    var password = document.getElementById("password").value;
    var confirmPassword = document.getElementById("confirmPassword").value;
    
    // Perform sign up logic (e.g., send data to the Flask API)
    // You can make an AJAX request to the Flask API here
    
    // Reset the form
    this.reset();
  });
  
  // Forget Password Form Submit Handler
  document.getElementById("forgetPasswordForm").addEventListener("submit", function(event) {
    event.preventDefault();
    
    // Get the form values
    var email = document.getElementById("email").value;
    
    // Perform forget password logic (e.g., send email to reset password)
    // You can make an AJAX request to the Flask API here
    
    // Reset the form
    this.reset();
  });
  