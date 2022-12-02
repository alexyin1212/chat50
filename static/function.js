function like(id) {
    let like = document.getElementById("like" + id);
    let dislike = document.getElementById("dislike" + id);
    let counter = document.getElementById("counter" + id)
    let count = parseInt(counter.innerHTML);
    let liked = false;
    let disliked = false;

    if (like.classList.contains("on")) {
        liked = true;
    }
    else if (dislike.classList.contains("on")) {
        disliked = true;
    }

    if (liked == false && disliked == false) {
        like.classList.add("on");
        count++;
        counter.innerHTML = count;
    }
    else if (liked == false && disliked == true) {
        like.classList.add("on");
        dislike.classList.remove("on");
        count += 2;
        counter.innerHTML = count;
    }
    else {
        like.classList.remove("on");
        count--;
        counter.innerHTML = count;
    }
}



function dislike(id) {   
    let like = document.getElementById("like" + id);
    let dislike = document.getElementById("dislike" + id);
    let counter = document.getElementById("counter" + id)
    let count = parseInt(counter.innerHTML);
    let liked = false;
    let disliked = false;

    if (like.classList.contains("on")) {
        liked = true;
    }
    else if (dislike.classList.contains("on")) {
        disliked = true;
    }

    if (liked == false && disliked == false) {
        dislike.classList.add("on");
        count--;
        counter.innerHTML = count;
    }
    else if (liked == true && disliked == false) {
        dislike.classList.add("on");
        like.classList.remove("on");
        count -= 2;
        counter.innerHTML = count;
    }
    else {
        dislike.classList.remove("on");
        count++;
        counter.innerHTML = count;
    }
}

function change_color(id) {
    let name = document.getElementById(id).name
    if (name == "dark") {
        .body {
            background-color: rgb(35, 35, 35);
            color: rgb(255, 255, 255);
        }
    }
    else if (name == "purple") {
        .body {
            background-color: rgb(227, 194, 255);
            color: rgb(255, 255, 255);
        }
    }
    else {
        .body {
            background-color: rgb(233, 233, 233);
            color: 'black';
        }
    }
    
}
    