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
