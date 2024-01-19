$('#username').trigger('focus')

let timer;
startTimer();
$('.login__button').prop("disabled","true")

function focusButton(){
    if($('#username').val().trim() != "" && $('#password').val().trim() != ""){
        $('.login__button').removeAttr("disabled")
        //$('.login__button').trigger('focus')
    }else{
        $('.login__button').prop("disabled","true")
    }
}
function restartTimer() {
    clearTimeout(timer);
    startTimer();
 }
 
function startTimer() {
    timer = setTimeout(focusButton, 777); 
}

$('#username').on('input',restartTimer)
$('#password').on('input',restartTimer)



