function chooseMonth(){
    let links = document.getElementsByClassName("a_choose");
    for (let item of links) {
        if (item.getAttribute("hidden") !== null){
            item.removeAttribute("hidden");
        } else {
            item.setAttribute("hidden", "");
        }
    }
}

function selectDay(item){
    if (item.nextElementSibling.getAttribute("hidden") !== null){
        item.nextElementSibling.removeAttribute("hidden");
    } else {
        item.nextElementSibling.setAttribute("hidden", "");
    }
}

function deselectDay(item){
    item.setAttribute("hidden", "");
}