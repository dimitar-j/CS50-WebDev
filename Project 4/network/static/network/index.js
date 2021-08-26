let page = 0
let has_next = false
let has_prev = false
let user = ""

document.addEventListener('DOMContentLoaded', function(){
    change_page(1)
    document.getElementById('next').addEventListener('click', function(){
        change_page(1)})
    document.getElementById('prev').addEventListener('click', function(){
        change_page(-1)})
})

function change_page(x){
    page += x
    console.log(`Changing to page: ${page}`)
    fetch(`/posts?page=${page}`)
    .then(response => response.json())
    .then(data => {
        has_next = data['has_next']
        has_prev = data['has_prev']
        user = data['user']
        update_buttons()
        clear_posts()
        data.posts.forEach(add_post)
    })
    window.scrollTo(0, 0)
    return false
}

function update_buttons(){
    next_bttn = document.getElementById('next')
    prev_bttn = document.getElementById('prev')

    if (has_next){
        next_bttn.disabled=false
    }else{
        next_bttn.disabled=true
    }
    if (has_prev){
        prev_bttn.disabled=false
    }else{
        prev_bttn.disabled=true
    }

}

function clear_posts(){
    document.querySelector('#posts').innerHTML = ""
}

function add_post(post){
    // Create container div
    const container = document.createElement('div')
    container.className = "container"

    // Create and add card div
    const card = document.createElement('div')
    card.className = "card"
    container.appendChild(card)

    // Create author h4 with link
    const author = document.createElement('h4')
    const a = document.createElement('a')
    a.setAttribute("href", `/${post[0]}`)
    a.innerHTML = post[0]
    author.appendChild(a)

    // Create content div
    const content = document.createElement('div')
    content.innerHTML = post[1]

    // Create text area for editing content
    const editArea = document.createElement('textarea')
    editArea.className = 'form-control'
    editArea.style.display = 'none'

    // Create edit button
    const edit = document.createElement('a')
    edit.innerHTML = "Edit post"
    edit.className = "link-primary"
    edit.href = "javascript: void(0)"
    edit.style.display = 'none'

    // Create save/discard changes buttons
    const saveDiscardDiv =  document.createElement('div')
    saveDiscardDiv.style.display = 'none'
    const save = document.createElement('button')
    save.className = "btn btn-primary"
    save.innerHTML = "Save Changes"
    save.style.display = 'inline-block'
    save.style.marginRight = '10px'
    const discard = document.createElement('button')
    discard.className = 'btn btn-danger'
    discard.style.display = 'inline-block'
    discard.innerHTML = "Discard Changes"
    saveDiscardDiv.appendChild(save)
    saveDiscardDiv.appendChild(discard)

    // Create like image div with heart image and like count text
    let postLiked = post[4]
    console.log(`Post liked by user: ${postLiked}`)
    const image = document.createElement('div')
    const heart = document.createElement('img')
    if (postLiked === true){
        heart.src = "\\static\\network\\heart_red.jpg"
    }else{
        heart.src = "\\static\\network\\heart_white.jpg"
    }
    heart.width = "30"
    heart.height = "30"
    heart.style = "float: left; margin-right: 5px;"
    heart.id = "heart"
    heart.style.animationPlayState = 'paused'
    image.appendChild(heart)
    const likes = document.createElement('div')
    likes.style = "padding-top: 3px;"
    let numLikes = post[3]
    if (numLikes === 1){
        likes.innerHTML = "1 Like"
    }else{
        likes.innerHTML = `${numLikes} Likes`
    }

    // Create timestampt div
    const timestamp = document.createElement('div')
    timestamp.className = "timestamp"
    timestamp.innerHTML = post[2]

    // Check if current user is author of post
    console.log(user)
    if (user === post[0]){
        edit.style.display = 'block'
        edit.addEventListener('click', function(){
            // Verify user again, in case user edited HTML in order to reveal 'edit' button
            if (user === post[0]){
                let text = content.innerHTML
                content.style.display = 'none'
                editArea.style.display = 'block'
                edit.style.display = 'none'
                editArea.value = text
                saveDiscardDiv.style.display = 'block'
            }
        })
    }

    // Check if user saved changes to post
    save.addEventListener('click', function(){
        let text = editArea.value
        saveDiscardDiv.style.display = 'none'
        edit.style.display = 'block'
        editArea.style.display = 'none'
        content.style.display = 'block'
        content.innerHTML = text
        fetch(`/edit/${post[5]}`, {
            method: "PUT",
            body: JSON.stringify({
                newContent: text
            })
        })
        
    })

    // Check if user discarded changes to post
    discard.addEventListener('click', function(){
        saveDiscardDiv.style.display = 'none'
        edit.style.display = 'block'
        editArea.style.display = 'none'
        content.style.display = 'block'
    })

    // Check if user liked/unliked post
    heart.addEventListener('click', function(){
        if (user !== ""){
            // Play like/unline animation
            if (postLiked){
                heart.style.animationName = 'unlike'
            }else{
                heart.style.animationName = 'like'
            }
            heart.style.animationPlayState = 'running'

            // Update image and like counter
            if (postLiked){
                heart.src = "\\static\\network\\heart_white.jpg"
                postLiked = false
                numLikes -= 1
            }else{
                heart.src = "\\static\\network\\heart_red.jpg"
                postLiked = true
                numLikes += 1
            }

            // Update like counter text
            if (numLikes === 1){
                likes.innerHTML = "1 Like"
            }else{
                likes.innerHTML = `${numLikes} Likes`
            }
            fetch(`/edit/${post[5]}`, {
                method: "PUT",
                body: JSON.stringify({
                    numLikes: numLikes,
                    liked: postLiked
                })
            })
        }
    })

    // Add new elements to DOM
    card.appendChild(author)
    card.appendChild(content)
    card.appendChild(editArea)
    card.appendChild(document.createElement('br'))
    card.appendChild(edit)
    card.append(saveDiscardDiv)
    if (user === post[0]){
        card.appendChild(document.createElement('br'))   
    }
    image.appendChild(likes)
    card.appendChild(image)
    card.appendChild(document.createElement('hr'))
    card.appendChild(timestamp)
    document.querySelector('#posts').append(container)
    document.querySelector('#posts').append(document.createElement('br'))

}