var toggle_button = document.querySelector(".form-group .password_toggler")
var toggle_button_2 = document.querySelector(".form-group .password_toggler_reg")
var toggle_button_3 = document.querySelector(".form-group .password_toggler_2")

//code for toggling password being shown on/off
if (toggle_button) {

    toggle_button.addEventListener("click", toggle_on_off)
        //toggle_button2.addEventListener("click", toggle_on_off(".form-group", ".password_toggler_reg"))
    function toggle_on_off() {
        let el = toggle_button;
        if (el.classList.contains("active")) {
            console.log("Hide password clicked")
            document.getElementById('password_sign_in').setAttribute("type", "password")
            el.classList.remove("active") //remove a class list from the element (.form-group .password_toggler)
        } else {
            console.log("Show password clicked")
            document.getElementById('password_sign_in').setAttribute("type", "text")
                // document.querySelector(".form-group #password_sign_in").setAttribute("type", "text")
            el.classList.add("active") //creating a class list for the element (.form-group .password_toggler)
        }
    }
}

toggle_button_2.addEventListener("click", function() {

    let el = toggle_button_2;
    if (el.classList.contains("active1")) {
        console.log("Hide password clicked")
        document.querySelector(".form-group #password").setAttribute("type", "password")
        el.classList.remove("active1") //remove a class list from the element (.form-group .password_toggler)
    } else {
        console.log("Show password clicked")
        document.querySelector(".form-group #password").setAttribute("type", "text")
        el.classList.add("active1") //creating a class list for the element (.form-group .password_toggler)
    }
});


toggle_button_3.addEventListener("click", toggle_on_off)
    //toggle_button2.addEventListener("click", toggle_on_off(".form-group", ".password_toggler_reg"))
function toggle_on_off() {
    let el = toggle_button_3;
    if (el.classList.contains("active")) {
        console.log("Hide password clicked")
        document.getElementById('password2').setAttribute("type", "password")
        el.classList.remove("active") //remove a class list from the element (.form-group .password_toggler)
    } else {
        console.log("Show password clicked")
        document.getElementById('password2').setAttribute("type", "text")

        // document.querySelector(".form-group #password_sign_in").setAttribute("type", "text")
        el.classList.add("active") //creating a class list for the element (.form-group .password_toggler)
    }

}

//function for getting passwordStrength
function getPasswordStrength(password) {
    toggle_button_3.addEventListener("click", toggle_on_off)
        //toggle_button2.addEventListener("click", toggle_on_off(".form-group", ".password_toggler_reg"))
    function toggle_on_off() {
        let el = toggle_button_3;
        if (el.classList.contains("active")) {
            console.log("Hide password clicked")
            document.getElementById('password2').setAttribute("type", "password")
            el.classList.remove("active") //remove a class list from the element (.form-group .password_toggler)
        } else {
            console.log("Show password clicked")
            document.getElementById('password2').setAttribute("type", "text")

            // document.querySelector(".form-group #password_sign_in").setAttribute("type", "text")
            el.classList.add("active") //creating a class list for the element (.form-group .password_toggler)
        }
    }
}


//function for getting passwordStrength
function getPasswordStrength(password) {
    let s = 0;

    if (password.length == 0) {
        s = 0;
    }
    if (password.length > 4) {
        s++;
    }

    if (password.length > 6) {
        s++;
    }

    if (/[A-Z]/.test(password)) { //testing for capital letters
        s++;
    }
    if (/[0-9]/.test(password)) { //testing for numbers 0-9
        s++;
    }

    if (/[^A-Za-z0-9]/.test(password)) {
        s++;
    }

    return s;
}


//code for displaying strength meter
var sign_up_password_box = document.querySelector(".form-group #password")
var sign_up_password_box_2 = document.querySelector(".form-group #password2")

if (sign_up_password_box) {
    sign_up_password_box.addEventListener("click", function() { //focus concentrates on whether or not
        console.log("are you even working // FOCUSING ON PASSWORD BOX")
        document.querySelector(".form-group .password_strength").style.display = "block";
        //document.querySelector(".form-group .password_strength").height = "0px";
    });
} else {
    console.log(".form_group #password NOT FOUND")
}


