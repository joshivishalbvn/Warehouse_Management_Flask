let mediaRecorder;
let audioChunks = [];

async function startRecording(id) {
  
  if (!window.isSecureContext) {
    $('#lg_sidebar_form').removeClass('sidebar-open')
    $.toast({
      text: "This feature only supports in secured site !!!",
      position: 'bottom-right',
      stack: false,
      icon: "error",
    });
    return;
  }

  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  mediaRecorder = new MediaRecorder(stream);

  mediaRecorder.ondataavailable = event => {
    if (event.data.size > 0) {
      audioChunks.push(event.data);
    }
  };

  mediaRecorder.onstop = () => {
    const audioBlob = new Blob(audioChunks);
    const audioUrl = URL.createObjectURL(audioBlob);
    document.getElementById("id_audio"+id).src = audioUrl;
    document.getElementById("play"+id).disabled = false;

    // Set recorded audio as a file for the file input
    let list = new DataTransfer();
    const recordedAudioFile = new File([audioBlob], 'recorded_audio.webm');
    list.items.add(recordedAudioFile);
    if(jobwork_url.includes("create")){
      document.getElementById("id_ordered_product_job_work"+id+"voice_note").files = list.files;
    }
    else{
      document.getElementById("id_voice_note").files = list.files;
    }
    audioChunks = [];
  };

  document.getElementById("start"+id).disabled = true;
  document.getElementById("stop"+id).disabled = false;
  mediaRecorder.start();
  document.getElementById("output"+id).innerHTML = "Recording started...";
}

function stopRecording(id) {
  mediaRecorder.stop();
  document.getElementById("start"+id).disabled = false;
  document.getElementById("stop"+id).disabled = true;
  document.getElementById("output"+id).innerHTML = "Recording stopped ! Click to play button to listen recorded audio clip.";
}

function playRecording(id) {
  document.getElementById("id_audio"+id).play();
  document.getElementById("output"+id).innerHTML = "Playing...";

  document.getElementById("id_audio"+id).addEventListener("ended", function() {
    document.getElementById("output"+id).innerHTML = "To record again, click on record button.";
  });
}