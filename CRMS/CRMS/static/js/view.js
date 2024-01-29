// Course Overview
const viewBtn = document.querySelector('.viewBox');
const courseBox = document.querySelector('.box');

viewBtn.addEventListener('click', () => {
    courseBox.classList.toggle('nact');
});
