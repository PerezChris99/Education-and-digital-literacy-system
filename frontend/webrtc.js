// WebRTC integration for virtual classrooms
// This is a simplified example and requires a signaling server for a complete implementation

let localVideo;
let remoteVideo;
let peerConnection;
let signalingServerUrl = 'ws://localhost:3000'; // Replace with your signaling server URL
let ws;
let isLowBandwidth = false; // Track low bandwidth mode

function startVirtualClassroom() {
    localVideo = document.createElement('video');
    localVideo.autoplay = true;
    localVideo.muted = true;
    document.getElementById('content').appendChild(localVideo);

    remoteVideo = document.createElement('video');
    remoteVideo.autoplay = true;
    document.getElementById('content').appendChild(remoteVideo);

    // Initialize WebSocket connection to the signaling server
    ws = new WebSocket(signalingServerUrl);

    ws.onopen = () => {
        console.log('Connected to signaling server');
    };

    ws.onmessage = (msg) => {
        const message = JSON.parse(msg.data);
        if (message.type === 'offer') {
            handleOffer(message);
        } else if (message.type === 'answer') {
            handleAnswer(message);
        } else if (message.type === 'candidate') {
            handleCandidate(message);
        } else if (message.type === 'hangup') {
            handleHangup();
        }
    };

    ws.onerror = (err) => {
        console.error('WebSocket error:', err);
    };

    ws.onclose = () => {
        console.log('Disconnected from signaling server');
    };

    startLocalStream();
}

function startLocalStream() {
    const constraints = {
        video: isLowBandwidth ? { width: 320, height: 240 } : true, // Reduce resolution in low bandwidth mode
        audio: true
    };

    navigator.mediaDevices.getUserMedia(constraints)
        .then(stream => {
            localVideo.srcObject = stream;
            startPeerConnection(stream);
        })
        .catch(error => {
            console.error('Error accessing media devices:', error);
        });
}

function startPeerConnection(stream) {
    peerConnection = new RTCPeerConnection({
        iceServers: [
            { urls: 'stun:stun.l.google.com:19302' },
            { urls: 'stun:stun1.l.google.com:19302' }
        ]
    });

    stream.getTracks().forEach(track => {
        peerConnection.addTrack(track, stream);
    });

    peerConnection.ontrack = event => {
        remoteVideo.srcObject = event.streams[0];
    };

    peerConnection.onicecandidate = event => {
        if (event.candidate) {
            send({
                type: 'candidate',
                candidate: event.candidate
            });
        }
    };

    peerConnection.oniceconnectionstatechange = () => {
        if (peerConnection.iceConnectionState === 'disconnected') {
            console.log('Peer disconnected');
            handleHangup();
        }
    };

    // If this is the first peer, create an offer
    if (localVideo && remoteVideo) {
        createOffer();
    }
}

function createOffer() {
    peerConnection.createOffer({
        offerToReceiveAudio: true,
        offerToReceiveVideo: true
    })
        .then(offer => peerConnection.setLocalDescription(offer))
        .then(() => {
            send({
                type: 'offer',
                sdp: peerConnection.localDescription
            });
        })
        .catch(error => console.error('Error creating offer:', error));
}

function handleOffer(message) {
    peerConnection.setRemoteDescription(new RTCSessionDescription(message.sdp))
        .then(() => peerConnection.createAnswer())
        .then(answer => peerConnection.setLocalDescription(answer))
        .then(() => {
            send({
                type: 'answer',
                sdp: peerConnection.localDescription
            });
        })
        .catch(error => console.error('Error handling offer:', error));
}

function handleAnswer(message) {
    peerConnection.setRemoteDescription(new RTCSessionDescription(message.sdp))
        .catch(error => console.error('Error handling answer:', error));
}

function handleCandidate(message) {
    peerConnection.addIceCandidate(new RTCIceCandidate(message.candidate))
        .catch(error => console.error('Error handling candidate:', error));
}

function send(message) {
    message.from = 'localUser'; // Replace with a unique identifier
    ws.send(JSON.stringify(message));
}

// Function to toggle low bandwidth mode
function setLowBandwidth(enabled) {
    isLowBandwidth = enabled;
    if (localVideo) {
        localVideo.srcObject.getTracks().forEach(track => {
            track.stop(); // Stop existing stream
        });
        startLocalStream(); // Restart with new constraints
    }
}

function hangUp() {
    send({ type: 'hangup' });
    handleHangup();
}

function handleHangup() {
    console.log('Hanging up.');
    closePeerConnection();
}

function closePeerConnection() {
    if (peerConnection) {
        peerConnection.close();
        peerConnection = null;
    }
    if (remoteVideo) {
        remoteVideo.srcObject = null;
    }
}
