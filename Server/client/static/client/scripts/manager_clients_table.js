//search client
function toDoSearchClient(){
    window.location.href = "?searchClient=" + document.getElementById("searchClient").value;
}

//if click on main checkbox
function onClickCheckClient(value){
    let all_check = document.getElementById(value);
    let clients = document.getElementsByClassName("checkbox_client");
    for (let client of clients) {
        if (all_check.checked){
            client.checked = true;
        }
        else {
            client.checked = false;
        }
    }
}

//this shows or hides the add user form
function changeHiddenAddClient(){
    let addBlock = document.getElementById("addClientBlock");
    let addButton = document.getElementById("addClientButton");
    if (addBlock.getAttribute("hidden") !== null){
        addBlock.removeAttribute("hidden");
        addButton.textContent = "Скрыть форму добавления";
    } else {
        addBlock.setAttribute("hidden", "");
        addButton.textContent = "Добавить пользователя";
    }
}

//remove chosen clients
function removeClient(){
    let clients = document.getElementsByClassName("checkbox_client");
    let choosePhoneClients = [];
    for (let client of clients) {
        if (client.checked){
            choosePhoneClients.push(client.id);
        }
    }
    //are you sure
    const agreement = confirm('Вы уверены, что хотите удалить ' + choosePhoneClients.length + ' пользователя(ей) (' + choosePhoneClients + ')?');
    if (agreement && choosePhoneClients.length != 0) {
        fetch(remove_client_link, {
            method: "POST",
            headers: {'Content-Type': 'application/json', "X-CSRFToken": csrf},
            body: JSON.stringify({
                nameBlock: 'removeClients',
                dataClientsRemove: choosePhoneClients
            })
        }).then(response => {
            //console.log("Response text: " + response.text());
            window.location.href = response.url;
        });
    }
}

//set or unset ban chosen client
function changeBanClient(tel){
    fetch(change_link, {
        method: "POST",
        headers: {'Content-Type': 'application/json', "X-CSRFToken": csrf},
        body: JSON.stringify({
            nameBlock: 'changeBanClient',
            telClient: tel
        })
    }).then((response) => {
        //console.log("Response text: " + response.text());
        window.location.href = response.url;
    });
}

//check out number in the form of add client
function checkPhone() {
    let input_value = document.getElementById("clientAddTel");
    //не удаляются скобки (если только не выбрать все и удалить)
    input_value.value = input_value.value.replace(/\D/g, '').replace(/(\d{1})(\d{1})?(\d{1,3})?(\d{1,4})?/, function(_, p1, p2, p3, p4){
        let output = ""
        if (p1) output = `(${p1}`;
        if (p2) output += `${p2})`;
        if (p3) output += ` ${p3}`;
        if (p4) output += ` ${p4}`;
        return output;
    });
}

//check form of add client
function formClientValidator(form) {
    if (form.clientAddTel.value.replace(/\D/g,'').length != 9){
        alert("Неправильный ввод телефона (9 цифр, учитывая код)");
        return false;
    }
    else {
        return true;
    }
}
