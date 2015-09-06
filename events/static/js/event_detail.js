$(function () {

    function refreshEmails() {
        var boxes = $('.user-email:checked');

        $('#emails').val(boxes.map(function () {
            return $(this).val();
        }).get().join('\n')).prop('rows', boxes.length);


    }

    $('.user-email').change(refreshEmails);

    refreshEmails();

    $(".grouper").click(function () {
        var boxes = $(this).parent('.group').find(':checkbox');
        console.log(boxes, boxes.length, boxes.filter(':checked').length);
        boxes.prop('checked', boxes.length > boxes.filter(':checked').length);
        refreshEmails();
    });

})
;
