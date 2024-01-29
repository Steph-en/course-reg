var objStudets =
[
    {
        username: "ENG19A00007Y",
        password: "Ait123"
    },
    // {
    //     username: "ENG19A00017Y",
    //     password: "Ait123"
    // },
    // {
    //     username: "ADS19A00106Y",
    //     password: "Ait123"
    // },
    // {
    //     username: "ADMIN",
    //     password: "Ait123"
    // }
]

var objAdmin =
[
    {
        username: "ADMIN",
        password: "Ait123"
    }
]

// Login for students
function getInfo()
{
    var username = document.getElementById("yourUsername").value
    var password = document.getElementById("yourPassword").value
    var button = document.querySelector(".btn")
    
    var i;

    for (i = 0; i < objStudets.length; i++) {
        if (username == objStudets[i].username && password == objStudets[i].password) {
            alert(username + " is valid!!!");
            window.location = 'student-dashboard.html';
            return
        } else {
        }
        alert("Incorrect username or password");
    }
};

// Login for admin
function getInfom()
{
    var username = document.getElementById("yourUsername").value
    var password = document.getElementById("yourPassword").value
    var button = document.querySelector(".btn")

    var i;

    for (i = 0; i < objAdmin.length; i++) {
        if (username == objAdmin[i].username && password == objAdmin[i].password) {
            alert(username + " is valid!!!");
            window.location = 'admin-dashboard.html';
            return
        } else {
        }
    }
    alert("Incorrect username or password");
};
// module.exports = getInfo;