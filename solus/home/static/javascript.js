var cook = Cookies.get('csrftoken')
function detailFunc(id){
    var modal = document.getElementsByClassName("modal")
    var detailAjax = new XMLHttpRequest 
    detailAjax.open("GET","post/"+id,true)
    detailAjax.setRequestHeader("HTTP_X_REQUESTED_WITH","XMLHttpRequest")
    detailAjax.responseType = "document"    
    detailAjax.send()
    detailAjax.addEventListener("load",()=>{
        modal[0].innerHTML = detailAjax.responseXML.body.innerHTML
        modal[0].style.display="block"
        var close = document.getElementById("detailClose")
            document.contains(close) ? close.addEventListener("click",function(){
            modal[0].style.display = "none"}): null;
    })   
}
function commentFunc(post,post_content){
    var post_id = document.getElementById(post_content)
    var commentAjax = new XMLHttpRequest     
    commentAjax.open("POST", "createcomment",true)
    commentAjax.setRequestHeader('X-CSRFToken',cook)
    commentAjax.setRequestHeader("Content-Type", "application/x-www-form-urlencoded")
    commentAjax.responseType = "document"
    commentAjax.send("comment="+post_id.value+"&post="+post)
    commentAjax.addEventListener("load",function(){
        post_id.value = ''
        change.innerHTML = "Comment posted"
        setTimeout(function(){
            change.innerHTML = ""
        },2000)
    })
    commentAjax.addEventListener("error", (error) => {
        console.log("An error occurred");  
    })    
}

function morecomment(page){
    var comment_div = document.getElementById("comment_div")
    var morecommentsAjax = new XMLHttpRequest
    morecommentsAjax.open("GET", page,true)
    morecommentsAjax.responseType = "document"
    morecommentsAjax.send()
}

function moreposts(page){
    var morepostsAjax = new XMLHttpRequest
    var post_container = document.getElementsByClassName("post_container")
    morepostsAjax.open("GET", page,true)
    morepostsAjax.responseType = "document"
    morepostsAjax.setRequestHeader("X-Requested-With",'XMLHttpRequest')
    morepostsAjax.setRequestHeader("Accept","text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8")
    morepostsAjax.responseType = "document"
    morepostsAjax.send()
    morepostsAjax.addEventListener("error",(err)=>{console.log(err);
    })
    morepostsAjax.addEventListener("load",function(){
        post_container[0].innerHTML += morepostsAjax.responseXML.body.innerHTML
        post_container[0].removeChild(document.querySelector("#nextPage"))
    })
}

function nextSlider(id,pic, ...args){
    var arr = [pic]
    var postPic = document.getElementById("pic"+id) 
    var prevButton = document.getElementById("prev"+id)
    var nextButton = document.getElementById("next"+id)
    var indicator = document.getElementById('indicator'+id)
    var mediaContainer = document.getElementById("mediaContainer"+id)
    var vid = document.createElement("video")
    var img = document.createElement("img")
    var playButton =document.createElement("button")
    var seek = document.createElement("p")
    vid.setAttribute("id","vid"+id)
    vid.setAttribute("class","card-img-bottom")
    playButton.setAttribute("id","playButton"+id)
    playButton.setAttribute("class","playButton")
    playButton.innerText="Play"
    seek.setAttribute("id","seek"+id)
    seek.setAttribute("class","seek")
    img.setAttribute("id","pic"+id)
    img.setAttribute("class", "card-img-bottom")
    for(var i = 0; i < args.length;i++){
        if(args[i] !== "/media/None"){
            arr.push(args[i])
        }
    }
    if(mediaContainer.contains(postPic)){
        var current = arr.indexOf(postPic.attributes.src.value)
        current < arr.length -1 ? current++ : current = arr.length -1
        if(arr[current].endsWith("mpd")){
            mediaContainer.replaceChild(vid,postPic)
            mediaContainer.contains(seek) ?null:mediaContainer.appendChild(seek)
            mediaContainer.contains(seek)?null:mediaContainer.insertBefore(vid,seek)
            mediaContainer.contains(playButton)?null:mediaContainer.appendChild(playButton)
            mediaContainer.contains(playButton)?null:mediaContainer.insertBefore(playButton,seek)
            initPlayer("vid"+id,arr[current],id)
        }else{
            postPic.setAttribute("src",arr[current])
        }
        indicator.style.display = "block"
        indicator.innerText = String(current+1)+"/"+String(arr.length)
        current == 0 ? prevButton.style.display = "none":prevButton.style.display = "block"
        current == arr.length -1 ? nextButton.style.display = "none": nextButton.style.display = "block"   
    }else{
        var currentSrc = arr[indicator.innerText[0]]
        var current = arr.indexOf(currentSrc)
        console.log(indicator.innerText);
        if(arr[current].endsWith("mpd")){
            indicator.style.display = "block"
            indicator.innerText = String(current+1)+"/"+String(arr.length)
            current == 0 ? prevButton.style.display = "none":prevButton.style.display = "block"
            current == arr.length -1 ? nextButton.style.display = "none": nextButton.style.display = "block" 
            initPlayer("vid"+id,arr[current],id)
        }else{
            
            mediaContainer.replaceChild(img,mediaContainer.querySelector("#"+vid.attributes.id.value))
            img.setAttribute("src",arr[current])
            indicator.style.display = "block"
            mediaContainer.removeChild(mediaContainer.querySelector("#"+playButton.attributes.id.value))
            mediaContainer.removeChild(mediaContainer.querySelector("#"+seek.attributes.id.value))
            indicator.innerText = String(current+1)+"/"+String(arr.length)
            current == 0 ? prevButton.style.display = "none":prevButton.style.display = "block"
            current == arr.length -1 ? nextButton.style.display = "none": nextButton.style.display = "block" 
        }
    }
}

