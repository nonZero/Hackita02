$(function () {
    var mark = function (b) {
        $('[name=users]:checkbox:visible').prop('checked', b);
    };
    $(".select-all").click(function () {
        mark(true);
    });
    $(".select-none").click(function () {
        mark(false);
    });
});
