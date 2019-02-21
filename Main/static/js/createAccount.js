function badOverall() {
    var errorOverallMessage = document.getElementById("errorOverall");
    var errorBool = false;

    //Check First Name Field
    var firstNameText = document.getElementById("firstNameText");
    var firstNameInput = document.forms["inputs"]["firstNameInput"].value;

    if (firstNameInput == "") {
        errorBool = true;
        firstNameText.style.color = "red";
    } else {
        firstNameText.style.color = "black";
    }

    //Check Last Name Field
    var lastNameText = document.getElementById("lastNameText");
    var lastNameInput = document.forms["inputs"]["lastNameInput"].value;

    if (lastNameInput == "") {
        errorBool = true;
        lastNameText.style.color = "red";
    } else {
        lastNameText.style.color = "black";
    }

    //Check Age Field
    var ageText = document.getElementById("ageText");
    var ageInput = document.forms["inputs"]["ageInput"].value;

    if (ageInput == "" || ageInput < 0)  {
        errorBool = true;
        ageText.style.color = "red";
    } else {
        ageText.style.color = "black";
    }

    //Check Email Field
    var emailText = document.getElementById("emailText");
    var emailInput = document.forms["inputs"]["emailInput"].value;

    if (emailInput == "" || emailInput == "bad") {
        errorBool = true;
        emailText.style.color = "red";
    } else {
        emailText.style.color = "black";
    }

    //Check Password Field
    var passwordText = document.getElementById("passwordText");
    var passwordInput = document.forms["inputs"]["passwordInput"].value;

    if (passwordInput == "") {
        errorBool = true;
        passwordText.style.color = "red";
    } else {
        passwordText.style.color = "black";
    }

    //Check Password Check Field
    var passwordCheckText = document.getElementById("passwordCheckText");
    var passwordCheckInput = document.forms["inputs"]["passwordCheckInput"].value;

    if (passwordCheckInput == "") {
        errorBool = true;
        passwordCheckText.style.color = "red";
    } else {
        passwordCheckText.style.color = "black";
    }

    //Make Sure Passwords Match
    var errorPassword = document.getElementById("errorPassword");

    if (passwordInput !== passwordCheckInput) {
        errorBool = true;
        passwordText.style.color = "red";
        passwordCheckText.style.color = "red";
        errorPassword.style.display = "block";
    } else {
        errorPassword.style.display = "none";
    }

    if (errorBool) {
        errorOverallMessage.style.display = "block";
    } else {
        errorOverallMessage.style.display = "none";
        window.location.href="/home";
    }
}