function prevSlider(id,pic, ...args){
    var arr = [pic]
    var postPic = document.getElementById("pic"+id) 
    var prevButton = document.getElementById("prev"+id)
    var nextButton = document.getElementById("next"+id)
    var indicator = document.getElementById('indicator'+id)
    var mediaContainer = document.getElementById("mediaContainer"+id)
    var vid = document.createElement("video")
    var img = document.createElement("img")
    var playButton =document.createElement("button")
    var seek = document.createElement("p")
    vid.setAttribute("id","vid"+id)
    vid.setAttribute("class","card-img-bottom")
    playButton.setAttribute("id","playButton"+id)
    playButton.setAttribute("class","playButton")
    playButton.innerText="Play"
    seek.setAttribute("id","seek"+id)
    seek.setAttribute("class","seek")
    img.setAttribute("id","pic"+id)
    img.setAttribute("class", "card-img-bottom")
    for(var i = 0; i < args.length;i++){
        if(args[i] !== "/media/None"){
            arr.push(args[i])
        }
    }
    
    if(mediaContainer.contains(postPic)){
        var current = arr.indexOf(postPic.attributes.src.value)
        current < arr.length -1 ? current-1 : null;
        if(arr[current-1].endsWith("mpd")){
            mediaContainer.replaceChild(vid,postPic)
            mediaContainer.contains(seek) ?null:mediaContainer.appendChild(seek)
            mediaContainer.contains(seek)?null:mediaContainer.insertBefore(vid,seek)
            mediaContainer.contains(playButton)?null:mediaContainer.appendChild(playButton)
            mediaContainer.contains(playButton)?null:mediaContainer.insertBefore(playButton,seek)
            initPlayer("vid"+id,arr[current-1],id)
        }else{
            current == arr.length - 1 ? postPic.setAttribute("src",arr[current - 1])
            : postPic.setAttribute("src",arr[current -1])
            }
        indicator.style.display = "block"
        current == arr.length - 1 ? indicator.innerText = String(current)+"/"+String(arr.length):
        null
        current < arr.length - 1 ? indicator.innerText = String(current)+"/"+String(arr.length):
        current == 0 ? prevButton.style.display = "none":prevButton.style.display = "block"
        current == arr.length -1 ? nextButton.style.display = "none": nextButton.style.display = "block"
        if(indicator.innerText[0]==1){
            prevButton.style.display="none"
            nextButton.style.display="block"}   
    }else{
        var currentSrc = arr[indicator.innerText[0]]
        var current = arr.indexOf(currentSrc)-1
        if(arr[current-1].endsWith("mpd")){
            indicator.style.display = "block"
            indicator.innerText = String(current)+"/"+String(arr.length)
            current == arr.length - 1 ? indicator.innerText = String(current)+"/"+String(arr.length):
            null
            current == 0 ? prevButton.style.display = "none":prevButton.style.display = "block"
            current == arr.length -1 ? nextButton.style.display = "none": nextButton.style.display = "block" 
            if(indicator.innerText[0]==1){
                prevButton.style.display="none"
                nextButton.style.display="block"} 
            initPlayer("vid"+id,arr[current-1],id)
        }else{
            mediaContainer.replaceChild(img,mediaContainer.querySelector("#"+vid.attributes.id.value))
            img.setAttribute("src",arr[current-1])
            indicator.style.display = "block"
            mediaContainer.removeChild(mediaContainer.querySelector("#"+playButton.attributes.id.value))
            mediaContainer.removeChild(mediaContainer.querySelector("#"+seek.attributes.id.value))
            indicator.innerText = String(current)+"/"+String(arr.length)
            current === 0 ? prevButton.style.display = "none":prevButton.style.display = "block"
            current === arr.length -1 ? nextButton.style.display = "none": nextButton.style.display = "block"
        }
    }
}

