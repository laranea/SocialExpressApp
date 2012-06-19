var trigger_id = 0;
var report_id = 0;
$(document).ready(function() {
    $.ajaxSetup({ cache: false });
    var getCookie = function(name) {
        var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
        return r ? r[1] : undefined;
    };

    $("#add_rule").click(function() {
      $("#rule_add_alert").fadeIn(1600);
      $("#rule_add_alert").delay(1200).fadeOut(1600);
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

    var delete_report = function() {
        $("#"+report_id).parent('td').parent('tr').fadeOut(1000);
        $.ajax({
        headers: {'X-CSRF-Token': getCookie("_xsrf"), 'Content-Type': 'application/x-www-form-urlencoded'},
        type: "POST",
        url: "/deletereport",
        data: {
            'reportId': report_id,
            '_xsrf': getCookie("_xsrf")
          },
        success: function (data) {
          }
        });
    };

    $('.delete-report').click(function() {
        report_id = $(this).attr("id");
        $("#delete_rpt_alert").delay(400).fadeIn(1600);
    });

    $('#report_del_yes').click(function() {
        delete_report();
        $("#delete_rpt_alert").delay(600).fadeOut(1600);
    });

    $('#report_del_no').click(function() {
        report_id = 0;
        $("#delete_rpt_alert").delay(600).fadeOut(1600);
    });

    $('.dwnld-report').click(function() {
        $("#dwnld_rpt_alert").fadeIn(1600);
        $("#dwnld_rpt_alert").delay(1200).fadeOut(1600);
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
        $("#new_trigger_alert").fadeIn(1600);
        $("#new_trigger_alert").delay(1200).fadeOut(1600);
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
        $("#"+trigger_id).parent('td').parent('tr').fadeOut(1000);
        $.ajax({
        headers: {'X-CSRF-Token': getCookie("_xsrf"), 'Content-Type': 'application/x-www-form-urlencoded'},
        type: "POST",
        url: "/deletetrigger",
        data: {
            'triggerId': trigger_id,
            '_xsrf': getCookie("_xsrf")
          },
        success: function (data) {
          }
        });
    };

    $('.delete-trigger').click(function() {
        trigger_id = $(this).attr("id");
        $("#delete_trigger_alert").delay(400).fadeIn(1600);
    });

    $('#trigger_del_yes').click(function() {
        delete_trigger();
        $("#delete_trigger_alert").delay(600).fadeOut(1600);
    });

    $('#trigger_del_no').click(function() {
        trigger_id = 0;
        $("#delete_trigger_alert").delay(600).fadeOut(1600);
    });

    $('.dwnld-realtime-report').click(function() {
        $("#dwnld_trigger_alert").fadeIn(1600);
        $("#dwnld_trigger_alert").delay(1200).fadeOut(1600);
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
