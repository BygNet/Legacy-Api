// Like Post
const likeButtons = document.querySelectorAll('button.likes')
likeButtons.forEach(button => {
  button.addEventListener('click', event => {
    event.stopPropagation()
    event.preventDefault()

    let likesIndicator = button.querySelector('span')
    let data = button.dataset
    let formData = new FormData()

    formData.append('postId', data.id)
    fetch('/like-post', {
      method: 'POST',
      body: formData
    }).then(() => {
      let likes = parseInt(likesIndicator.textContent)
      likesIndicator.textContent = String(likes + 1)
    })
  })
})