function profilePostsFunc(page) {
    var profilePostAjax = new XMLHttpRequest
    var profilePostContainer = document.getElementsByClassName("profilePostContainer")
    profilePostAjax.open("GET", page, true)
    profilePostAjax.setRequestHeader("X-Requested-With",'XMLHttpRequest')
    profilePostAjax.responseType = "document"
    profilePostAjax.send()
    profilePostAjax.addEventListener("load", function(){
        profilePostContainer[0].innerHTML = profilePostAjax.responseXML.body.innerHTML
    })
    profilePostAjax.addEventListener("error",(error) =>{
        console.log(error)
    })
    
}

function menu(id){
    var form = document.getElementById("form"+id)
    if(form.style.display == "none"){
        form.style.display = "block"
    }else{
        form.style.display = "none"
    }
}

function getNotifications(){
    var ajax = new XMLHttpRequest()
    var notificationsContainer = document.getElementById("notificationDetails")
    ajax.open("GET", "/notifications",true)
    ajax.responseType = "document"
    ajax.send()
    ajax.addEventListener("load",function(){
        notificationsContainer.innerHTML+=ajax.responseXML.body.innerHTML
        document.querySelector("#notification_length").innerHTML = document.querySelector("#length").innerHTML
    })
}

function createPost(){
    var modal = document.getElementById("modal")
    modal.style.display = "block"
}

function showSearch(){
    var searchForm = document.getElementById("searchForm");
    var searchButton = document.getElementById("showSearch");
    searchForm.style.display = "block"
    if(searchButton.innerText == "Hide"){
        searchForm.style.display = "none"
        searchButton.innerText = "Search"
    }else{
        searchButton.innerText = "Hide"
    }
}
function pinfo(post, elementAjax){
    var info = document.getElementById("info"+post)
    var newElement = document.createElement("div")
    var table = document.createElement("table")
    var liketd = document.createElement("td")
    var reportTd = document.createElement("td")
    var ajaxTd = document.createElement("td")
    var like = document.createElement("div")
    var report = document.createElement("div")
    var p = document.createElement("p")
    var tr = document.createElement("tr")
    ajaxTd.setAttribute("class", "postComments postCommentsContainer")
    reportTd.setAttribute("class","float-right")
    reportTd.setAttribute("style", "margin-right:1% width:100%")
    liketd.setAttribute("width", "34%")
    like.setAttribute("class","like")
    report.setAttribute("class", "btn btn-primary report")
    report.setAttribute("onclick", "reportFunc(post)".replace("post",post))
    table.setAttribute("class","container-fluid")
    report.setAttribute("class", "report")
    if(elementAjax.endsWith("True")){
        like.innerHTML = '<ion-icon name="thumbs-down" size="large"></ion-icon>'
    }else{
        like.innerHTML = '<ion-icon name="thumbs-up" size="large"></ion-icon>'
    }
    if(like.innerHTML == '<ion-icon name="thumbs-down" size="large"></ion-icon> <p>unLike</p>'){
        like.setAttribute("onclick", "unLikeFunc(post)".replace("post",post))
    }else{
        like.setAttribute("onclick", "likeFunc(post)".replace("post",post))
    }
    report.innerHTML='<ion-icon name="remove-circle" size="large"></ion-icon>'
    ajaxTd.innerText = elementAjax.replace("True","").replace("False","")
    reportTd.appendChild(report)
    liketd.appendChild(like)
    tr.appendChild(liketd)
    tr.appendChild(ajaxTd)
    tr.appendChild(reportTd)
    table.appendChild(tr)
    newElement.appendChild(table)
    info.innerHTML = newElement.innerHTML
    newElement.appendChild(p)
}

