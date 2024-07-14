// seperate situation of pdf and none pdf
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
            document.getElementById('answer').innerHTML = `<h2>Answer:</h2><p>${data.answer}</p>`;
        } catch (error) {
            console.error('Error:', error);
            document.getElementById('answer').innerHTML = '<p>An error occurred. Please try again.</p>';
        }
    }
    else {
        try{
        const response = await fetch('/upload/nonepdf/', {
            method: 'POST',
            body: formData
        });
        
            const data = await response.json();
            document.getElementById('answer').innerHTML = `<h2>Answer:</h2><p>${data.answer}</p>`;
        } catch (error) {
            console.error('Error:', error);
            document.getElementById('answer').innerHTML = '<p>An error occurred. Please try again.</p>';
        }
    }
});