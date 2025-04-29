
(() => {
  const image = document.querySelector(".image");
  const app_screen = document.querySelector(".app");
  const lock_screen = document.querySelector(".login");
  const notification = document.querySelector(".notification");
  const login_not=document.querySelector("#login_notification")
  const status = document.querySelector(".status");
  const password = document.querySelector(".password");
  const styles = getComputedStyle(document.documentElement);
  const open = document.querySelector(".open-button");
  const close = document.querySelector(".close-button");
  document.querySelector(".password-submit").addEventListener("click",onPasswordSubmit);
  open.addEventListener("click", onOpen);
  close.addEventListener("click", onClose);

  document.getElementById('myForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevents the page from reloading
    myFunction();
  });

  document.getElementById('forgot-password').addEventListener('click', function(event) {
    event.preventDefault(); // Prevents the page from reloading
    fetch("/forget-password", { method: "get" }).then(async ()=>{
        login_not.innerText = "Password sent to your phone number";
        login_not.style.transform = "scaleY(1)";
        setTimeout(() => (login_not.style.transform = "scaleY(0)"), 5000);
    })
  });

  function myFunction() {
    const inputValue = document.getElementById('myInput').value;
    fetch("/emergency-unlock", {
      method: "post",
      body: JSON.stringify({ password: inputValue }),
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
      },
    }).then(async (res) => {
      const resp = await res.json();
      if(res.status==400){
        notification.innerText = "Password do not match";
      }
      else{
        notification.innerText = "Door unlocked";
        status.innerText = "Open";
        status.style.borderColor = styles.getPropertyValue("--open");
        status.style.color = styles.getPropertyValue("--open");
      }
        open.disabled = false;
        notification.style.transform = "scaleY(1)";
        setTimeout(() => (notification.style.transform = "scaleY(0)"), 5000);
    })
    .catch(() => {
      open.disabled = false;
    });
  }

  function register_user(){

  }

  
  function screen_apper() {
    lock_screen.style.display = "none";
    app_screen.style.display = "flex";
    notification.style.transform = "scaleY(1)";
    notification.innerText = "Logged In";
    setTimeout(() => (notification.style.transform = "scaleY(0)"), 5000);
    status.innerText = "Open";
    status.style.borderColor = styles.getPropertyValue("--open");
    status.style.color = styles.getPropertyValue("--open");
    fetch("/status", { method: "get" }).then(async (req) => {
      let requ = await req.json();
      if (requ.msg == "Open") {
        status.innerText = "Open";

        status.style.borderColor = styles.getPropertyValue("--open");
        status.style.color = styles.getPropertyValue("--open");
      } else {
        status.innerText = "Locked";
        status.style.borderColor = styles.getPropertyValue("--close");
        status.style.color = styles.getPropertyValue("--close");
      }
    });
    getting_data();
  }

  function onPasswordSubmit(e) {
    e.preventDefault();
    e.target.disabled=true
    login_not.innerText = "Logging In";
    login_not.style.transform = "scaleY(1)";
    
    fetch("/login", {
      method: "post",
      body: JSON.stringify({ password: password.value }),
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then(async (res) => {
        e.target.disabled=false
        const resp = await res.json();
        if (resp.msg == "success") {
          screen_apper();
        }
        else{
          login_not.innerText="Incorrect Password"
        }
        setTimeout(() => login_not.style.transform = "scaleY(0)", 3000);
      })
      .catch((e)=>{
        login_not.innerText="Error try again"
        setTimeout(() => login_not.style.transform = "scaleY(0)", 3000);
      });
  }

  function onOpen() {
    open.disabled = true;
    fetch("/open-lock", { method: "get" })
      .then(async (res) => {
        const resp = await res.json();
        if(res.status==400){
          notification.innerText = "FaceId donot match";
        }
        else{
          notification.innerText = "Door unlocked";
          status.innerText = "Open";
          status.style.borderColor = styles.getPropertyValue("--open");
          status.style.color = styles.getPropertyValue("--open");
        }
          open.disabled = false;
          notification.style.transform = "scaleY(1)";
          setTimeout(() => (notification.style.transform = "scaleY(0)"), 5000);
      })
      .catch(() => {
        open.disabled = false;
      });
  }

  function onClose() {
    close.disabled = true;
    fetch("/close-lock", { method: "get" })
      .then(async (res) => {
        const resp = await res.json();
        close.disabled = false;
        if (resp.msg == "Lock closed")
          notification.style.transform = "scaleY(1)";
        notification.innerText = "Door locked";
        setTimeout(() => (notification.style.transform = "scaleY(0)"), 5000);
        status.innerText = "Locked";
        status.style.borderColor = styles.getPropertyValue("--close");
        status.style.color = styles.getPropertyValue("--close");
      })
      .catch(() => {
        close.disabled = false;
      });
  }

  function getting_data() {
    const socket = new WebSocket("ws://127.0.0.1:8000/camera");

    socket.onopen = function () {
      notification.innerText = "Connection established";
      notification.style.backgroundColor = styles.getPropertyValue("--open");
      notification.style.transform = "scaleY(1)";

      setTimeout(() => (notification.style.transform = "scaleY(0)"), 5000);
    };

    socket.onmessage = async function (event) {
      const arrayData = event.data;
      const blob = new Blob([arrayData]);
      const url = URL.createObjectURL(blob);
      image.src = url;
    };

    socket.onclose = function () {
      notification.innerText = "Connection closed";
      status.innerText = "X";
      status.style.borderColor = styles.getPropertyValue("--close");
      status.style.color = styles.getPropertyValue("--close");
      notification.style.backgroundColor = styles.getPropertyValue("--close");
      notification.style.transform = "scaleY(1)";
      setTimeout(() => (notification.style.transform = "scaleY(0)"), 5000);
    };

    socket.onerror = function (error) {
      notification.innerText = "Error occured closed";
      notification.style.transform = "scaleY(1)";
      setTimeout(() => (notification.style.transform = "scaleY(0)"), 5000);
    };

    socket.send("Hello");
  }
})();
