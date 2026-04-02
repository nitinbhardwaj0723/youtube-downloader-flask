async function fetchInfo() {
    const url = document.getElementById("youtubeUrl").value;
    const errorBox = document.getElementById("error");
    const videoInfo = document.getElementById("videoInfo");

    errorBox.innerText = "";
    videoInfo.classList.add("hidden");

    if (!url) {
        errorBox.innerText = "Please enter a YouTube URL";
        return;
    }

    const formData = new FormData();
    formData.append("url", url);

    const response = await fetch("/get_info", {
        method: "POST",
        body: formData
    });

    const data = await response.json();

    if (data.error) {
        errorBox.innerText = data.error;
        return;
    }

    document.getElementById("thumbnail").src = data.thumbnail;
    document.getElementById("title").innerText = data.title;
    document.getElementById("uploader").innerText = data.uploader;
    document.getElementById("duration").innerText = data.duration;
    document.getElementById("videoUrl1").value = data.url;
    document.getElementById("videoUrl2").value = data.url;

    videoInfo.classList.remove("hidden");
}