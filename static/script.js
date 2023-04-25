let isFirstResponse = true;

function generateResponse(event) {
    event.preventDefault();
    const textarea = document.getElementById('conversation');
    const apiKey = document.getElementById('api_key').value;
    const formData = new FormData(event.target);
    formData.append('api_key', apiKey);

    textarea.value += '\n';

    fetch('/', {
        method: 'POST',
        body: formData,
        headers: {
            'Accept': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        textarea.value = data.conversation;
        textarea.scrollTop = textarea.scrollHeight;
    });
}