const video = document.getElementById('video');

// Start webcam
navigator.mediaDevices.getUserMedia({ video: true })
  .then((stream) => {
    video.srcObject = stream;
  });

function captureAndSend() {
  const canvas = document.createElement('canvas');
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  canvas.getContext('2d').drawImage(video, 0, 0);

  const image = canvas.toDataURL('image/jpeg');

  fetch('/verify', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ image: image })
  })
  .then(response => response.json())
  .then(data => {
    if (data.authenticated) {
      window.location.href = "https://shefiyyahaurll.github.io/Nena-Cake/";
    } else {
      alert("Wajah tidak dikenali!");
    }
  });
}
