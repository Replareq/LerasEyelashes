function checkPhone() {
    let input_value = document.getElementById("phone");
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

function formValidator(form) {
    if (form.phone.value.replace(/\D/g,'').length != 9){
        alert("Неправильный ввод телефона (9 цифр, учитывая код)");
        return false;
    }
    else {
        return true;
    }
}
