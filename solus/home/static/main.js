const q = document.getElementById("search")
const change = document.getElementById("change")
const postBody = document.getElementById("postBody")
const comment = document.getElementById("comment")
const post_id = document.getElementsByClassName("post_id")
const commentButton = document.getElementById("commentButton")
const post_pic = document.getElementsByClassName("post_pic")
var searchAjax = new XMLHttpRequest

function ajaxPOST(data, url){  
    searchAjax.open('POST', url, true)
    searchAjax.setRequestHeader('X-CSRFToken',cook)
    searchAjax.setRequestHeader("X-Requested-With",'XMLHttpRequest')
    searchAjax.setRequestHeader("Content-Type", "application/x-www-form-urlencoded")
    searchAjax.responseType = 'document'
    searchAjax.send("search="+data)
    searchAjax.addEventListener("load",() => {
        changeFunc()
    })
    searchAjax.addEventListener("progress", () => {
        change.innerHTML = "Loading"
    })
}
q.addEventListener("keyup",(key) =>{
    if(q.value == ""){document.getElementById("change").style.display = "none" ;
    }
    if(key.which >65 && key.which < 90){
        if(document.location.pathname == "/"){
            ajaxPOST(q.value,'q/search')
        }else{
            ajaxPOST(q.value,"search")
        }
}  
})

function changeFunc(){
    if(q.value != ""){
        change.innerHTML =searchAjax.responseXML.body.innerHTML
        change.style.display = "block"
    }
    else{
        change.innerHTML = ""
    }
}
function confirm(event){
    change.innerText = event
}

function sub(){
    console.log("Form submitted");
    
}

function post_iter(obj,id){
    let objs = document.getElementById(obj)
    let pic = document.getElementById(id)
    console.log(objs)
}

function formClose(){
    let modal = document.getElementById("modal")
    modal.style.display = "none"
}

function addPic(){
    let postForm = document.getElementById("postForm")
    let p = document.createElement("p")
    let add = document.getElementById("add")   
    if(document.getElementById("pic9")){
        add.style.display = "none"
    }else if(document.getElementById("pic8")){
        let newElement = document.createElement("input")
        newElement.setAttribute("type", "file")
        newElement.setAttribute("name","pic9")
        newElement.setAttribute("id","pic9")
        postForm.insertBefore(newElement, add)
        let pic9 = document.getElementById("pic9")
        postForm.insertBefore(p,pic9)
        postForm.insertBefore(p, add)

    }
    else if(document.getElementById("pic7")){
        let newElement = document.createElement("input")
        newElement.setAttribute("type", "file")
        newElement.setAttribute("name","pic8")
        newElement.setAttribute("id","pic8")
        postForm.insertBefore(newElement, add)
        let pic8 = document.getElementById("pic8")
        postForm.insertBefore(p,pic8)
        postForm.insertBefore(p, add)

    }else if(document.getElementById("pic6")){
        let newElement = document.createElement("input")
        newElement.setAttribute("type", "file")
        newElement.setAttribute("name","pic7")
        newElement.setAttribute("id","pic7")
        postForm.insertBefore(newElement, add)
        let pic7 = document.getElementById("pic7")
        postForm.insertBefore(p,pic7)
        postForm.insertBefore(p, add)

    }else if(document.getElementById("pic5")){
        let newElement = document.createElement("input")
        newElement.setAttribute("type", "file")
        newElement.setAttribute("name","pic6")
        newElement.setAttribute("id","pic6")
        postForm.insertBefore(newElement, add)
        let pic6 = document.getElementById("pic6")
        postForm.insertBefore(p,pic6)
        postForm.insertBefore(p, add)

    }else if(document.getElementById("pic4")){
        let newElement = document.createElement("input")
        newElement.setAttribute("type", "file")
        newElement.setAttribute("name","pic5")
        newElement.setAttribute("id","pic5")
        postForm.insertBefore(newElement, add)
        let pic5 = document.getElementById("pic5")
        postForm.insertBefore(p,pic5)
        postForm.insertBefore(p, add)

    }else if(document.getElementById("pic3")){
        let newElement = document.createElement("input")
        newElement.setAttribute("type", "file")
        newElement.setAttribute("name","pic4")
        newElement.setAttribute("id","pic4")
        postForm.insertBefore(newElement, add)
        let pic4 = document.getElementById("pic4")
        postForm.insertBefore(p,pic4)
        postForm.insertBefore(p, add)

    }else if(document.getElementById("pic2")){
        let newElement = document.createElement("input")
        newElement.setAttribute("type", "file")
        newElement.setAttribute("name","pic3")
        newElement.setAttribute("id","pic3")
        postForm.insertBefore(newElement, add)
        let pic3 = document.getElementById("pic3")
        postForm.insertBefore(p,pic3)
        postForm.insertBefore(p, add)

    }else if(document.getElementById("pic1")){
        let newElement = document.createElement("input")
        newElement.setAttribute("type", "file")
        newElement.setAttribute("name","pic2")
        newElement.setAttribute("id","pic2")
        postForm.insertBefore(newElement, add)
        let pic2 = document.getElementById("pic2")
        postForm.insertBefore(p,pic2)
        postForm.insertBefore(p, add)

    }else if(document.getElementById("pic")){
        let newElement = document.createElement("input")
        newElement.setAttribute("type", "file")
        newElement.setAttribute("name","pic1")
        newElement.setAttribute("id","pic1")
        postForm.insertBefore(newElement, add)
        postForm.insertBefore(p,pic1)
        postForm.insertBefore(p, add)
        
    }else{
        let newElement = document.createElement("input")
        newElement.setAttribute("type", "file")
        newElement.setAttribute("name","pic")   
        newElement.setAttribute("id","pic")
        newElement.setAttribute("onchange","picFunc()")
        postForm.insertBefore(newElement, add)
        postForm.insertBefore(p, add)

    }
 
}
 
