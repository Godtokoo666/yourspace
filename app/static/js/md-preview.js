document.addEventListener('DOMContentLoaded', (event) => {
    const md = window.markdownit();
    const input = document.getElementById('editor');
    const preview = document.getElementById('preview');

    console.log(input);
    if (input && preview) {
        input.addEventListener('input', () => {
            const markdownText = input.value;
            preview.innerHTML = md.render(markdownText);
        });
    }
});
