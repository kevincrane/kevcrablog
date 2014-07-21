/**
 * Javascript functions for general use
 * @author: Kevin Crane
 */

// Convert Markdown to a syntax-highlighted blog post
markdownToHtml = function (inputText, converter) {
    var postHtml = converter.makeHtml(inputText);
    $(postHtml).find('pre code').each(
        function (i, block) {
            hljs.highlightBlock(block)
        }
    );
    return postHtml;
};

// Create HTML to display a preview of a post on the blog homepage
postPreviewHtml = function (title, body, created) {
    var previewHtml = "<div class='post-preview'>\n";
    previewHtml += "<h3 class='post-preview-title'>" + title + "</h3>\n";
    previewHtml += "<p class='post-preview-body'>" + markdownToHtml(body) + "</p>\n";
    previewHtml += "<h6 class='post-preview-created'>Created <i>" + created + "</i></h6>\n";
    return previewHtml;
};