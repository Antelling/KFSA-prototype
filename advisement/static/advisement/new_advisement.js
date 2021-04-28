$(".toggle-ico").click(function() {
    let elem = $(this);
    elem.parent().toggleClass("hidden");
});

function reqListCourse(index, target) {
    t = $(target);
    let grade = t.find("option:selected").val();
    if (grade) {
        let grade_name = t.find("select").attr("name");
        let courseNum = t.find(".course_num").text();
        let courseName = t.find(".course_name").text();
        let requirement = t.parent().parent().parent().find("h1").text();
        let inputCourseNum = t.find(".course_num input").val();
        let inputCredit = t.find(".credit_input").val();
        transcript.push({
            "req": requirement,
            "num": courseNum,
            "inputCourseNum": inputCourseNum,
            "inputCredit": inputCredit,
            "name": courseName,
            "grade": grade,
            "grade_name": grade_name,
            "type": "reqlist"
        });
    }
}
function credDemCourse(index, target) {
    t = $(target);
    tt = t;
    let courseNum = t.find(".course_num").val();
    if (courseNum) {
        let grade = t.find("option:selected").text();
        let courseName = t.find(".course_name").val();
        let requirement = t.parent().parent().parent().find("h1").text();
        let credits = t.find(".credit_input").val();
        let row_num = t.attr("name");
        transcript.push({
            "req": requirement,
            "num": courseNum,
            "name": courseName,
            "grade": grade,
            "credit": credits,
            "type": "creditdemand",
            "row_num": row_num
        });
    }
}

function loadTranscript() {
    transcript = [];
    $(".reqlistcourse").each(reqListCourse);
    $(".creddemcourse").each(credDemCourse);
    console.log(transcript);
    let notes = $("#notepad").val();
    let payload = JSON.stringify({serialization: transcript, notes: notes})
    $.post(
        window.location, {csrfmiddlewaretoken: csrf_token, payload:payload},
        function (response) {
            console.log(response);
        }
    );
}

$("#save").click(loadTranscript);

/* write information about a course to the notes textarea */
function courseToNotes(course, error) {
    let ta = $("#notepad");
    msg = `\nCourse Transfer Error: ${error}\n`;
    if (course.inputCourseNum) {
        msg += `\tcourse number: ${course.inputCourseNum}\n`
    } else {
        msg += `\tcourse number: ${course.num}`
    }
    msg += `course name: ${course.name}
    \tpast requirement: ${course.req}
    \tgrade: ${course.grade}\n`
    ta.val(ta.val() + msg);
}
function alienCourse(course) {
   courseToNotes(course, "Unknown course requirement type.")
}
function orphanCourse(course) {
    courseToNotes(course, "The requirement this course claims to satisfy is not found in this program.")
}
function overflowCourse(course) {
   courseToNotes(course, "This course wants to be inserted into a slot that is greater than the amount of slots this requirement has.")
}
function unwantedCourse(course) {
    courseToNotes(course, "The requirement this course claims to satisfy no longer requires this course.")
}
function fillInCourse(course) {
    "use strict";
    let requirement_listing = $($("h1:contains('" + course.req + "')").parent()[0]);
    if (!requirement_listing) {
        orphanCourse(course);
        return;
    }
    if (course.type === "reqlist") {
        let grade_select = $(requirement_listing.find("select[name='" + course.grade_name + "']")[0]);
        if (!grade_select.length) {
            unwantedCourse(course);
            return;
        }
        grade_select.val(course.grade);
        if (course.inputCourseNum) {
            requirement_listing.find(".course_num input").val(course.inputCourseNum);
        }
        if (course.inputCredit) {
            requirement_listing.find(".credit_input").val(course.inputCredit);
        }
    } else if (course.type === "creditdemand") {
        let row = requirement_listing.find("tr[name='" + course.row_num + "']")[0];
        if (!row) {
            overflowCourse(course);
            return;
        }
        row = $(row);
        row.find(".course_num").val(course.num);
        row.find(".course_name").val(course.name);
        row.find(".credit_input").val(course.credit);
        row.find("select").val(course.grade);
    } else {
        alienCourse(course);
    }
}
function applyTranscript(transcript) {
    transcript.forEach(fillInCourse);
}
function loadPastTranscript() {
    return JSON.parse(JSON.parse(document.getElementById('checksheet-data').textContent));
}

$(function() {
    let t = loadPastTranscript();
    applyTranscript(t);
});

$(".uneditable").find("select").prop("disabled", true);


function reqlist_total_credits(index, rl) {
    rl = $(rl);
    let title = rl.find("h1").text()
    let vals = rl.find("select").map((i, e) => e.value).get()
    let credit_amounts = rl.find(".cred-amount").map((i, x) => parseInt($(x).val()))
    let rows_completed = vals.map(v => ["A", "A-", "B+", "B", "B-", "C+", "C", "D", "P"].includes(v))
    let n_filled_in_reqs = rows_completed.filter(v => v).length
    let n_asked_for_reqs = rl.find("select").length

    //sum up amount of completed credits
    let n_completed_credits = 0
    for (let i = 0; i < credit_amounts.length; i++) {
        if (rows_completed[i]) {
            n_completed_credits += credit_amounts[i]
        }
    }

    rl.find(".filled_in_credits").text(n_completed_credits)
    rl.find(".asked_for_reqs").text(n_asked_for_reqs)
    rl.find(".filled_in_reqs").text(n_filled_in_reqs)
}

$("select, .credit_input").change(function (){
    let req = $(this).closest(".requirement")[0]
    reqlist_total_credits(0, req)
})

function go() {
    $(".requirement").map(reqlist_total_credits)
}

go()
