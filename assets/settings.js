window.addEventListener("load", function () {
    var navbar = document.querySelector(".navbar-nav");

    if (navbar) {
        var li = document.createElement("li");
        li.className = "nav-item";

        var a = document.createElement("a");
        a.className = "nav-link";
        a.href = "/plugins/status-page/user";

        var icon = document.createElement("i");
        icon.className = "fa fa-rss pr-1";

        var text = document.createTextNode("Status");

        a.appendChild(icon);
        a.appendChild(text);

        li.appendChild(a);
        navbar.appendChild(li);
    }
});
