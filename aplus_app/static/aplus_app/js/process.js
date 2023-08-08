function openNav(a){
    document.getElementById(a).style.width = "250px";
    document.getElementById("nav-wrapper").style.display = "block"
}


function closeNav(a){
    document.getElementById(a).style.width = "0px"
    document.getElementById("nav-wrapper").style.display = "none"
}




function toast(msg, last, bg, fc){
    let box = document.createElement("toastbox")
    box.innerText = msg

    box.style.backgroundColor = bg
    box.style.color = fc

    document.body.appendChild(box)

    setTimeout(()=>{
        document.body.removeChild(box)
    }, last)

}
