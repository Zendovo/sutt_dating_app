const chatId = JSON.parse(document.getElementById('chat-id').textContent)
const senderName = JSON.parse(document.getElementById('first-name').textContent) + ' ' + JSON.parse(document.getElementById('last-name').textContent)
const loc = 'ws://' + window.location.host + '/ws/chat/' + chatId + '/'

const chatSocket = new WebSocket(loc)

chatSocket.onopen = function (e) {
    console.log(e);
};

chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);

    const message = document.createElement('div')
    message.className = 'message row mt-2'
    const msgSender = document.createElement('div')
    msgSender.className = 'row fw-bold px-4'
    msgSender.innerHTML = data.sender
    const msgContent = document.createElement('div')
    msgContent.className = 'row px-4'
    msgContent.innerHTML = data.message

    message.appendChild(msgSender)
    message.appendChild(msgContent)

    document.getElementById('messages').appendChild(message);

    msgDiv = document.getElementById('messages')
    msgDiv.scrollTop += 100000
};

chatSocket.onclose = function (e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function (e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function (e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;

    if (message == '') {
        return
    }

    chatSocket.send(JSON.stringify({
        'message': message,
        'sender': senderName
    }));
    messageInputDom.value = '';
};