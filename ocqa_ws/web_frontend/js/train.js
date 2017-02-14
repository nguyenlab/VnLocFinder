var SERVICE_URL = "http://150.65.242.59:34082"

$(document).ready(function() {
    $(".segments").on("keypress", function(event) {
        if(event.which == 13) {
          send_segments(event);
        }
    });

    $(".search").on("keypress", function(event) {
        if(event.which == 13) {
          send_query(event);
        }
    });

    $("#search").on("focusout", function(event) {
          send_query(event);
    });
});

function send_query(event) {
    if ($("#search").val() == "") {
        $(".segments input").val("");
        return;
    }

    $.ajax({
      url: SERVICE_URL + "/qa_serv/qseg",
      dataType: "json",
      crossDomain: true,
      data: {
        query: $("#search").val()
      },
      success: segments_recv
    });
}

function segments_recv(data) {
    if (data != null) {
        for (var field in data) {
            if (data.hasOwnProperty(field)) {
                $("#" + field).val(data[field]);
            }
        }
    }
    else {
        alert("No segments could be extracted");
    }
}

function send_segments(event) {
    $(".segments").css("display", "none");
    $("#loading-icon").css("display", "block");

    $.ajax({
      url: SERVICE_URL + "/qa_serv/qtrain",
      dataType: "json",
      crossDomain: true,
      data: {
        query: $("#search").val(),
        qtype: $("#qtype").val(),
        qexpr: $("#qexpr").val(),
        quant: $("#quant").val(),
        topic: $("#topic").val(),
        cond: $("#cond").val()
      },
      success: response_recv
    });
}

function response_recv(data) {
    $("#loading-icon").css("display", "none");

    if (data != null) {
        $("#success-icon").css("display", "block");

        setTimeout(function () {
            $("#success-icon").css("display", "none");
            $(".segments").css("display", "block");
            $(".segments input").val("");
            $("#search").val("");
            $("#search").focus();
        }, 1000);
    }
    else {
        alert("Problem detected while sending the segments");
        $(".segments").css("display", "block");
    }
}