function postFunc(post){
    var postInfoAjax = new XMLHttpRequest
    postInfoAjax.open("GET", "postinfo/"+post, true)
    postInfoAjax.responseType = "document"
    postInfoAjax.send()
    postInfoAjax.addEventListener("load", function(){
        pinfo(post,postInfoAjax.responseXML.body.innerText)    
    })
}
function initApp(){
    shaka.polyfill.installAll()
    if(shaka.Player.isBrowserSupported()){
        initPlayer()
    }else{
        console.log("Unsupported browser");
        
    }
}

function initPlayer(vid,vurl,id){
    var video = document.getElementById(vid);
    var player = new shaka.Player(video)
    var seek = document.getElementById("seek"+id)
    var playButton = document.getElementById("playButton"+id)
    video.setAttribute("src",vurl)
    video.addEventListener("canplay",()=>{
        video.play()
    })
    
    window.player = player
    player.addEventListener("error", onErrorEvent)
    player.configure({
        streaming:{
            bufferingGoal:10,
            rebufferingGoal:5
        }
    })
   
    video.addEventListener("loadstart",()=>{
        playButton.innerHTML='<ion-icon name="cog" size="large"></ion-icon>'
        playButton.style.animation="slider 1.4s 0s infinite"
        
    }) 
    video.addEventListener("loadeddata", ()=>{
        playButton.innerHTML = '<ion-icon name="play" size="large"></ion-icon>'
    })
    video.addEventListener("dblclick",()=>{ 
        if(navigator.userAgent.search("Firefox")!=-1){
            video.mozRequestFullScreen()
        }else{
            video.webkitRequestFullScreen()
        }
    })
    video.onplaying=()=>{  
        setInterval(()=>{
            video.duration > 59 ?
            seek.innerText = String(((video.currentTime)/59).toFixed(1))[0]+":"+video.currentTime.toFixed(0)%59
            +"/"+String(((video.duration)/59).toFixed(1))[0]+":"+String((video.duration%60).toFixed(1))[0]: 
            seek.innerText="0:"+video.currentTime.toFixed(0)+"/"+"0:"+video.duration.toFixed(0)             
        },1000)
        if(video.currentTime===video.duration){
            playButton.innerHTML = '<ion-icon name="play" size="large"></ion-icon>';
        } 
        playButton.style.animation=""
        playButton.innerHTML = '<ion-icon name="pause" size="large"></ion-icon>'
        playButton.onclick=()=>{ 
            if(playButton.innerHTML==('<ion-icon name="pause" size="large" role="img" class="icon-large hydrated" aria-label="pause"></ion-icon>')){
                
                video.pause()
                playButton.innerHTML = '<ion-icon name="play" size="large"></ion-icon>'
            }else{
                video.play()
                playButton.innerHTML = '<ion-icon name="pause" size="large"></ion-icon>'
            }
        }
    }
    player.load(vurl).then(() =>{
    }).catch(onErorr)
}
function playButton(vid,vurl){
    var video =document.getElementById("vid"+vid)
    if(video.played.length < 1){
        initPlayer("vid"+vid,vurl,vid)
    }
   
}

function onErrorEvent(error){
    onError(error)
}
function onErorr(error){
    console.error("Error code ", error.code, error)
}


function posterFunc(vUrl,vId){
    var video = document.getElementById("vid"+vId)
    video.setAttribute("poster",vUrl.replace("mpd","jpg"))
}
