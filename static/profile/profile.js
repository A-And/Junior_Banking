function dorpChange() {
    if (document.getElementById('drop').value == "Classic") {
        document.getElementById('content').style.background = "rgb(255,255,255)";
        document.getElementById('body').style.background = "rgb(11,140,82)";
        $("#name").css("color", "rgb(11,140,82)");
        $("#nav_bar").css("background-color", "rgb(11,140,82)");
        <!--		$("#nav_bar li a").css("color","rgb(11,140,82)");-->
        $(".edit").css("color", "rgb(11,140,82)");
        $(".edit").css("background-color", "rgb(208,206,206)");
        document.getElementById('backpicture').src = "../images/profile/kids.jpg";
    }

    if (document.getElementById('drop').value == "Star") {
        document.getElementById('content').style.background = "rgb(179,162,199)";
        document.getElementById('body').style.background = "rgb(96,74,123)";
        $("#name").css("color", "rgb(96,74,123)");
        $("#nav_bar").css("background-color", "rgb(96,74,123)");
        <!--		$("#nav_bar li a").css("color","rgb(255,255,255)");-->
        $(".edit").css("color", "rgb(255,255,255)");
        $(".edit").css("background-color", "rgb(127,127,127)");
        document.getElementById('backpicture').src = "../images/profile/star.jpg";
    }

    if (document.getElementById('drop').value == "Sky") {
        document.getElementById('content').style.background = "rgb(157,195,230)";
        document.getElementById('body').style.background = "rgb(0,204,255)";
        $("#name").css("color", "rgb(47,85,151)");
        $("#nav_bar").css("background-color", "rgb(47,85,151)");
        <!--		$("#nav_bar li a").css("color","rgb(255,255,255)");-->
        $(".edit").css("color", "rgb(255,255,255)");
        $(".edit").css("background-color", "rgb(47,85,151)");
        document.getElementById('backpicture').src = "../images/profile/sky.jpg";
    }

    if (document.getElementById('drop').value == "Fish") {
        document.getElementById('content').style.background = "rgb(142,180,227)";
        document.getElementById('body').style.background = "rgb(23,55,94)";
        $("#name").css("color", "rgb(0,112,192)");
        $("#nav_bar").css("background-color", "rgb(23,55,94)");
        <!--		$("#nav_bar li a").css("color","rgb(255,255,255)");-->
        $(".edit").css("color", "rgb(255,255,255)");
        $(".edit").css("background-color", "rgb(0,112,192)");
        document.getElementById('backpicture').src = "../images/profile/fish.jpg";
    }

    if (document.getElementById('drop').value == "Marvel") {
        document.getElementById('content').style.background = "rgb(244,177,131)";
        document.getElementById('body').style.background = "rgb(0,0,0)";
        $("#name").css("color", "rgb(192,0,0)");
        $("#nav_bar").css("background-color", "rgb(192,0,0)");
        <!--		$("#nav_bar li a").css("color","rgb(255,255,255)");-->
        $(".edit").css("color", "rgb(255,255,255)");
        $(".edit").css("background-color", "rgb(192,0,0)");
        document.getElementById('backpicture').src = "../images/profile/marvel.jpg";
    }
}
function changeProfile() {
    $('#myModal').modal('hide');
    $('#myModal').modal('show');
    $('#accountNumber').val("");
    $('#address').val("");
    $('#dob').val("");
    $('#email').val("");
    $('#parentName').val("");
    $('#parentNumber').val("");
    $('#branch').val("");
}

function selectDate() {
    $('.datepicker').datepicker();
}
function save() {

    $('#myModal').modal('hide');
    $('#outAccountNumber').val($('#accountNumber').val());
    $('#outAddress').val($('#address').val());
    $('#outDob').val($('#dob').val());
    $('#outEmail').val($('#email').val());
    $('#outParentName').val($('#parentName').val());
    $('#outParentNumber').val($('#parentNumber').val());
    $('#outBranch').val($('#branch').val());
}

function validator2() {
    var accountNumberP = /^[a-z0-9_-]{8,8}$/;
    var emailP = /^[\w]+([\.\w-]*)?@[\w]+(\.[\w-]+)*(\.[a-z]{2,3})(\.[a-z]{2,3})*?$/i;
    var parentNameP = /^[a-z0-9_-]{3,30}$/;
    var parentNumberP = /^[0-9]{3,20}$/;
    flag = true;
    if ($('#accountNumber').val() == "" || null || accountNumberP.test($('#accountNumber').val()) == false) {
        flag = false;
        $('#accountNumber').css("border-color", "red");
    }
    else {
        $('#accountNumber').css("border-color", "black");
    }

    if ($('#address').val() == "" || null) {
        flag = false;
        $('#address').css("border-color", "red");
    }
    else {
        $('#address').css("border-color", "black");
    }

    if ($('#dob').val() == "" || null) {
        flag = false;
        $('#dob').css("border-color", "red");
    }
    else {
        $('#dob').css("border-color", "black");
    }

    if ($('#email').val() == "" || null || emailP.test($('#email').val()) == false) {
        flag = false;
        $('#email').css("border-color", "red");
    }
    else {
        $('#email').css("border-color", "black");
    }

    if ($('#parentName').val() == "" || null || parentNameP.test($('#parentName').val()) == false) {
        flag = false;
        $('#parentName').css("border-color", "red");
    }
    else {
        $('#parentName').css("border-color", "black");
    }

    if ($('#parentNumber').val() == "" || null || parentNumberP.test($('#parentNumber').val()) == false) {
        flag = false;
        $('#parentNumber').css("border-color", "red");
    }
    else {
        $('#parentNumber').css("border-color", "black");
    }

    if ($('#branch').val() == "" || null) {
        flag = false;
        $('#branch').css("border-color", "red");
    }
    else {
        $('#branch').css("border-color", "black");
    }

    if (flag == true)
        save();

}