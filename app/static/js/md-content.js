document.addEventListener('DOMContentLoaded', (event) => {
    const md = window.markdownit();
    const articleContent = document.getElementById('article-Content').dataset.content;
    if (articleContent) {
        const markdownContent = md.render(articleContent);
        document.getElementById('article-Content').innerHTML = markdownContent;
    }
});
