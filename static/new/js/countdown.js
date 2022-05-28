 
const eventBox = document.getElementById('event-box');
const countdownBox = document.getElementById('countdown-box')

//Si da error puede ser porque la fecha no esta siendo enviada en ingles o numero
const eventDate = Date.parse(eventBox.textContent)


const myCountdown = setInterval(()=>{
    const now = new Date().getTime()
    
    const diff = eventDate - now


    const d = Math.floor(eventDate / (1000 * 60 * 60 * 24) - (now / (1000 * 60 * 60 * 24)))
    const h = Math.floor((eventDate / (1000 * 60 * 60) - (now / (1000 * 60 * 60))) % 24)
    const m = Math.floor((eventDate / (1000 * 60) - (now / (1000 * 60))) % 60)
    const s = Math.floor((eventDate / (1000) - (now / (1000))) % 60)

    
    if (diff > 0 ){
        countdownBox.innerHTML = d + " dias, " + h + " horas, " + m + " minutos, " + s + " segundos "
    }else{
        countdownBox.innerHTML = "Subasta cerradaa"
        clearInterval(myCountdown)
    }
    
    }, 1000)

 