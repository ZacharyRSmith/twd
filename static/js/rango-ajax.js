$(document).ready(function(){
    $('#like').click(function(){
        catid = $(this).attr("data-catid");
        $.get('/rango/like_category/', {category_id: catid}, function(data){
            $('#like_count').html(data);
            $('#like').hide();
        });
    });

    $('#suggestion').keyup(function(){
        query_in = $(this).val();
        $.get('/rango/suggest_category/', {query: query_in}, function(cat_list){
            $('#cats').html(cat_list);
        });
    });
});
