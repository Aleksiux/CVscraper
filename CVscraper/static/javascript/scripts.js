
//----------------------------------------------Like on cvs------------------------------------------------------------


const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
const buttons = document.querySelectorAll(".heart-like-button");
buttons.forEach(button => {
  button.addEventListener("click", (e) => {
    if (button.classList.contains("liked")) {
      button.classList.remove("liked");
      removeFromLikeSection(e);
    } else {
      button.classList.add("liked");
      addToLikeSection(e);
    }
  });
});

function addToLikeSection(e) {
  let cv_id = e.currentTarget.dataset.cvId;
  let url = "cv/add_to_like_section";

  let data = { cv_id: cv_id };

  fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json", 'X-CSRFToken': csrftoken },
    body: JSON.stringify(data)
  })
    .then(res => res.json())
    .then(data => {
      document.getElementById("like_section").innerHTML = data;
      console.log(data);
    })
    .catch(error => {
      console.log(error);
    });
}

function removeFromLikeSection(e) {
  let cv_id = e.currentTarget.dataset.cvId;
  let url = "cv/remove_from_like_section";

  let data = { cv_id: cv_id };

  fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json", 'X-CSRFToken': csrftoken },
    body: JSON.stringify(data)
  })
    .then(res => res.json())
    .then(data => {
      document.getElementById("like_section").innerHTML = data;
      console.log(data);
    })
    .catch(error => {
      console.log(error);
    });
}

