const myImage = document.querySelector("img");

myImage.onclick = () => {
  const mySrc = myImage.getAttribute("src");
  if (mySrc === "static/images/enkor.jpg") {
    myImage.setAttribute("src", "static/images/enkor2.jpg");
  } else {
    myImage.setAttribute("src", "static/images/enkor.jpg");
  }
};

let myButton = document.querySelector("button");
let myHeading = document.querySelector("h1");

function setUserName() {
  const myName = prompt("Введите своё имя.");
  if (!myName) {
    setUserName();
  } else {
    localStorage.setItem("name", myName);
    myHeading.textContent = `Добро пожаловать, ${myName}`;
  }
}

if (!localStorage.getItem("name")) {
  setUserName();
} else {
  const storedName = localStorage.getItem("name");
  myHeading.textContent = `Добро пожаловать, ${storedName}`;
}

myButton.onclick = () => {
  setUserName();
};