//search booking
function toDoSearchBooking(){
    window.location.href = "?searchBooking=" + document.getElementById("searchBooking").value;
}

//if click on main checkbox
function onClickCheckBooking(checkObject){
    let booking = document.getElementsByClassName("checkbox_booking");
    for (let book of booking) {
        if (checkObject.checked){
            book.checked = true;
        }
        else {
            book.checked = false;
        }
    }
}

//shows or hides the add books form
function changeHiddenAddBooking(){
    let addBlock = document.getElementById("addBookingBlock");
    let addButton = document.getElementById("addBookingButton");
    if (addBlock.getAttribute("hidden") !== null){
        addBlock.removeAttribute("hidden");
        addButton.textContent = "Скрыть форму добавления";
    } else {
        addBlock.setAttribute("hidden", "");
        addButton.textContent = "Добавить новые записи";
    }
}

//increases the amount of added time
function addTimesBookingButton(button){
    let input = document.createElement("input");
    input.type = "time";
    input.name = "time"; //+ (times++);
    input.setAttribute("required", "");
    input.setAttribute("class", "inputTime");

    let del_button = document.createElement("button");
    del_button.setAttribute("onclick", "removeTimesBookingButton(this)");
    del_button.setAttribute("type", "button");
    del_button.setAttribute("class", "removeTimeButton")
    del_button.innerHTML = "-";

    button.parentNode.insertBefore(document.createElement("br"), button);
    button.parentNode.insertBefore(del_button, button);
    button.parentNode.insertBefore(input, button);
}

//reduces the amount of added time
function removeTimesBookingButton(button){
    button.previousSibling.remove();
    button.nextSibling.remove();
    button.remove();
    //times--;
}

//remove the book
function removeBooking(){
    let booking = document.getElementsByClassName("checkbox_booking");
    let chooseBook = [];
    for (let book of booking) {
        if (book.checked){
           chooseBook.push(book.id);
        }
    }
    //are you sure
    const agreement = confirm('Вы уверены, что хотите удалить ' + chooseBook.length + ' запись(ей)?');
    if (agreement) {
        fetch(remove_booking_link, {
            method: "POST",
            headers: {'Content-Type': 'application/json', "X-CSRFToken": csrf},
            body: JSON.stringify({
                nameBlock: 'removeBooking',
                dataBookingRemove: chooseBook
            })
        }).then(response => {
            //console.log("Response text: " + response.text());
            window.location.href = response.url;
        });
    }
}
