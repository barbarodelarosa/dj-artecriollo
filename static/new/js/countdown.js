
const eventBox = document.getElementById('event-box');
const countdownBox = document.getElementById('countdown-box')

const eventDate = Date.parse(eventBox.textContent)
console.log(eventDate)

const myCountdown = setInterval(()=>{
    const now = new Date().getTime()
    // console.log(now)
    
    const diff = eventDate - now
    // console.log(diff)

    const d = Math.floor(eventDate / (1000 * 60 * 60 * 24) - (now / (1000 * 60 * 60 * 24)))
    const h = Math.floor((eventDate / (1000 * 60 * 60) - (now / (1000 * 60 * 60))) % 24)
    const m = Math.floor((eventDate / (1000 * 60) - (now / (1000 * 60))) % 60)
    const s = Math.floor((eventDate / (1000) - (now / (1000))) % 60)
    console.log(s)

    if (diff > 0 ){
        countdownBox.innerHTML = d + " dias, " + h + " horas, " + m + " minutos, " + s + " segundos "
    }else{
        clearInterval(myCountdown)
        countdownBox.innerHTML = "Conteo regresivo completado"
    }

}, 1000)