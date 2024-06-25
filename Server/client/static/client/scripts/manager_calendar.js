/*
function chooseMonth(){
    let links = document.getElementsByClassName("choose_month");
    for (let item of links) {
        if (item.getAttribute("hidden") !== null){
            item.removeAttribute("hidden");
        } else {
            item.setAttribute("hidden", "");
        }
    }
}

function selectNewMonth(newMonth){
    let oldMonth = document.getElementById("selectedMonth");
    oldMonth.innerHTML = newMonth.textContent;
}

function selectMonthYear(){
    let month = document.getElementById("selectedMonth").textContent.trim();
    let year = document.getElementById("selectedYear").value;

    window.location.href = "?monthYear=" + month + " " + year;
}*/

function prevMonth(nowMonth, nowYear, allMonth){
    //alert(allMonth[allMonth.indexOf(nowMonth)-1]);
    if (nowMonth==="Январь"){
        window.location.href = "?monthYear=" + "Декабрь " + (nowYear-1);
    } else {
        window.location.href = "?monthYear=" + allMonth[allMonth.indexOf(nowMonth)-1] + " " + nowYear;
    }

}

function nextMonth(nowMonth, nowYear, allMonth){
    //alert(allMonth[allMonth.indexOf(nowMonth)-1]);
    if (nowMonth==="Декабрь"){
        window.location.href = "?monthYear=" + "Январь " + (nowYear+1);
    } else {
        window.location.href = "?monthYear=" + allMonth[allMonth.indexOf(nowMonth)+1] + " " + nowYear;
    }

}