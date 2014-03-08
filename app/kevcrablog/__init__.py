# Blog Post Markdown editor tags
MARKDOWN_PRE_HTML = '''
<div class="markdown">
'''

MARKDOWN_POST_HTML = '''
</div>
<script type="text/javascript">
    converter = new Showdown.converter();
    $(document).ready(function() {
        updateLivePost = function() {
            inputText = $("#markdown-input").val()
            $("#markdown-preview").html(converter.makeHtml(inputText));
            $('pre code').each(function(i, e) { hljs.highlightBlock(e) });
        };
        updateLivePost();
        $("#markdown-input").on("keyup", updateLivePost);
    });
</script>
'''