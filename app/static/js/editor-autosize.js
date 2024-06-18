document.addEventListener('DOMContentLoaded', (event) => {
    const editor = document.getElementById('editor');
    console.log(editor);
    editor.addEventListener('input', () => {
        editor.style.maxHeight = 'none';
        editor.style.height = 'auto';
        editor.style.maxHeight =`${editor.scrollHeight}px`;
    });
});
