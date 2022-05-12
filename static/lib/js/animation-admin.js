
function toggleShow(idPubContainer) {
  $(".pubs_container_one_type#"+idPubContainer).toggleClass('show');
  $(".result_type_container#"+idPubContainer+" .triangle_to_open_and_hide").toggleClass('dontShow');
}

function really_delete_pub(pub_id) {
  name = $('table tr#'+ pub_id +' .preview_and_pub_name a.name').html();
  $('.question_block h1').html('Вы точно хотите удалить публикацию «'+ name +'»?');
  $('.cancel_or_delete a').attr('href', '/pub/delete/'+pub_id);
  $('.pub_additional_functions_bg, .question_block').addClass('show');
}

function really_delete_account(user_id) {
  name = $('table tr#'+ user_id +' .info_container a.name').html();
  $('.question_block h1').html('Вы точно хотите удалить пользователя «'+ name +'»?');
  $('.cancel_or_delete a').attr('href', '/account/'+ user_id +'/delete/');
  $('.pub_additional_functions_bg, .question_block').addClass('show');
}

function really_delete_category(category_id) {
  category_name = $('table.categories tr#'+ category_id +' td.name').html();
  tags_in_category_count = $('table.categories tr#'+ category_id +' .this_category_tags li').length;
  // pubs_with_tags_in_category_count = $('table.tags .pubs["category_id='+ category_id +'"] li').length;
  $('.delete_tag_or_tag_category input[name="tag_or_category_to_delete"]').val('category')
  $('.delete_tag_or_tag_category input[name="object_id"]').val(category_id)
  $('.delete_tag_or_tag_category .title').html('Вы точно хотите удалить категорию «'+ category_name +'»?');
  $('.delete_tag_or_tag_category .description').html('Вы уверены, что не будете потом об этом жалеть? Это нельзя будет восстановить. Также с этой категорией будет удалено '+ tags_in_category_count +' тегов этой категории, а публикации с ними их потеряют. Точно это Вам нужно?');
  $('.create_or_edit_tag_or_tag_category').css('width','29%');
  $('.create_or_edit_tag_or_tag_category').css('left','35%');
  $('.create_or_edit_tag_or_tag_category').css('top','30%');
  $('.delete_tag_or_tag_category button#delete').html('Удалить категорию');
  $('.pub_additional_functions_bg, .question_block.delete_tag_or_tag_category').addClass('show');
}

function really_delete_tag(tag_id) {
  tag_name = $('table.tags tr#'+ tag_id +' td.name').html();
  pubs_with_this_tag_count = $('table.tags tr#'+ tag_id +' .pubs li').length;
  $('.delete_tag_or_tag_category input[name="tag_or_category_to_delete"]').val('tag')
  $('.delete_tag_or_tag_category input[name="object_id"]').val(tag_id)
  $('.delete_tag_or_tag_category .title').html('Вы точно хотите удалить тег «'+ tag_name +'»?');
  $('.delete_tag_or_tag_category .description').html('Вы уверены, что не будете потом об этом жалеть? Это нельзя будет восстановить. Также с удалением этого тега '+ pubs_with_this_tag_count +' публикаций останутся без них. Точно это Вам нужно?');
  $('.create_or_edit_tag_or_tag_category').css('width','auto');
  $('.create_or_edit_tag_or_tag_category').css('left','41%');
  $('.create_or_edit_tag_or_tag_category').css('top','20%');
  $('.delete_tag_or_tag_category button#delete').html('Удалить тег');
  $('.pub_additional_functions_bg, .question_block.delete_tag_or_tag_category').addClass('show');
}

$('.create_new.category').on('click', function() {
  $('.create_or_edit_tag_or_tag_category h1.title').html('Новая категория:');
  $('.create_or_edit_tag_or_tag_category button#create_or_edit').html('Создать категорию');
  $('.create_or_edit_tag_or_tag_category').css('width','29%');
  $('.create_or_edit_tag_or_tag_category').css('left','36%');
  $('.create_or_edit_tag_or_tag_category').css('top','30%');
  $('.create_or_edit_tag_or_tag_category input[name="to_create_or_edit"]').val('create');
  $('.create_or_edit_tag_or_tag_category input[name="tag_or_category_to_create_or_edit"]').val('category');
  $('.pub_additional_functions_bg, .question_block.create_or_edit_tag_or_tag_category, .category_or_tag_name').addClass('show');
});

