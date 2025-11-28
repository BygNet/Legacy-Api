const adNames = [
    "PolybuzzAd", "ExplosionsAd", "NewStepAd", "RevolutAd", "ZeldaAd", "DiscordAd"
]

// Open Create Modal
let createButton = document.querySelector('button#createButton')
createButton.addEventListener('click', () => {
  document.querySelector('#createModal').classList.remove('hidden')
})

// Close Create Modal
document.querySelector('button#cancelButton').addEventListener('click', () => {
  document.querySelector('#createModal').classList.add('hidden')
})

document.querySelector('#createForm').addEventListener('submit', e => {
  e.preventDefault()

  let formData = new FormData(e.target)

  fetch('/create-post', {
    method: 'POST',
    body: formData
  }).then(() => {
    window.location.reload()
  })
})

// Open Upload Modal
let uploadButton = document.querySelector('button#uploadImageButton')
uploadButton.addEventListener('click', () => {
  document.querySelector('#uploadImageModal').classList.remove('hidden')
})

// Close Upload Modal
document.querySelector('button#cancelUploadButton').addEventListener('click', () => {
  document.querySelector('#uploadImageModal').classList.add('hidden')
})

document.querySelector('#uploadForm').addEventListener('submit', e => {
  e.preventDefault()

  let formData = new FormData(e.target)

  fetch('/upload-image', {
    method: 'POST',
    body: formData
  }).then(() => {
    window.location.reload()
  })
})

// Cycle Images
const adBanner = document.querySelector('img#bannerAdBar')

let adIndex = 0
function cycleAds() {
  adIndex = (adIndex + 1) % adNames.length
  adBanner.src = `/static/ads/${adNames[adIndex]}.jpg`
}
setInterval(cycleAds, 4000)

adBanner.addEventListener('click', () => {
    window.location.href = '/upgrade'
})
