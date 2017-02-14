var SERVICE_URL = "http://150.65.242.90:34082"

var ENTTYPE_ELEM = {
    1: "#details-person",
    6: "#details-orgplace"
}

var answers = null;

$(document).ready(function() {
    $("#search").on("keypress", function(event) {
        if(event.which == 13) {
          send_query(event);
        }
    });

    $("#search").on("focus", function(event) {
        $(".details").css("display", "none");
        $(".tips").css("display", "block");
    });
});


function send_query(event) {
    $("#answers").css("display", "none");
    $(".details").css("display", "none");
    $("#loading-icon").css("display", "block");
    $("#answers").empty();

    $.ajax({
      url: SERVICE_URL + "/qa_serv/query",
      dataType: "json",
      crossDomain: true,
      data: {
        query: $("#search").val()
      },
      success: fill_results
    });
}

function fill_results(data) {
    if (data != null && data.length > 0) {
        answers = data
        num_answers = answers.length;

        for (var i = 0; i < num_answers; i++) {
            if (data[i].uri == "gps://here")
                break

            set_result(data[i], i);
        }
    }
    else {
        set_noanswer();
    }

    $("#answers").css("display", "block");
    $("#loading-icon").css("display", "none");
}

function set_result(answer, index) {
    var row_new = $("<tr class=\"answer\" onclick=\"show_details(" + index + ")\"></tr>");
    var pict_col = $("<td class=\"ans-picture\"></td>")
    var ans_link = $("<a href=\"" + answer.uri + "\" target=\"_blank\"></a>");
    var pict_elem = $("<img src=\"" + answer.pictureURL + "\" />");
    var text_col = $("<td class=\"ans-text\"></td>");
    pict_col.append(pict_elem);
    ans_link.append(answer.name);
    text_col.append(ans_link);
    row_new.append(pict_col);
    row_new.append(text_col);
    $("#answers").append(row_new);
}

function set_noanswer() {
    var query = $("#search").val();
    var exist_re = /^Is there/i;
    var place_re = /^Where/i;
    var person_re = /^Who/i;
    var noans = "I don't know...";

    if (query.match(exist_re)) {
        noans = "I don't think so...";
    }
    else if (query.match(place_re)) {
        noans = "I couldn't find such place...";
    }
    else if (query.match(person_re)) {
        noans = "I don't know such person...";
    }

    var row_new = $("<tr class=\"noanswer\"><td>" + noans + "</td></tr>");
    $("#answers").append(row_new);
}

function show_details(index) {
    $(ENTTYPE_ELEM[answers[index].entType] + " tr td[data-attr]").each(function (i) {
        var attr = answers[index][$(this).attr("data-attr")];

        if (attr) {
            this.innerHTML = attr;
        }
        else {
            this.innerHTML = "";
        }
    });

    $(ENTTYPE_ELEM[answers[index].entType]).css("display", "block");
    new_offset_top = $("#answers tr").eq(index).offset().top;
    cur_offset_left = $(ENTTYPE_ELEM[answers[index].entType]).offset().left
    $(ENTTYPE_ELEM[answers[index].entType]).offset({top: new_offset_top, left: cur_offset_left});

    $(".tips").css("display", "none");
}
