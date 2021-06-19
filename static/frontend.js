// When the page has loaded, run a function to attach a submit
// handler to the user input form.
window.onload = function () {
    document.getElementById('ask').onsubmit = async function (e) {
        // Stop the normal form submit process as we are going to 
        // process it here instead.
        e.preventDefault();

        // Get the message that the user typed into the input field.
        const userInput = document.getElementById('message');
        const message = userInput.value;
        
        // Don't do anything if the user didn't type anything in the input field.
        if (message.length === 0) {
            return
        };

        // Add what the user just typed to the current conversation record.
        const currentConversation = document.getElementById('conversation');
        currentConversation.innerHTML = `${currentConversation.innerHTML}<div class = "userMessage">User: ${message}</div>`;

        // Send what the user just typed to the bot backend for processing.
        const response = await fetch(`/message`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: `message=${message}`
        });

        // Get the text response from the bot backend.
        const botResponse = await response.text();

        // Clear the text input ready for the user to type another message.
        userInput.value = '';

        // Add what the bot responded with to the current conversation record.
        currentConversation.innerHTML = `${currentConversation.innerHTML}<div class = "botResponse">${botResponse}</div>`;

        // Force the conversation area to scroll so that the latest messages
        // at the bottom are visible.
        currentConversation.scrollTop = currentConversation.scrollHeight - currentConversation.clientHeight;
    };
}
