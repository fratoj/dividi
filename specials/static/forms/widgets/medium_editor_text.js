$(document).ready(function() {
    var editor = new MediumEditor('.thought__title', {
        toolbar: {
            buttons: ['bold', 'italic', 'underline', 'h1', 'h3', 'quote'],
        },
        placeholder: {
            text: 'Type your title...'
        }
    });
    editor.subscribe('blur', function(event, editable){
        var html = editable.innerHTML.trim();
        var input_el = document.querySelectorAll('input.medium-editor-element')[0];
        input_el.value = html;
    });
    // editor.subscribe('addElement', function(event, editable){
    //     console.log('hi', editable);
    // });
    // editor.on('input.medium-editor-element', 'ValueChange', function (event) {
    //     console.log(event);
    //     debugger;
    // });
    document.querySelectorAll('input.medium-editor-element')[0].hidden = true;
    document.querySelectorAll('input.medium-editor-element')[0].required = false;
    document.querySelector('h1.medium-editor-element').
    document.querySelectorAll('h1.medium-editor-element')[0].innerHTML =
        document.querySelectorAll('input.medium-editor-element')[0].value;
});
