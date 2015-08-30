$(function () {
    "use strict";

    var original = $("#voteform").serialize();


    var refresh = function() {
        $("#voteform .save").toggle($("#voteform").serialize() != original)
    };


    $("#voteform input").change(refresh);

    $("#voteform").ajaxForm({
        success: function() {
            $('#voteform button,#voteform input').prop('disabled', false);
            $('#voteform .ok').show().slideUp(1500);
            $('#voteform .loader').hide();
            original = $("#voteform").serialize();
            refresh();
        },
        beforeSubmit: function() {
            $('#voteform button,#voteform input').prop('disabled', true);
            $('#voteform .ok').hide();
            $('#voteform .loader').show();
        },
        error: function() {
            alert("Unexpected error. Please reload page.");
        }
    })
});