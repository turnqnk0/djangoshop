const productContainers = [...document.querySelectorAll('.product-container')]
const nxtBtn = [...document.querySelectorAll('.nxt-btn')]
const preBtn = [...document.querySelectorAll('.pre-btn')]

productContainers.forEach((item, i) => {
    let containerDimensions = item.getBoundingClientRect();
    let containerWidth = containerDimensions.width;

    nxtBtn[i].addEventListener('click', () => {
        item.scrollLeft += containerWidth / 2;
    })
    preBtn[i].addEventListener('click', () => {
        item.scrollLeft -= containerWidth / 2;
    })


    item.addEventListener('scroll', (event) => {
        if(event.deltaX > 0) {
            item.scroll += containerWidth;
        }
        else {
            item.scroll -= containerWidth;
        }
    });

})


let items = document.querySelectorAll('.slider .list .item');
let next = document.getElementById('next');
let prev = document.getElementById('prev');
let thumbnails = document.querySelectorAll('.thumbnail .item');


let countItem = items.length
let itemActive = 0;

next.onclick = function (){
    itemActive = itemActive + 1;
    if (itemActive >= countItem){
        itemActive = 0;
    }
    showSlider();
}

prev.onclick = function (){
    itemActive = itemActive - 1;
    if(itemActive < 0){
        itemActive = countItem - 1;
    }
    showSlider();
}

let refreshInterval = setInterval(() => {
    next.click();
}, 3000)
function showSlider() {
    let itemActiveOld = document.querySelector('.slider .list .item.active');
    let thumbnailActiveOld = document.querySelector('.thumbnail .item.active');
    itemActiveOld.classList.remove('active');
    thumbnailActiveOld.classList.remove('active');


    items[itemActive].classList.add('active');
    thumbnails[itemActive].classList.add('active');

    clearInterval(refreshInterval);

}

thumbnails.forEach((thumbnail, index) => {
    thumbnail.addEventListener('click' , () => {
        itemActive = index;
        showSlider();
    })
})