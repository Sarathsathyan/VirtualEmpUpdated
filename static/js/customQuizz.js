'use strict'
// Written using ES5 JS for browser support

// This block of code for confirmation of finish test button; toast starts here
window.addEventListener('DOMContentLoaded', function () {
    // Method to trigger toast on error.
    var alert_message = document.getElementById('messageInfo');
    if (alert_message != null) {
        var toastHTML = alert_message.value;
        M.toast({html: toastHTML, classes: 'rounded'});
    }
    var ele = document.querySelectorAll('.modal');
    var instances = M.Modal.init(ele);
});
// This block of code for confirmation of finish test button; toast ends here

//Disable enroll button
function getButtonLoader() {
    var btnElement = document.getElementById('formSubmitBtn');
    document.getElementsByClassName('isEnroll')[0].classList.add('hide');
    document.getElementsByClassName('isLoading')[0].classList.remove('hide');
    btnElement.disabled = true;
}

//Button to start Test
let start_test_btn = document.getElementById("startTest");
if (start_test_btn != null) {
    start_test_btn.onclick = function() {
        var qid = document.getElementById("qId").value;
        var currentTime = new Date();
        localStorage.setItem('starttime', currentTime.getTime());
        sessionStorage.setItem("startTimer", true)
        window.location.href = `/userlogin/userdashboard/userQuizz/${qid}/`
    }
}

// Method to start timer for test
if (sessionStorage.getItem("startTimer")) {
    let startTime = localStorage.getItem('starttime')
    let currentTime = new Date()
    var difference = currentTime.getTime() - startTime;
    // document.write(difference)
    var ms = difference;
    var ms = 1000 * Math.round(ms / 1000);
    var d = new Date(ms);
    var time_diff = d.getUTCMinutes() + ':' + d.getUTCSeconds();
    var time = time_diff;
    var timeParts = time.split(":");
    var timer = +timeParts[0] * (30000 * 60) + (+timeParts[1] * 30000);
    var time1 = "60:00";
    var timeParts1 = time1.split(":");
    var timer1 = +timeParts1[0] * (30000 * 60) + (+timeParts1[1] * 30000);

    let actual_time = timer1 - timer;
    console.log(actual_time)

    var total_seconds = (actual_time / 1000) / 60;
    var c_minutes = parseInt(total_seconds / 60);
    var c_seconds = parseInt(total_seconds % 60);

    setTimeout("CheckTime()", 1000);
    history.pushState(null, document.title, location.href);
    window.addEventListener('popstate', function (event) {
        history.pushState(null, document.title, location.href);
    });
}

function CheckTime() {


    document.getElementById("quiz-time-left").innerHTML = 'Remaining Time: ' + c_minutes + ' m : ' + c_seconds + ' s';
    if (total_seconds <= 0) {
        setTimeout('document.quiz.submit()', 1);
    } else {
        total_seconds = total_seconds - 1;
        c_minutes = parseInt(total_seconds / 60);
        c_seconds = parseInt(total_seconds % 60);
        setTimeout("CheckTime()", 1000);
    }
}


function Myfunc() {
    console.log(total_seconds)
    var remaining = total_seconds / 60
    var tot_remaining = 30 - remaining
    document.getElementById("time").value = ~~tot_remaining

}

// Show check option on left panel
function isChecked(id) {
    document.getElementById("isOptionUnChecked" + id).classList.add('hide');
    document.getElementById("isOptionChecked" + id).classList.remove('hide');
}


// Question panel tab function
function question(evt, questionNo, type) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].style.backgroundColor = "";
    }

    if (type == 'pre') {
        questionNo = parseInt(questionNo) - 1
    }
    if (type == 'next') {
        questionNo = parseInt(questionNo) + 1
    }
    document.getElementById(questionNo).style.display = "block";
    let tabid = 'defaultOpen' + questionNo
}

let tabid = 'defaultOpen' + 1
let tab = document.getElementById(tabid);
if (tab != null) tab.click();

// Submit the question form
var submit_quiz_form = document.getElementById("complete_test");
if (submit_quiz_form != null) {
    submit_quiz_form.onclick = function () {
        document.getElementById("quiz").submit();
        localStorage.setItem("startLoader", 1);
    }
}

//Progress Loader
var i = 0;

function progressLoader() {
    if (i == 0) {
        var elem = document.getElementById("myBar");
        var width = 1;
        var id = setInterval(frame, 25);

        function frame() {
            if (width >= 100) {
                clearInterval(id);
                i = 0;
                localStorage.clear();
                sessionStorage.clear();
                document.getElementById("endUserSessionForm").submit();
            } else {
                width++;
                elem.style.width = width + "%";
            }
        }
    }
}

if (localStorage.getItem('startLoader') == 1) setTimeout(progressLoader, 5000);
