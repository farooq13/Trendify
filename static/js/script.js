function showNotifications(){
  const container = document.getElementById('container');
  if (container.classList.contains('d-none')){
    container.classList.remove('d-none');
  } else {
    container.classList.add('d-none')
  }
};


function getCookie(name){
let cookieValue = null;
if (document.cookie && document.cookie !== ''){
  const cookies = document.cookie.split(';');
  for (i = 0; i < cookies.length; i++){
    const cookie = cookies[i].trim();
    if (cookie.substring(0, name.length + 1) == (name + '=')){
      cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
      break;
    }
  }
};
return cookieValue;
}


function removeNotification(removeNotificationURL, redirectURL){
const csrftoken = getCookie('csrftoken');
let xmlhttp = new XMLHttpRequest();

xmlhttp.onreadystatechange = function(){
  if (xmlhttp.readyState == XMLHttpRequest.DONE){
    if (xmlhttp.status == 200){
      window.location.replace(redirectURL);
    }
  }
};

xmlhttp.open("DELETE", removeNotificationURL, true);
xmlhttp.setRequestHeader("X-CSRFToken", csrftoken);
xmlhttp.send();
}

console.log('Working...');