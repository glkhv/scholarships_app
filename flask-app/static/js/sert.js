$('.notif__sert-info__buttons button').on('click', function (e) {
    e.preventDefault();

    const id = $(this).attr('data-id');
    const url = $(this).attr('data-action');

    $.ajax({
        url: `/sert/${url}/${Number(id)}`,
        type: 'POST',
        cache: false,
        contentType: false,
        processData: false,
        success: function (data) {
            alert(data.message);
        }
    });
});