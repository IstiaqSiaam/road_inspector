const form = document.getElementById("upload-form");
const input = document.getElementById("video-input");
const status = document.getElementById("status");
const video = document.getElementById("output-video");

form.addEventListener("submit", async e => {
  e.preventDefault();
  status.innerText = "Uploading and processing...";
  video.style.display = "none";

  const data = new FormData();
  data.append("file", input.files[0]);

  const resp = await fetch("/upload-video/", {
    method: "POST",
    body: data
  });

  if (!resp.ok) {
    status.innerText = "Error processing video.";
    return;
  }

  const blob = await resp.blob();
  const url  = URL.createObjectURL(blob);
  video.src = url;
  video.style.display = "block";
  status.innerText = "Done!";
});
