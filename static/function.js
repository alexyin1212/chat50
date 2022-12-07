function like(id, user_id) {
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

    var dict = {"likes": count, "post_id": id, "user_id": user_id, "status": "liked"};    
    var dataJson = JSON.stringify(dict);
    
    $.ajax({
        url: "/likes",
        type: "POST",
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        data: dataJson
    });
}



function dislike(id, user_id) {   
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

    var dict = {"likes": count, "post_id": id, "user_id": user_id, "status": "disliked"};
    var dataJson = JSON.stringify(dict);
    
    $.ajax({
        url: "/likes",
        type: "POST",
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        data: dataJson
    });
}