if (sign_up_password_box) {

    sign_up_password_box.addEventListener("keyup", function(e) { //keyup = keys being pressed
        let password = e.target.value;
        let strength = getPasswordStrength(password)
        let passwordStrengthSpan = document.querySelectorAll(".form-group .password_strength span")
        strength2 = Math.max(strength, 1)
        passwordStrengthSpan[1].style.width = strength * 20 + "%";

        if (strength == 0) {
            passwordStrengthSpan[0].innerText = "Strength: Neutral";
            passwordStrengthSpan[1].style.color = "#111";
            passwordStrengthSpan[1].style.background = "#d13636";
            document.querySelector('.btn').style.display = "none";
        } else if (strength2 > 0 && strength2 < 2) {
            passwordStrengthSpan[0].innerText = "Strength: Weak";
            passwordStrengthSpan[1].style.color = "#111";
            passwordStrengthSpan[1].style.background = "#d13636";
            document.querySelector('.btn').style.display = "none";
        } else if (strength2 >= 2 && strength2 <= 4) {

            passwordStrengthSpan[0].innerText = "Strength: Medium";
            passwordStrengthSpan[1].style.color = "#111";
            passwordStrengthSpan[1].style.background = "#ffff00";
            document.querySelector('.btn').style.display = "none";

        } else {
            passwordStrengthSpan[0].innerText = "Strength: Strong";
            passwordStrengthSpan[1].style.color = "#111";
            passwordStrengthSpan[1].style.background = "#008000";
            document.querySelector('.btn').style.display = "block";

        }
    });
}



//code for showing password strength tip
if (sign_up_password_box) {

    sign_up_password_box.addEventListener("mouseenter", function() {
        console.log("mouse hovered over password_box")
        document.querySelector(".strong_password_tip").style.display = "block"; //get the class for to display the password tip content

    });

    sign_up_password_box.addEventListener("mouseleave", function() {
        console.log("mouse moved away from password_box")
        document.querySelector(".strong_password_tip").style.display = "none"; //get the class for to display the password tip content

    });

}
//code for confirming two passwords are equal to each other
//document.querySelector(".form-group #password").addEventListener("mouseout", get_password);


sign_up_password_box.addEventListener("keyup", check_for_similar_passwords)
sign_up_password_box_2.addEventListener("keyup", check_for_similar_passwords)

function check_for_similar_passwords() {

    const password1 = document.getElementById('password').value
    const password2 = document.getElementById('password2').value
    console.log("password1:", password1, "password2:", password2)

    if (password1 == password2) {
        console.log("passwords are equal to each other")
            //disable the warning: ..... element
        document.querySelector('.confirm_password').style.display = "none";
        //document.querySelector(".form-group .password_strength").style.display = "none";
        document.querySelector('.btn').disabled = false;
        document.querySelector('.btn').style.display = "block";

    } else {
        console.log("Please make sure your passwords equal each other")
            //enable the warning: ..element
        document.querySelector('.confirm_password').style.display = "block";
        document.querySelector('.confirm_password').style.color = "red";
        document.querySelector('.btn').disabled = true;

        if (document.querySelector('.btn').disabled == true) {
            document.querySelector('.btn').style.display = "none";

            //aa
            //console.log(";p;")
            //document.querySelector('.btn').addEventListener("mouseover", displayError)

            //function displayError() {
            //  console.log("lol bro")
            //}
        }
    }
}


//code for validating email

var email_box = document.querySelector(".form-group #email")
if (email_box) {
    email_box.addEventListener("keyup", function(e) {
        const email_content = document.getElementById('email').value

        if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(email_content)) {
            document.querySelector(".email_validator_text").style.display = "none";
            document.querySelector('.btn').style.display = "block";
            console.log("valid email address")
        } else {
            console.log("invalid email address")
            document.querySelector(".email_validator_text").style.display = "block";
            document.querySelector('.btn').style.display = "none";
        }
        console.log(email_content)
    });

}


var sign_up_password_box = document.querySelector(".form-group #password");