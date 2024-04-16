// document.getElementById('send-button').addEventListener('click', function(event) {
//     event.preventDefault(); // Prevent form submission

//     const userQuery = document.getElementById('user-input').value;
//     document.getElementById('user-input').value = '';

//     displayMessage(userQuery, 'user'); 

//     fetch('/query', {
//         method: 'POST',
//         body: new FormData(document.querySelector('form'))
//     })
//     .then(response => response.json())
//     .then(data => {
//         displayMessage(data.answer, 'bot');
//     }); 
// });

// function displayMessage(message, type) {
//     const messagesContainer = document.getElementById('chat-history'); 
//     const messageElement = document.createElement('div');
//     messageElement.classList.add('chat-message', type); 
//     messageElement.textContent = message;
//     messagesContainer.appendChild(messageElement);

//      // Scroll to the bottom
//      messagesContainer.scrollTop = messagesContainer.scrollHeight; 
// }

// // Theme Toggling
// document.getElementById('theme-toggle').addEventListener('click', function() {
//     document.body.classList.toggle('dark-theme');
// });
