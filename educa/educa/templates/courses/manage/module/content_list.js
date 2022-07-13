$('#modules').sortable({
    stop: function(event, ui) {
        modules_order = {};
        $('#modules').children().each(function(){
            // Обновляем поле порядкового номера.
            $(this).find('.order').text($(this).index() + 1);
            // Связываем порядковый номер с идентификатором объекта.
            modules_order[$(this).data('id')] = $(this).index();
    });
    $.ajax({
        type: 'POST',
        url: '{% url "module_order" %}',
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        data: JSON.stringify(modules_order)
    });
    }
});

$('#module-contents').sortable({
    stop: function(event, ui) {
        contents_order = {};
        $('#module-contents').children().each(function(){
            // Связываем порядковый номер с идентификатором объекта.
            contents_order[$(this).data('id')] = $(this).index();
        });
        $.ajax({
            type: 'POST',
            url: '{% url "content_order" %}',
            contentType: 'application/json; charset=utf-8',
            dataType: 'json',
            data: JSON.stringify(contents_order),
        });
    }   
});