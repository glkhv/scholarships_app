$(document).mouseup(function (e) {
    let sideBlock = $(".side__block");
    let close = $('.side__close button');
    if (close.is(e.target) || (!sideBlock.is(e.target) && sideBlock.has(e.target).length === 0)) {
        $('.side').removeClass('active');
    }
});


$('.side-open').on('click', function (e) {
    e.preventDefault();

    $('#side').addClass('active');

    const id = $(this).attr('data-id');
    const page = $(this).attr('page');
    const url = $(this).attr('url');

    $.ajax({
        url: `/${url}/${Number(id)}`,
        type: 'POST',
        cache: false,
        contentType: false,
        processData: false,
        success: function (data) {
            $('.side__block').html(fillData(data, page));

            setTimeout(() => {
                $('.side-div').fadeOut(300);
            }, 1000)

            checkButtons();
        }
    });
});


function fillData(data, page) {
    let array = [];
    for (let i = 1; i <= Object.keys(data).length - 1; i++) {
        array.push(Array(data[i].title, data[i].event_type, data[i].event_status));
    }

    let output = array.map(item => {
        return `
                <div class="side__info-docs__item">
                        <div class="side__info-img">
                            <a href="#">
                                <img src="static/img/sert.png" alt="">
                            </a>
                        </div>
                        <div class="side__info-text">
                            <div class="side__info-text__top">
                                <h3>${item[0]}</h3>
                                <p>${item[1]}, ${item[2]}</p>
                            </div>
                            <div class="side__info-text__bottom">
                                <p><img src="static/img/ok.svg" alt=""> Действителен
                                    до 13.05.2022</p>
                            </div>
                        </div>
                    </div>`
    });

    const result = fillSide(output, data, page);

    return result;
}


function fillSide(...args) {

    const output = args[0];
    const data = args[1];
    const page = args[2];

    let buttons = '';
    let descr = '';

    if (page == "app") {
        buttons = `
        <div class="side__buttons">
            <button data-cancel data-action="deny" data-id="${data[0].id}">Отклонить заявку</button>
            <button data-accept data-action="accept" data-id="${data[0].id}">Принять заявку</button>
        </div>
        `
    }

    if (page == "grant") {
        buttons = `
        <div class="side__buttons grants">
            <button data-cancel data-action="deny" data-id="${data[0].id}">Отклонить заявку</button>
        </div>
        `
    }

    if (page == "grant" || page == "app") {
        descr = `
        <div class="side__info-descr__items">
            <div class="side__info-descr__item">
                <h6>Специальность</h6>
                <p>${data[0].speciality_name} (${data[0].speciality_code})</p>
            </div>
            <div class="side__info-descr__item">
                <h6>Общее кол-во оценок</h6>
                <p>${data[0].total_marks_count}</p>
            </div>
            <div class="side__info-descr__item">
                <h6>Кол-во оценок “Отлично”</h6>
                <p>${data[0].excellent_marks_count}</p>
            </div>
        </div>`
    }

    if (page == "student") {
        descr = `
        <div class="side__info-descr__items student">
            <div class="side__info-descr__item">
                <h6>Специальность</h6>
                <p>${data[0].speciality_name} (${data[0].speciality_code})</p>
            </div>
            <div class="side__info-descr__item">
                <h6>Почта</h6>
                <p>${data[0].email}</p>
            </div>
            <div class="side__info-descr__item">
                <h6>Номер телефона</h6>
                <p>${data[0].number}</p>
            </div>
        </div>`
    }


    return `
            <div class="side-div" style="position: absolute; left:0; top:0; width: 100%; height: 100%; background: #fff; z-index:24;"></div>
            <div class="side__close">
                <button>
                    <img src="static/img/close.svg" alt="">
                </button>
            </div>
            <div class="side__info">
                <div class="side__info-title">
                    <h1>${data[0].fullname}, ${data[0].academic_group_number}</h1>
                    <p>${page == "student" ? '' : data[0].type}</p>
                </div>
                <div class="side__info-block">
                    <div class="side__info-descr">
                        ${descr}
                    </div>
                    <div class="side__info-docs">
                        <h2>Прикрепленные документы</h2>
                        <div class="side__info-docs__items">
                            ${output}
                        </div>
                    </div>
                </div>
            </div>
            ${buttons}`
}


function checkButtons() {
    $('.side__buttons button').on('click', function (e) {
        e.preventDefault();

        const id = $(this).attr('data-id');
        const url = $(this).attr('data-action');

        $.ajax({
            url: `/${url}/${Number(id)}`,
            type: 'POST',
            cache: false,
            contentType: false,
            processData: false,
            success: function (data) {
                alert(data.message)
            }
        });
    });
}
