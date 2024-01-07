function close_onclick(){
    html.innerHTML = '';
    form.style.display = "block";
    preview.style.display = "none";
}

function preview_onclick(){
    fetch("/preview", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            html: html_text.value
        })
    }).then(res => res.json()).then(data => {
        html.innerHTML = data.html || res.text;
        form.style.display = "none";
        preview.style.display = "block";
    })
}

function submit_onclick(){
    let url = new URL(window.location.href);
    url.searchParams.set("html", html_text.value);
    window.location.replace(url);
}

window.onload = () => {
    close_btn.onclick = close_onclick;
    preview_btn.onclick = preview_onclick;
    submit_btn.onclick = submit_onclick;
}