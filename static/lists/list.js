window.TddLists = {};


window.TddLists.initialize = function(params) {
    $('input[name="text"]').on('keypress click', () => {
        $('.has-error').hide();
    });

    if (params) {
        window.TddLists.updateItems(params.listApiUrl);

        let form = $('#id_item_form');
        form.on('submit', function (event) {
            event.preventDefault();

            $.post(params.itemsApiUrl, {
                'list': params.listId,
                'text': form.find('input[name="text"]').val(),
                'csrfmiddlewaretoken': form.find('input[name="csrfmiddlewaretoken"]').val(),
            }).done(function () {
                $('.has-error').hide();
                window.TddLists.updateItems(params.listApiUrl);
                form.find('input[name="text"]').val('');
            }).fail(function (xhr) {
                $('.has-error').show();

                let responseJSON = JSON.parse(xhr.responseText);
                let errorText;
                if (responseJSON.text || responseJSON.non_field_errors)
                    errorText = responseJSON.text || responseJSON.non_field_errors;
                else
                    errorText = 'Error talking to server. Please try again.';
                $('.has-error .help-block').text(errorText);
            });
        });
    }
};


window.TddLists.updateItems = function (url) {
    $.get(url).done(function(response) {
        let rows = '';
        if (response.items && response.items.length > 0){
            for (let i=0; i<response.items.length; i++) {
                let item = response.items[i];
                rows += '\n<tr><td>' + (i+1) + ': ' + item.text + '</td></tr>';
            }
        }
        $('#id_list_table').html(rows);
    });
};
