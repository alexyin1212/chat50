function like(id, user_id) {
    // set variables for the like and dislike button
    let like = document.getElementById("like" + id);
    let dislike = document.getElementById("dislike" + id);
    // set variables for the text (number of karma)
    let counter = document.getElementById("counter" + id)
    // set int varible for the number of karma
    let count = parseInt(counter.innerHTML);
    // set state of like and dislike
    let liked = false;
    let disliked = false;

    // if the liked button is purple
    if (like.classList.contains("on")) {
        // liked status is true
        liked = true;
    }
    // if the disliked button is purple
    else if (dislike.classList.contains("on")) {
        // disliked status is true
        disliked = true;
    }

    // if both buttons are off
    if (liked == false && disliked == false) {
        // make like button purple and increment counter by 1 then set the innerhtml to the counter
        like.classList.add("on");
        count++;
        counter.innerHTML = count;
    }
    // if like button is off but dislike button is on
    else if (liked == false && disliked == true) {
        // make like button purple, dislike button back to grey stage and increment counter by 2 then set the innerhtml to the counter
        like.classList.add("on");
        dislike.classList.remove("on");
        count += 2;
        counter.innerHTML = count;
    }
    // if like button is on
    else {
        // make like button back to grey stage and decrease counter by 1 then set the innerhtml to the counter
        like.classList.remove("on");
        count--;
        counter.innerHTML = count;
    }

    // create a dictionary to pass to json
    var dict = {"likes": count, "post_id": id, "user_id": user_id, "status": "liked"};
    // stringify the dict     
    var dataJson = JSON.stringify(dict);
    
    // use ajax syntax to post the data to /likes
    $.ajax({
        url: "/likes",
        type: "POST",
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        data: dataJson
    });
}



function dislike(id, user_id) {   
    // set variables for the like and dislike button
    let like = document.getElementById("like" + id);
    let dislike = document.getElementById("dislike" + id);
    // set variables for the text (number of karma)
    let counter = document.getElementById("counter" + id)
    // set int varible for the number of karma
    let count = parseInt(counter.innerHTML);
    // set state of like and dislike
    let liked = false;
    let disliked = false;

    // if the liked button is purple
    if (like.classList.contains("on")) {
        // liked status is true
        liked = true;
    }
    // if the disliked button is purple
    else if (dislike.classList.contains("on")) {
        // disliked status is true
        disliked = true;
    }

     // if both buttons are off
    if (liked == false && disliked == false) {
        // make dislike button purple and decrease counter by 1 then set the innerhtml to the counter
        dislike.classList.add("on");
        count--;
        counter.innerHTML = count;
    }
    // if like button is on but dislike button is off
    else if (liked == true && disliked == false) {
        // make dislike button purple, like button back to grey stage and decrease counter by 2 then set the innerhtml to the counter
        dislike.classList.add("on");
        like.classList.remove("on");
        count -= 2;
        counter.innerHTML = count;
    }
    // if dislike button is on
    else {
        // make dislike button back to grey stage and increment counter by 1 then set the innerhtml to the counter
        dislike.classList.remove("on");
        count++;
        counter.innerHTML = count;
    }

    // create a dictionary to pass to json
    var dict = {"likes": count, "post_id": id, "user_id": user_id, "status": "disliked"};
    // stringify the dict     
    var dataJson = JSON.stringify(dict);

    // use ajax syntax to post the data to /likes
    $.ajax({
        url: "/likes",
        type: "POST",
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        data: dataJson
    });
}

