function validate() {
    var thisForm = document.forms[0];
    var emailP = /^[\w]+([\.\w-]*)?@[\w]+(\.[\w-]+)*(\.[a-z]{2,3})(\.[a-z]{2,3})*?$/i;
    if (thisForm.Account_Number.value == "") {
        alert("Please fill in your account number.");
        return false;
    }
    if (thisForm.Parent_Name.value == "") {
        alert("Please fill in your parent or guardian name.");
        return false;
    }
    if (thisForm.Address.value == "") {
        alert("Please fill in your address.");
        return false;
    }
    if (thisForm.Parent_Number.value == "") {
        alert("Please fill in your parent or guardian contact number.");
        return false;
    }
    if (thisForm.DOB.value == "") {
        alert("Please fill your date of birth.");
        return false;
    }
    if (thisForm.E - mail.value == "") {
        alert("Please fill your E-mail address.");
        return false;
    }
    if (!emailP.test(thisForm.E - mail.value)) {
        alert("Please fill your E-mail address correctly.");
        return false;
    }
    if (thisForm.Brach.value == "") {
        alert("Please fill your local Lloyds brach");
        return false;
    }
}

function dorpChange() {
    if (document.getElementById('drop').value == "Classic") {
        document.getElementById('content').style.background = "rgb(255,255,255)";
        document.getElementById('body').style.background = "rgb(11,140,82)";
        document.getElementById('bottom_bar').style.background = "rgb(208,206,206)";
        $("#name").css("color", "rgb(11,140,82)");
        $("#nav_bar li a").css("color", "rgb(11,140,82)");
        $(".edit").css("color", "rgb(11,140,82)");
        $(".edit").css("background-color", "rgb(208,206,206)");
        $(".change_color").css("color", "rgb(11,140,82)");
        $(".change_color").css("background-color", "rgb(208,206,206)");
        document.getElementById('backpicture').src = "../images/profile/kids.png";
    }

    if (document.getElementById('drop').value == "Star") {
        document.getElementById('content').style.background = "rgb(179,162,199)";
        document.getElementById('body').style.background = "rgb(96,74,123)";
        document.getElementById('bottom_bar').style.background = "rgb(179,162,199)";
        $("#name").css("color", "rgb(96,74,123)");
        $("#nav_bar li a").css("color", "rgb(255,255,255)");
        $(".edit").css("color", "rgb(255,255,255)");
        $(".edit").css("background-color", "rgb(127,127,127)");
        $(".change_color").css("color", "rgb(255,255,255)");
        $(".change_color").css("background-color", "rgb(127,127,127)");
        document.getElementById('backpicture').src = "../images/profile/star.jpg";
    }

    if (document.getElementById('drop').value == "Sky") {
        document.getElementById('content').style.background = "rgb(157,195,230)";
        document.getElementById('body').style.background = "rgb(0,204,255)";
        document.getElementById('bottom_bar').style.background = "rgb(183,222,232)";
        $("#name").css("color", "rgb(47,85,151)");
        $("#nav_bar li a").css("color", "rgb(255,255,255)");
        $(".edit").css("color", "rgb(255,255,255)");
        $(".edit").css("background-color", "rgb(47,85,151)");
        $(".change_color").css("color", "rgb(255,255,255)");
        $(".change_color").css("background-color", "rgb(47,85,151)");
        document.getElementById('backpicture').src = "../images/profile/sky.jpg";
    }

    if (document.getElementById('drop').value == "Fish") {
        document.getElementById('content').style.background = "rgb(142,180,227)";
        document.getElementById('body').style.background = "rgb(23,55,94)";
        document.getElementById('bottom_bar').style.background = "rgb(142,180,227)";
        $("#name").css("color", "rgb(0,112,192)");
        $("#nav_bar li a").css("color", "rgb(255,255,255)");
        $(".edit").css("color", "rgb(255,255,255)");
        $(".edit").css("background-color", "rgb(0,112,192)");
        $(".change_color").css("color", "rgb(255,255,255)");
        $(".change_color").css("background-color", "rgb(0,112,192)");
        document.getElementById('backpicture').src = "../images/profile/fish.jpg";
    }

    if (document.getElementById('drop').value == "Marvel") {
        document.getElementById('content').style.background = "rgb(244,177,131)";
        document.getElementById('body').style.background = "rgb(0,0,0)";
        document.getElementById('bottom_bar').style.background = "rgb(244,177,131)";
        $("#name").css("color", "rgb(192,0,0)");
        $("#nav_bar li a").css("color", "rgb(255,255,255)");
        $(".edit").css("color", "rgb(255,255,255)");
        $(".edit").css("background-color", "rgb(192,0,0)");
        $(".change_color").css("color", "rgb(255,255,255)");
        $(".change_color").css("background-color", "rgb(192,0,0)");
        document.getElementById('backpicture').src = "../images/profile/marvel.jpg";
    }
}
function changeProfile() {
    $('#myModal').modal('show');
}

function selectDate() {
    $('.datepicker').datepicker();
}
