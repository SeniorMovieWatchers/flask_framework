$("#search").click(function() {
    var new_data = {
        keyword: $("#search_text").val()
    };
    
    $.ajax({
            url: 'http://fa16-cs411-50.cs.illinois.edu:5000/search-movie',
            dataType: 'JSON',
            type: 'POST',
            contentType: 'application/json; charset=utf-8',
            success: function(result) {
                console.log(result);
            },
            data: JSON.stringify(new_data)
        });
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
