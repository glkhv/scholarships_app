document.querySelectorAll('button[data-side]').forEach(item => {

    const id = item.getAttribute('data-side');

    item.onclick = event => {
        event.preventDefault();

        document.getElementById(id).classList.toggle('active');
    }
});

const side = document.querySelectorAll('.side');
side.forEach(item => {
    let closeButton = item.querySelector('.side__close button');
    let sideBlock = item.querySelector('.side__block');

    item.onmouseup = (event) => {

        let target = event.target;

        if (!sideBlock.contains(target) || closeButton.contains(target)) {
            item.classList.remove('active');
        }
    }
})


const menuSelect = document.querySelector('.select > div');
const menuSelectList = menuSelect.querySelector('ul');

menuSelect.addEventListener('click', () => {
    menuSelect.classList.toggle('active');
    menuSelectList.classList.toggle('active');
});

document.addEventListener('click', event => {
    let target = event.target;
    let select = target == menuSelect || menuSelect.contains(target);
    let selectActive = menuSelect.classList.contains('active');
    if (!select && selectActive) {
        menuSelect.classList.remove('active');
        menuSelectList.classList.remove('active');
    }
});

const grantBlockHeight = document.querySelector('.grant__block');
const grantBottomHeight = document.querySelector('.grant__bottom');
const grantBlock = document.querySelector('.grant__block');

if (grantBlockHeight && grantBottomHeight && grantBlock) {
    let diffHeight = grantBottomHeight.getBoundingClientRect().top - grantBlockHeight.getBoundingClientRect().top;

    grantBlock.style.maxHeight = `${diffHeight}px`;
}
