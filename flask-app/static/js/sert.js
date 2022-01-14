$('.notif__sert-info__buttons button').on('click', function (e) {
    e.preventDefault();

    const id = $(this).attr('data-id');
    const url = $(this).attr('data-action');
    const item = $(this).parents('.notif__sert');

    $.ajax({
        url: `/sert/${url}/${Number(id)}`,
        type: 'POST',
        cache: false,
        contentType: false,
        processData: false,
        success: function (data) {
            alert(data.message);

            setTimeout(() => {
                item.slideUp(300);
            }, 500);
        }
    });
});

$('.select-block__list li a').on('click', function () {
    let current = $(this);

    $('[data-filter]').each(function () {
        console.log($(this).attr('data-filter'));
        if ($(this).attr('data-filter') != current.text()) {
            $(this).slideUp(200);
        }
        else {
            $(this).slideDown(200);
        }
    });

    if (current.attr('data-all')) {
        $('[data-filter]').each(function () {
            $(this).slideDown(200);
        });
    }
});