function textAreaFunc(){
    if(! document.getElementById("postFormSubmit")){
        let postForm = document.getElementById("postForm")
        let newElement = document.createElement("input")
        let p = document.createElement("p")
        newElement.setAttribute("type","submit")
        newElement.setAttribute("value","Post")
        newElement.setAttribute("class","btn btn-default")
        newElement.setAttribute("id","postFormSubmit")
        postForm.appendChild(newElement)
        let submit = document.getElementById("postFormSubmit")
        postForm.insertBefore(p,submit)
    }   
    
}

function picFunc(){
    let newElement = document.createElement("input")
    let postForm = document.getElementById("postForm")
    let p = document.createElement("p")
    newElement.setAttribute("type","submit")
    newElement.setAttribute("class","btn btn-primary")
    newElement.setAttribute("value","Post")
    newElement.setAttribute("id","post")
    postForm.appendChild(newElement)
    let post = document.getElementById("post")
    postForm.insertBefore(p,post)
}

function reportFunc(post){
    let likeAjax = new XMLHttpRequest
    likeAjax.open("POST","createreport" ,true)
    likeAjax.setRequestHeader("X-CSRFToken", cook)
    likeAjax.setRequestHeader("Content-Type", "application/x-www-form-urlencoded")
    likeAjax.send("post="+id)
    likeAjax.addEventListener("error",(error) => {
        console.log("An error occurred")
    })
    
}
function likeFunc(id){
    let likeAjax = new XMLHttpRequest
    likeAjax.open("POST","createlike" ,true)
    likeAjax.setRequestHeader("X-CSRFToken", cook)
    likeAjax.setRequestHeader("Content-Type", "application/x-www-form-urlencoded")
    likeAjax.send("post="+id)
    likeAjax.addEventListener("error",(error) => {
        console.log("A error occurred")
    })
    likeAjax.addEventListener("load",()=>{
        postFunc(id)
    })
}

function unLikeFunc(id){
    let unLikeAjax = new XMLHttpRequest
    unLikeAjax.open("POST","unlike" ,true)
    unLikeAjax.setRequestHeader("X-CSRFToken", cook)
    unLikeAjax.setRequestHeader("Content-Type", "application/x-www-form-urlencoded")
    unLikeAjax.send("post="+id)
    unLikeAjax.addEventListener("error",(error) => {
        console.log("A error occurred")
    })
    unLikeAjax.addEventListener("load",()=>{
        postFunc(id)
    })
}

function submit(){
    console.log("Submitted");
}

function commentFunc(event,id){
    let ajax = new XMLHttpRequest
    let comment = document.getElementById("comment"+id)
    ajax.open("POST","createcomment")
    ajax.setRequestHeader("X-CSRFToken", cook) 
    ajax.setRequestHeader("Content-Type", "application/x-www-form-urlencoded")   
    ajax.send("post="+id+"&"+"comment="+comment.value)
    ajax.addEventListener("loadend",()=>{
        comment.value = null
        comment.blur()
        postFunc(id)
    })
    event.preventDefault()
}

function postUpdate(event, id ){
    let pic9 = document.getElementById("pic9"+id)
    let pic8 = document.getElementById("pic8"+id)
    let pic7 = document.getElementById("pic7"+id)
    let pic6 = document.getElementById("pic6"+id)
    let pic5 = document.getElementById("pic5"+id)
    let pic4 = document.getElementById("pic4"+id)
    let pic3 = document.getElementById("pic3"+id)
    let pic2 = document.getElementById("pic2"+id)
    let pic1 = document.getElementById("pic1"+id)
    let pic = document.getElementById("pic"+id)
    let pics = [pic, pic1, pic2, pic3, pic4, pic5, pic6, pic7, pic8, pic9]
    for(item of pics){
        if(item){
            if(item.alt){
                if(pics.indexOf(item)==0){
                    document.querySelector("#pic").value == "" ?
                    document.querySelector("#pic").value = item.alt:
                    null
                }else{
                    let picVal = document.querySelector("#pic"+pics.indexOf(item).value)
                    picVal.value == "" ?
                    document.querySelector("#pic"+pics.indexOf(item)).value = item.alt:
                    null
                }               
            }else {
                if(pics.indexOf(item)==0){
                    document.querySelector("#pic").value == "" ?
                    document.querySelector("#pic").value=item.innerHTML:
                    null
                }else{
                    document.querySelector("#pic"+pics.indexOf(item).value) == "" ?
                    document.querySelector("#pic"+pics.indexOf(item)).value =item.innerHTML:null
                }
            }
        }
    }
    event.preventDefault()
}

function closeModal(){
    let modal = document.getElementsByClassName("modal")
    modal[0].style.display ="none"
}
function showNotifications() {
    document.querySelector("#notificationDetails").style.display == "block"?
    document.querySelector("#notificationDetails").style.display = "none":
    document.querySelector("#notificationDetails").style.display = "block"
}
function confirmation(){
    if(document.querySelector("#password").value !== document.querySelector("#confirm").value){
    console.log(document.querySelector("#password").value,document.querySelector("#confirm").value);
    document.querySelector("#warn").innerText = "Passwords did not match"        
    }else{
    document.querySelector("#warn").innerText = ""
    }  
}
// setInterval(()=>{
//     let e = document.querySelector("#ro").style.transform
//     console.log(e);
// },1000) 

