// Get a reference to the submit button element
var submitButton = document.getElementById("submit");

// Define a function to validate the input fields
function validateInput() {
  // Get a reference to the input field elements
  var num1 = document.getElementById("num1");
  var num2 = document.getElementById("num2");

  // Check if the input fields are empty or not
  if (num1.value == "" || num2.value == "") {
    // Alert the user that they need to enter two numbers
    alert("Please enter two numbers.");
    // Prevent the form from being submitted
    return false;
  }

  // Check if the input fields are valid numbers or not
  if (isNaN(num1.value) || isNaN(num2.value)) {
    // Alert the user that they need to enter valid numbers
    alert("Please enter valid numbers.");
    // Prevent the form from being submitted
    return false;
  }

  // If everything is OK, allow the form to be submitted
  return true;
}

// Attach the function to the click event of the submit button element
submitButton.addEventListener("click", validateInput);
