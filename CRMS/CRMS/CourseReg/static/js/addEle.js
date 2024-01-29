// Add Drop Course
const add = document.querySelector('.btn-li-add');
const dropCourse = document.querySelector('.dropSection');
const drop = document.querySelector('.btn-li-drop');

add.addEventListener('click', () => {
    dropCourse.classList.remove('nact');
});

drop.addEventListener('click', () => {
    dropCourse.classList.add('nact');
});

// Slide course
const addForm = document.querySelector("form.add");
const addLable = document.querySelector("label.add");
const dropLable = document.querySelector("label.drop");

dropLable.onclick = () => {
    addForm.style.marginLeft = "-50%";
};

addLable.onclick = () => {
    addForm.style.marginLeft = "0%";
};

function myfun() {
    var x = document.querySelectorAll("form.dropSection");
    if (x.style.display === "block") {
        x.style.display = "none";
    } else {
        x.style.display = "block";
    };
};