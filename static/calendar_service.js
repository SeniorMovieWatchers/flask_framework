var CLIENT_ID = '567865399405-tn5a3lefjbea3phdaui3gh27a9q9r1cl.apps.googleusercontent.com';

var SCOPES = ["https://www.googleapis.com/auth/calendar"];

/**
 * Check if current user has authorized this application.
 */
function checkAuth() {
  gapi.auth.authorize(
    {
      'client_id': CLIENT_ID,
      'scope': SCOPES.join(' '),
      'immediate': true
    }, handleAuthResult);
}

/**
 * Handle response from authorization server.
 *
 * @param {Object} authResult Authorization result.
 */
function handleAuthResult(authResult) {
  if (authResult && !authResult.error) {
    // Hide auth UI, then load client library.
    loadCalendarApi();
  }
}

function loadCalendarApi() {
  gapi.client.load('calendar', 'v3', create_event);
}

/**
 * Initiate auth flow in response to user clicking authorize button.
 *
 * @param {Event} event Button click event.
 */
function handleAuthClick(event) {
  gapi.auth.authorize(
    {client_id: CLIENT_ID, scope: SCOPES, immediate: true},
    handleAuthResult);
  return false;
}

var summary;
var description;

function create_event() {
  date = $("#date").val();
  start_time = $("#start-time").val();
  end_time = $("#end-time").val();
  email = $("#email").val();
  var event = {
    'summary' : summary,
    'description' : description,
    'start' : {
      'dateTime' : date + "T" + start_time,
      'timeZone' : 'America/Chicago'
    },
    'end' : {
      'dateTime' : date + "T" + end_time,
      'timeZone' : 'America/Chicago'
    },
    'attendees' : [
      {'email' : email}
    ]
  };
  console.log(event);
  
  var request = gapi.client.calendar.events.insert({
    'calendarId': 'primary',
    'resource': event
  });

  request.execute(function(event) {
    $.notify({
      message: 'Successfully created calendar event' 
    });
  });
}

function createCalendar(i) {
  summary = $("#movie-title-" + i).text();
  description = $("#movie-plot-" + i).text();
}