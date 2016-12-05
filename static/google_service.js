function onSuccess(googleUser) {
    console.log(googleUser.getBasicProfile().getId());
    $('#google-signin').hide();
    $('#username').text(googleUser.getBasicProfile().getGivenName());
    $('#profile_image').attr('src', googleUser.getBasicProfile().getImageUrl());
    $('#profile-header').show();
    signIn(googleUser);
    updateRecs();
}

function signIn(googleUser) {
    var new_data = {
        id : googleUser.getBasicProfile().getId(),
        username: googleUser.getBasicProfile().getGivenName(),
        email: googleUser.getBasicProfile().getEmail()
    };

    $.ajax({
        url: 'http://fa16-cs411-50.cs.illinois.edu:5000/signin',
        dataType: 'JSON',
        type: 'POST',
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify(new_data)
    });
}

function onFailure(error) {
    console.log(error);
}

function renderButton() {
    gapi.signin2.render('google-signin', {
        'scope': 'profile email',
        'width': 200,
        'height': 40,
        'longtitle': true,
        'theme': 'light',
        'onsuccess': onSuccess,
        'onfailure': onFailure
  });
}

$('#signout-button').click(function() {
    var auth2 = gapi.auth2.getAuthInstance();
    auth2.signOut().then(function () {
        $('#profile-header').hide();
        $('#google-signin').show();
    });
})
