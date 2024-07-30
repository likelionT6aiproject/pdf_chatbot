document.addEventListener('DOMContentLoaded', (event) => {
    localStorage.removeItem('conversation');
});

document.getElementById('uploadForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const userId = document.getElementById('userId').value;
    const pdfFile = document.getElementById('pdfFile').files[0];
    const question = document.getElementById('question').value;

    const formData = new FormData();
    formData.append('user_id', userId);
    formData.append('question', question);
    
    if (pdfFile) {
        formData.append('pdf', pdfFile);
        try {
            const response = await fetch('/upload/', {
                method: 'POST',
                body: formData
            });
    
            const data = await response.json();
            const answer = data.answer;
            addConversation(userId, question, answer);
        } catch (error) {
            console.error('Error:', error);
            addConversation(userId, question, 'An error occurred. Please try again.');
        }
    } else {
        try {
            const response = await fetch('/upload/nonepdf/', {
                method: 'POST',
                body: formData
            });
    
            const data = await response.json();
            const answer = data.answer;
            addConversation(userId, question, answer);
        } catch (error) {
            console.error('Error:', error);
            addConversation(userId, question, 'An error occurred. Please try again.');
        }
    }
});

function addConversation(userId, question, answer) {
    const conversationDiv = document.getElementById('conversation');
    const conversationItem = document.createElement('div');
    conversationItem.innerHTML = `<h3>User ID: ${userId}</h3><p><strong>Question:</strong> ${question}</p><p><strong>Answer:</strong> ${answer}</p>`;
    conversationDiv.appendChild(conversationItem);
}

function saveConversation(userId, question, answer) {
    let conversation = localStorage.getItem('conversation');
    conversation = conversation ? JSON.parse(conversation) : [];
    conversation.push({ userId, question, answer });
    localStorage.setItem('conversation', JSON.stringify(conversation));
}

function loadConversation() {
    const conversationDiv = document.getElementById('conversation');
    const conversation = localStorage.getItem('conversation');
    if (conversation) {
        JSON.parse(conversation).forEach(item => {
            const conversationItem = document.createElement('div');
            conversationItem.innerHTML = `<h3>User ID: ${item.userId}</h3><p><strong>Question:</strong> ${item.question}</p><p><strong>Answer:</strong> ${item.answer}</p>`;
            conversationDiv.appendChild(conversationItem);
        });
    }
}
