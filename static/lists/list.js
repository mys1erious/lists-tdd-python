window.TddBook = {};
window.TddBook.initialize = function() {
    $('input[name="text"]').on('keypress click', () => {
        $('.has-error').hide();
    });
};
