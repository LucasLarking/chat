//  ###########  CREATE ROOM FORM ###########

let inputName = document.querySelector('.inputName');
let inputDescription = document.querySelector('.inputDescription');
let nameError = document.querySelector('.nameError');
let descriptionError = document.querySelector('.descriptionError');
let form = document.querySelector('form');
let nameOk = false;
let descriptonOk = false;

form.addEventListener('submit', formSubmit)

inputName.addEventListener('focusout', inputNameValidation);
inputDescription.addEventListener('focusout', inputDescriptionValidation);

function inputNameValidation() {
    let errors = 0
    if (inputName.value === '' || inputName.value == null) {
        errors += 1
        nameError.textContent = 'Var god ange användarnamn'

    }
    if (inputName.value.length >= 50) {
        nameError.textContent = 'Användarnamnet är för långt'
        errors += 1
    }

    if (inputName.value.length > 0 && inputName.value.trim().length === 0) {
        nameError.textContent = 'Användarnamn måste innehålla bokstäver'
        errors += 1
    }

    if (errors >= 1) {

        inputName.classList.add('error');
        inputName.classList.remove('valid');
        nameOk = false

    } else {
        inputName.classList.remove('error');
        inputName.classList.add('valid');
        nameError.textContent = '';
        nameOk = true

    }

}
function inputDescriptionValidation() {
    let errors = 0
    if (inputDescription.value === '' || inputDescription.value == null) {
        errors += 1
        descriptionError.textContent = 'Var god ange beskrivning'

    }
    if (inputDescription.value.length >= 5000) {
        descriptionError.textContent = 'Beskrivningen är för långt'
        errors += 1
    }

    if (inputDescription.value.length > 0 && inputDescription.value.trim().length === 0) {
        descriptionError.textContent = 'Beskrivningen måste innehålla bokstäver'
        errors += 1
    }
    if (inputDescription.value.length < 5 && inputDescription.value.trim().length > 0) {
        descriptionError.textContent = 'Beskrivningen är för kort'
        errors += 1
    }


    if (errors >= 1) {

        inputDescription.classList.add('error');
        inputDescription.classList.remove('valid');
        descriptionOk = false

    } else {
        inputDescription.classList.remove('error');
        inputDescription.classList.add('valid');
        descriptionError.textContent = '';
        descriptionOk = true

    }

}

function formSubmit(e) {

    inputNameValidation()
    inputDescriptionValidation()

    if (nameOk & descriptionOk) {
        let o = 1
    } else {
        e.preventDefault()
    }

}

//  ###########  CREATE ROOM FORM ###########

