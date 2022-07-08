let page=1;
let empty_page = false;
let block_request = false;

$(window).on("scroll", function(){
    let margin = $(document).height() - $(window).height() - 200;
    if($(window).scrollTop() > margin && !empty_page && !block_request){
        block_request = true;
        page += 1;
        $.get(`?page=${page}`, function(data){
            if(data=''){
                empty_page = true;
            }else{
                block_request = false;
                console.log(data);
                $('#action-list').html(data);
            }
        });
    }
})