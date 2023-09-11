<?php
// Get the values of the input fields from the $_POST array
$num1 = $_POST["num1"];
$num2 = $_POST["num2"];

// Add the two numbers together and store the result in another variable
$result = $num1 + $num2;

// Display the input values and the result on the web page with some HTML tags and attributes
echo "<html>";
echo "<head>";
echo "<title>Number Adder</title>";
echo "<link rel='stylesheet' href='style.css'>";
echo "</head>";
echo "<body>";
echo "<h1>Number Adder</h1>";
echo "<p>You entered:</p>";
echo "<p>First number: <span>$num1</span></p>";
echo "<p>Second number: <span>$num2</span></p>";
echo "<p>The result of adding them together is: <span>$result</span></p>";
echo "</body>";
echo "</html>";
?>
