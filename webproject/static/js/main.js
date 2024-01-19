$('.requests__list-item').on('click',(e)=>{
    const textarea=document.getElementById('queryTextArea')
    if($("#queryTextArea").prop('disabled')) return;
    $('.chat__textarea').val($(e.target).text().trim())
    $('.chat__textarea').trigger('focus')
})


$('.chat__btn-send').on('click',sendMessage)
$('.chat__textarea').trigger('focus');
$('.chat__textarea').on('keydown',(e)=> (e.key === 'Enter' && e.shiftKey == false)? $('.chat__btn-send')[0].click():void(0))
$('.chat__textarea').on('input',(e)=>{
    e.target.value = e.target.value=="\n"?"":e.target.value
    !e.target._baseScrollHeight && getScrollHeight(e.target)
    e.target.rows = 1
    rows = Math.ceil((e.target.scrollHeight - e.target._baseScrollHeight) / 16) + 1
    e.target.rows = (rows >=5)? 5 : rows
})

$('#clear_all').on("input",(e)=>{
    let checked = $(e.target).is(':checked')
    $('.chat__checkbox-input').prop('checked', checked);
})

$('.chat__btn-clear').on('click', ()=>{
    list_msg = []
    $('.chat__list-item').each((i,e)=>{
        if($(e).find('.chat__checkbox-input').is(':checked')){
            list_msg.push($(e).attr("id"))
        }
    })

    if(list_msg.length > 0){
        $.ajax({
            url: '/delete/',
            type: 'POST',
            data: { data: JSON.stringify(list_msg)},
            //headers: { 'X-CSRFToken': csrftoken },
            success: function(res) {
                if(res.result == "ok"){
                    $('.chat__list-item').each((i,e)=>{
                        if(list_msg.includes($(e).attr("id"))){
                            $(e).remove()
                        }
                    })
                }
            },
            error: function(xhr, status, error) {

            }, 
            timeout: 60000 // 20 segundos de espera
        });
    }
})

function getScrollHeight(e){
    let savedValue = e.value
    e.value = ''
    e._baseScrollHeight = e.scrollHeight
    e.value = savedValue
}

function sendMessage(){
    const textarea = $('.chat__textarea')
    const premium = $('#conversation').attr("premium") === "True"
    let req = textarea.val();

    if(req.trim() === "") return
    textarea.val("");
    textarea[0].rows = 1;
    
    $.ajax({
        url: '/message/',
        type: 'POST',
        data: { data: JSON.stringify({'role': 'user', 'content': req})},
        //headers: { 'X-CSRFToken': csrftoken },
        success: function(res) {
            addResult(res.data[res.data.length-1].content, true)
            if(res.id != "0") $('.chat__list-message li:last').attr('id',res.id)
            if(!premium) prueba_excedido()         
        },
        error: function(xhr, status, error) {
            error = error === "timeout" ? "Tiempo de espera excedido":""
            addResult(`Ocurrió un error procesando tu consulta: ${error}`, true)
        }, 
        timeout: 60000
    });
    addResult(req, false)
}


function addResult(m,type){
    if(type === true) $(".chat__list-message li:last").html($(".chat__list-message li:last").html() + addResponse(m))
    else $(".chat__list-message").html( $(".chat__list-message").html() + addRequest(m))
     
    $('.chat__textarea').prop("disabled",!type)
    if(type) document.querySelector('.chat__query').removeAttribute("disabled")
    else document.querySelector('.chat__query').setAttribute("disabled","")

    $('.chat__checkbox-input').prop("disabled",!type)

    type === true? $('.chat__textarea').trigger('focus') : void(0)
    showLoading("spinner1",!type)
    scrollToTop();
}

function addRequest(m){
    return (`
    <li class="py-4 mt-2 mx-0 chat__list-item">
        <div class="chat__conversation">
            <div class="chat__checkbox">
                <input class="chat__checkbox-input" type="checkbox">
            </div>
            <div class="chat__result-request">
                <div class=" ps-3 chat__image py-3"><img width="40px" height="40px" src="../static/img/user.jpg"/></div>
                <div class=" pe-4 chat__content py-3"><pre class="message">${m}</pre></div>
            </div>
        </div>
    </li>`);
}

function addResponse(m){
    return (`
   
        <div class="chat__conversation">
            <div class="chat__checkbox-hidden">
            </div>
            <div class="chat__result-response">
                <div class="ps-3 chat__image py-3"><img width="40px" height="40px" src="../static/img/system.jpg"/></div>
                <div class="pe-4 chat__content py-3"><pre class="message">${m}</pre></div>
            </div>
        </div>
    `);
}


function showLoading(id,enable){
    if(enable===true){
        $(`#${id}`).removeAttr("hidden")
    }else{
        $(`#${id}`).attr("hidden","")
    }
}
function scrollToTop(){
    const chat_result = $('.chat__result');
    chat_result.animate({
        scrollTop:chat_result[0].scrollHeight
    }, 500) 
}

function calculateTextareaHeight(textarea) {
    const textareaClone = textarea.cloneNode();
    textareaClone.value = textarea.value;
    textareaClone.style.height = 'auto';
    textareaClone.style.overflow = 'auto';
    textareaClone.style.visibility = 'hidden';
    document.body.appendChild(textareaClone);
    const height = textareaClone.scrollHeight;
    textareaClone.parentNode.removeChild(textareaClone);
    return height;
}

function prueba_excedido(){
    $(".chat__textarea").prop("disabled","true")
    document.querySelector(".chat__query").setAttribute("disabled","")
    $('.chat__alert').html(
        `<div class="mt-2 alert alert-warning alert-dismissible fade show" role="alert">
             Has excedido el periodo de prueba con 1 consulta permitida al bot           
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>`
    )
}


