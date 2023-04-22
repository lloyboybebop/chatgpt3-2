document.getElementById('chatgpt-form').addEventListener('submit', function (event) {
    event.preventDefault();

    const prompt = document.getElementById('prompt').value;
    const plugins = Array.from(document.getElementsByName('plugins'))
        .filter(checkbox => checkbox.checked)
        .map(checkbox => checkbox.value)
        .join(',');

    fetch('/generate', {
        method: 'POST',
        body: new FormData(event.target)
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('An error occurred while generating the text.');
        }
    })
    .then(data => {
        document.getElementById('generated-text').textContent = data.generated_text;
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred. Please try again.');
    });
});
