function isEmail(email) {
    var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    return regex.test(email);
}

$("#signup").click(function(){
    $("#signup-jumbotron").css("display", "block");
});

$("#edit-account").click(function() {
    $("#update-jumbotron").css("display", "block");
});

$("#logout").click(function() {
    $("#login-button").css("display", "block");
    $("#signup").css("display", "block");
    $("#email-text").css("display", "block");
    $("#password-text").css("display", "block");
    $("#logout").css("display", "none");
    $("#edit-account").css("display", "none");
});

$("#search-user").click(function() {
    var new_data = {
            username : $("#user").val()
        };

        $.ajax({
            url: 'http://fa16-cs411-50.cs.illinois.edu/home/search-user-username',
            dataType: 'JSON',
            type: 'POST',
            contentType: 'application/json; charset=utf-8',
            success: function(result){
                $("#table-content").html('');
                $("#query-executed").html(result['query']);
                user_list = result['user_list'];
                var index;
                for (index = 0; index < user_list.length; index++) {
                    var user = user_list[index];
                    var result = "<tr>";
                    result += "<td>" + user['id'] + "</td>";
                    result += "<td>" + user['username'] + "</td>"
                    result += "<td>" + user['email'] +"</td>";
                    $( "#table-content" ).append(result);
                }
            },
            data: JSON.stringify(new_data)
        });
});

$("#search-user-email").click(function() {
    var new_data = {
            email : $("#user-email").val()
        };

        $.ajax({
            url: 'http://fa16-cs411-50.cs.illinois.edu/home/search-user-email',
            dataType: 'JSON',
            type: 'POST',
            contentType: 'application/json; charset=utf-8',
            success: function(result){
                $("#table-content").html('');
                $("#query-executed").html(result['query']);
                user_list = result['user_list'];
                var index;
                for (index = 0; index < user_list.length; index++) {
                    var user = user_list[index];
                    var result = "<tr>";
                    result += "<td>" + user['id'] + "</td>";
                    result += "<td>" + user['username'] + "</td>"
                    result += "<td>" + user['email'] +"</td>";
                    $("#table-content").append(result);
                }
            },
            data: JSON.stringify(new_data)
        });
});

$("#duplicate-email").click(function() {
    $.ajax({
        url: 'http://fa16-cs411-50.cs.illinois.edu/home/duplicate-email',
        dataType: 'JSON',
        type: 'GET',
        contentType: 'application/json; charset=utf-8',
        success: function(result){
            $("#table-content").html('');
            $("#query-executed").html(result['query']);
            user_list = result['user_list'];
            var index;
            for (index = 0; index < user_list.length; index++) {
                var user = user_list[index];
                var result = "<tr>";
                result += "<td>" + user['id'] + "</td>";
                result += "<td>" + user['username'] + "</td>"
                result += "<td>" + user['email'] +"</td>";
                $("#table-content").append(result);
            }
        }
    });
});


    $("#submit-signup").click(function() {
    var new_data = {
            username : $("#name").val(),
            email : $("#email").val(),
            password : $("#password").val()
        };

        $.ajax({
            url: 'http://fa16-cs411-50.cs.illinois.edu/home/new-user',
            dataType: 'JSON',
            type: 'POST',
            contentType: 'application/json; charset=utf-8',
            success: function(result){
                $("#query-executed").html(result['query']);
            },
            data: JSON.stringify(new_data)
        });
});

$("#submit-update").click(function(){

    var errorMessage = "";
    var fieldMissing = "";

    if($("#email").val() == ""){

        fieldMissing += "Email\n"

    }

    if($("#name").val() == ""){

        fieldMissing += "Name\n"

    }

    if(fieldMissing != ""){

        errorMessage += "The following field(s) are missing:" + fieldMissing;

    }

    if(isEmail($("#email").val()) == false){

        errorMessage += "Email is invalid\n";

    }

    if(errorMessage != ""){

        alert(errorMessage);

    }else{

        /*var new_data = {
            name : $("#name").val(),
            email : $("#email").val(),
            password : $("#password").val();
        };

        $.ajax({
            url: '/new-update',
            dataType: 'JSON',
            type: 'POST',
            contentType: 'application/json; charset=utf-8',
            success: function(result){
                console.log(result)
            },
            data: JSON.stringify(new_data);
        });*/

        $("#update-jumbotron").css("display", "none");
        $("#login-button").css("display", "none");
        $("#signup").css("display", "none");
        $("#email-text").css("display", "none");
        $("#password-text").css("display", "none");
        $("#edit-account").css("display", "block");
        $("#logout").css("display", "block");

    } 

});

$("#submit-signup").click(function(){

    var errorMessage = "";
    var fieldMissing = "";

    if($("#email").val() == ""){

        fieldMissing += "Email\n"

    }

    if($("#name").val() == ""){

        fieldMissing += "Name\n"

    }

    if($("#password").val() == ""){

        fieldMissing += "Password\n"

    }

    if($("#passwordConfirm").val() == ""){

        fieldMissing += "Confirm Password\n"

    }

    if(fieldMissing != ""){

        errorMessage += "The following field(s) are missing:" + fieldMissing;

    }

    if(isEmail($("#email").val()) == false){

        errorMessage += "Email is invalid\n";

    }

    if($("#password").val() != $("#passwordConfirm").val()){

        errorMessage += "Passwords don't match";

    }

    if(errorMessage != ""){

        alert(errorMessage);

    }else{

        /*var new_data = {
            name : $("#name").val(),
            email : $("#email").val(),
            password : $("#password").val();
        };

        $.ajax({
            url: '/new-user',
            dataType: 'JSON',
            type: 'POST',
            contentType: 'application/json; charset=utf-8',
            success: function(result){
                console.log(result)
            },
            data: JSON.stringify(new_data);
        });*/

        $("#signup-jumbotron").css("display", "none");
        $("#login-button").css("display", "none");
        $("#signup").css("display", "none");
        $("#email-text").css("display", "none");
        $("#password-text").css("display", "none");
        $("#edit-account").css("display", "block");
        $("#logout").css("display", "block");

    } 

});
