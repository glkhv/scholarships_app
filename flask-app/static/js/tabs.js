$('.notif__menu a').click(function () {
    var id = $(this).attr('data-tab'),
        content = $('.notif__content-item[data-tab="' + id + '"]');

    $('.notif__menu a.active').removeClass('active'); // 1
    $(this).addClass('active'); // 2

    $('.notif__content-item.active').removeClass('active').hide(); // 3
    content.addClass('active').fadeIn(500); // 4
});