window.addEventListener("load", function () {
    var navbar = document.querySelector(".navbar-nav");

    if (navbar) {
        var li = document.createElement("li");
        li.className = "nav-item";

        var a = document.createElement("a");
        a.className = "nav-link";
        a.href = "/plugins/status-page/user";
        a.innerText = "Status";

        li.appendChild(a);
        navbar.appendChild(li);
    }
});
