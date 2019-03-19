$(document).ready(function() {
    new MediumEditor('.thought__content', {
        toolbar: {
            buttons: ['bold', 'italic', 'underline', 'h3'],
        },
        placeholder: {
            text: 'Type your thought...'
        }
    });
});
