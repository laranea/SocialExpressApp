var id = 0;
$(document).ready(function() {
    $.ajaxSetup({ cache: false });

    var getCookie = function(name) {
        var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
        return r ? r[1] : undefined;
    };

    $("#add_rule").click(function() {
      $.ajax({
        headers: {'X-CSRF-Token': getCookie("_xsrf"), 'Content-Type': 'application/x-www-form-urlencoded'},
        type: "POST",
        url: "/addrule",
        data: {
            'keyword': $('#keyword').val(),
            'compare': $('#compare').val(),
            'country': $('#country').val(),
            'emails': $('#emails').val(),
            '_xsrf': getCookie("_xsrf")
        },
        success: function (data) {
        }
      });
      return false;
    });

    $('.delete-report').click(function() {
        $.ajax({
        headers: {'X-CSRF-Token': getCookie("_xsrf"), 'Content-Type': 'application/x-www-form-urlencoded'},
        type: "POST",
        url: "/deletereport",
        data: {
            'reportId': $(this).attr("id"),
            '_xsrf': getCookie("_xsrf")
          },
        success: function (data) {
          }
        });
    });

    $('.dwnld-report').click(function() {
        $.ajax({
        headers: {'X-CSRF-Token': getCookie("_xsrf"), 'Content-Type': 'application/x-www-form-urlencoded'},
        type: "POST",
        url: "/downloadreport",
        data: {
            'reportId': $(this).attr("id"),
            '_xsrf': getCookie("_xsrf")
          },
        success: function (data) {
          }
        });
    });

    $('#realtime-report').click(function() {
        $.ajax({
        headers: {'X-CSRF-Token': getCookie("_xsrf"), 'Content-Type': 'application/x-www-form-urlencoded'},
        type: "POST",
        url: "/newrealtimereportcrieria",
        data: {
            'keyword': $('#keyword').val(),
            'sentiment': $('#sentiment').val(),
            'country': $('#country').val(),
            'language': $('#language').val(),
            'changes': $('#changes').val(),
            'change-rate': $('#change-rate').val(),
            'emails': $('#emails').val(),
            '_xsrf': getCookie("_xsrf")
          },
        success: function (data) {
          }
        });
        return false;
    });

    var delete_trigger = function () {
        $.ajax({
        headers: {'X-CSRF-Token': getCookie("_xsrf"), 'Content-Type': 'application/x-www-form-urlencoded'},
        type: "POST",
        url: "/deletetrigger",
        data: {
            'triggerId': id,
            '_xsrf': getCookie("_xsrf")
          },
        success: function (data) {
          }
        });
    };

    $('.delete-trigger').click(function() {
        id = $(this).attr("id");
        delete_trigger();
    });

    $('.dwnld-realtime-report').click(function() {
        $.ajax({
        headers: {'X-CSRF-Token': getCookie("_xsrf"), 'Content-Type': 'application/x-www-form-urlencoded'},
        type: "POST",
        url: "/downloadrealtimereport",
        data: {
            'reportId': $(this).attr("id"),
            '_xsrf': getCookie("_xsrf")
          },
        success: function (data) {
          }
        });
    });
});