$('.create_new.tag').on('click', function() {
  $('.create_or_edit_tag_or_tag_category h1.title').html('Новый тег:');
  $('.create_or_edit_tag_or_tag_category button#create_or_edit').html('Создать тег');
  $('.create_or_edit_tag_or_tag_category').css('width','auto');
  $('.create_or_edit_tag_or_tag_category').css('left','30%');
  $('.create_or_edit_tag_or_tag_category').css('top','20%');
  $('.create_or_edit_tag_or_tag_category input[name="to_create_or_edit"]').val('create');
  $('.create_or_edit_tag_or_tag_category input[name="tag_or_category_to_create_or_edit"]').val('tag');
  $('.pub_additional_functions_bg, .question_block.create_or_edit_tag_or_tag_category, .category_or_tag_name, .title.category, select.category, .title.pub_types, label.one_pub_type').addClass('show');
});

function edit_category(category_id) {
  category_name = $('table.categories tr#'+ category_id +' td.name').html();
  $('.create_or_edit_tag_or_tag_category h1.title').html('Редактирование категории «'+ category_name +'»');
  $('.create_or_edit_tag_or_tag_category button#create_or_edit').html('Отредактирвать категорию');
  $('.create_or_edit_tag_or_tag_category').css('width','39%');
  $('.create_or_edit_tag_or_tag_category').css('left','31%');
  $('.create_or_edit_tag_or_tag_category').css('top','30%');
  $('.create_or_edit_tag_or_tag_category input[name="to_create_or_edit"]').val('edit');
  $('.create_or_edit_tag_or_tag_category input[name="tag_or_category_to_create_or_edit"]').val('category');
  $('.create_or_edit_tag_or_tag_category input[name="object_id"]').val(category_id);
  $('.create_or_edit_tag_or_tag_category input[name="category_or_tag_name"]').val(category_name);
  $('.pub_additional_functions_bg, .question_block.create_or_edit_tag_or_tag_category, .category_or_tag_name').addClass('show');
}
function edit_tag(tag_id) {
  tag_name = $('table.tags tr#'+ tag_id +' td.name').html();
  $('.create_or_edit_tag_or_tag_category h1.title').html('Редактирование тега «'+ tag_name +'»');
  $('.create_or_edit_tag_or_tag_category button#create_or_edit').html('Отредактирвать тег');
  $('.create_or_edit_tag_or_tag_category').css('width','auto');
  $('.create_or_edit_tag_or_tag_category').css('left','30%');
  $('.create_or_edit_tag_or_tag_category').css('top','20%');
  $('.create_or_edit_tag_or_tag_category input[name="to_create_or_edit"]').val('edit');
  $('.create_or_edit_tag_or_tag_category input[name="tag_or_category_to_create_or_edit"]').val('tag');
  $('.create_or_edit_tag_or_tag_category input[name="object_id"]').val(tag_id);
  $('.create_or_edit_tag_or_tag_category input[name="category_or_tag_name"]').val(tag_name);
  $('.question_block select').val($('table.tags tr#'+ tag_id +' td.category')[0].id);
  $.each($('table.tags tr#'+ tag_id +' .pub_types p'), function(){
    $('.question_block input[value="'+ this.id +'"].pub_type').prop('checked', true);
  });
  $('.pub_additional_functions_bg, .question_block.create_or_edit_tag_or_tag_category, .category_or_tag_name, .title.category, select.category, .title.pub_types, label.one_pub_type').addClass('show');
}

$('.pub_additional_functions_bg').on('click', function(e) {
  if (!($(e.target).hasClass("dont_close_on_click"))) {
    $('.pub_additional_functions_bg, .question_block, .question_block.create_or_edit_tag_or_tag_category, .category_or_tag_name, .title.category, select.category, .title.pub_types, label.one_pub_type').removeClass('show');
    $('.question_block input[name="category_or_tag_name"]').val('');
    $('.question_block input').prop('checked', false);
    $('.question_block select').val(1);
  }
});
