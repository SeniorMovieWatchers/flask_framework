$("#search-movie").click(function() {
    var new_data = {
        keyword: $("#search-text").val()
    };
    
    $.ajax({
            url: 'http://fa16-cs411-50.cs.illinois.edu/home/search-movie',
            dataType: 'JSON',
            type: 'POST',
            contentType: 'application/json; charset=utf-8',
            success: function(result) {
                
                var auth2 = gapi.auth2.getAuthInstance();
                if (auth2.isSignedIn.get()) {
                    $("#recomendations-jumbotron").css("display", "block");    
                }
                
                movie_list = result['movie_list'];
                var i;
                for(i = 1; i <= movie_list.length; i++){
                    var movieid = "movie-" + i;
                    var imageid = "img-" + i;
                    var titleid = "movie-title-" + i;
                    var ratingid = "rating-" + i;
                    var plotid = "movie-plot-" + i;
                    var actorsid = "actors-" + i;
                    $("#"+movieid).css("display", "block");
                    $("#"+movieid).data("movie-db-id", movie_list[i-1]['id']);
                    $("#"+imageid).attr("src", movie_list[i-1]['url']);
                    $("#"+titleid).text(movie_list[i-1]['title']);
                    $("#"+ratingid).text(movie_list[i-1]['rating']);
                    $("#"+plotid).text(movie_list[i-1]['plot']);
                    $("#"+actorsid).text(movie_list[i-1]['casts']);
                }
                var j;
                for(j = movie_list.length; j <= 5; j++){
                    var movieid = "movie-" + i;
                    $("#"+movieid).css("display", "none");
                }
            },
            data: JSON.stringify(new_data)
        });
});

function addFavs(i){
 
    $("#favorite-btn-"+i).click(function(){ 
        $("#favorite-btn-"+i).addClass("disabled");
    });
    
    var movieid = $("#movie-"+i).data("movie-db-id");
    var auth2 = gapi.auth2.getAuthInstance();
    if (auth2.isSignedIn.get()) {
        
        var profile = auth2.currentUser.get().getBasicProfile();
        var userid = profile.getId();
        
        var new_data = {
            user_id: userid,
            movie_id: movieid
        };

        $.ajax({
                url: 'http://fa16-cs411-50.cs.illinois.edu/home/add-favorite',
                dataType: 'JSON',
                type: 'POST',
                contentType: 'application/json; charset=utf-8',
                success: function(result) {

                },
                data: JSON.stringify(new_data)
        });
    }
}

/*$("#favorite-btn-1").click(function() {
    
    $("#favorite-btn-1").click(function(){ 
        $("#favorite-btn-1").addClass("disabled");
    });
    
    var movieid = $("#movie-1").data("movie-db-id");
    var auth2 = gapi.auth2.getAuthInstance();
    if (auth2.isSignedIn.get()) {
        
        var profile = auth2.currentUser.get().getBasicProfile();
        var userid = profile.getId();
        
        var new_data = {
            user_id: userid,
            movie_id: movieid
        };

        $.ajax({
                url: 'http://fa16-cs411-50.cs.illinois.edu/home/add-favorite',
                dataType: 'JSON',
                type: 'POST',
                contentType: 'application/json; charset=utf-8',
                success: function(result) {

                },
                data: JSON.stringify(new_data)
        });
    }
});*/

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
