
const eventBox = document.getElementById('event-box');
const countdownBox = document.getElementById('countdown-box')
console.log("eventBox")
console.log(eventBox.textContent)
const eventDate = Date.parse(eventBox.textContent)

const myCountdown = setInterval(()=>{
    const now = new Date().getTime()
    
    const diff = eventDate - now
    console.log(now)
    console.log(eventDate)
    console.log(diff)

    const d = Math.floor(eventDate / (1000 * 60 * 60 * 24) - (now / (1000 * 60 * 60 * 24)))
    const h = Math.floor((eventDate / (1000 * 60 * 60) - (now / (1000 * 60 * 60))) % 24)
    const m = Math.floor((eventDate / (1000 * 60) - (now / (1000 * 60))) % 60)
    const s = Math.floor((eventDate / (1000) - (now / (1000))) % 60)
    console.log(d)
    console.log(h)
    console.log(m)
    
    if (diff > 0 ){
        countdownBox.innerHTML = d + " dias, " + h + " horas, " + m + " minutos, " + s + " segundos "
    }else{
        clearInterval(myCountdown)
        countdownBox.innerHTML = "Subasta cerrada"
    }
    
    }, 1000)

 