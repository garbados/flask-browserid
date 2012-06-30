$(function() {
  var gotAssertion, logoutCallback, loginURL, logoutURL;

  gotAssertion = function(assertion) {
    if (assertion) {
      return $.ajax({
        type: 'POST',
        url: '{{ login_url }}',
        data: {
          assertion: assertion
        },
        success: function(res, status, xhr) {
          return location.reload(true);
        },
        error: function(res, status, xhr) {
          return alert("login failure: " + status);
        }
      });
    }
  };
  logoutCallback = function(event) {
    $.ajax({
      type: 'POST',
      url: '{{ logout_url }}',
      success: function() {
        return location.reload(true);
      },
      error: function(res, status, xhr) {
        console.log(res);
        return alert("logout failure: " + status);
      }
    });
    return false;
  };
  return $(function() {
    $('#browserid-login').click(function() {
      navigator.id.get(gotAssertion);
      return false;
    });
    $('#browserid-logout').click(function() {
      navigator.id.logout(logoutCallback);
      return false;
    });
  });
});
