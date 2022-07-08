$('a.like').click(function(e){
    e.preventDefault();
    $.post(
        '{% url "images:like" %}',
        {
            id: $(this).data('id'), 
            action: $(this).data('action')
        },
        function(data){
            if(data['status']=='ok'){
                let previous_action = $('a.like').text();

                // изменяем текст ссылки
                $('a.like').text(previous_action == 'like' ? 'unlike' : 'like');

                // измееняем пользователей которые лайкнули
                let img = $("<img>");
                let p = $("<p>");
                let div = $("<div>");

                img.attr({
                    src: "{{ user.profile.photo.url}}", 
                    alt: ""
                });
                p.text("{{user.first_name}}");

                div.append(img);
                div.append(p);

                previous_action == 'like' ? $(".image-likes").prepend(div) : $('.image-likes div:nth-child(1)').remove();
              

                // Изменяем переменную действия.
                $('a.like').data('action', previous_action == 'like' ? 'unlike': 'like');
                
                $('span.count .total').text(
                    previous_action == 'like' ? parseInt($('span.count .total').text()) + 1: parseInt($('span.count .total').text()) - 1
                );
            }
        })
});