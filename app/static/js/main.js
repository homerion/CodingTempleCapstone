function new_entry(entry,entry_id,key) {
  return `<div class="list-group-item border-right border-left form-check d-flex pl-5">
    <input class="form-check-input" type="checkbox" name="${entry_id}" id="${key}ent${entry_id}">
    <label class="form-check-label mr-auto" for="${key}ent${entry_id}">
        ${entry}
    </label>
    <img onclick="removeentry()" style="width:1em" src="../static/open_iconic/svg/circle-x.svg" alt='delete'>
  </div>`
}

$("input[type='search']").on('input', event => {
  console.log(event.target.value);
})
$('.card').on('change',":checkbox",event=>{
  let id = event.target.id;
  let name = $(`#${id}`).prop('name');
  let text = $(`label[for=${id}]`).text();
  let labels =  $(`label:contains(${text})`);
  labels.toggleClass('strike');
  if ($(`#${id}`).is(':checked')) {
    $(`label:contains(${text})`).siblings('input').prop('checked',true)
  } else {
    $(`label:contains(${text})`).siblings('input').prop('checked',false)
  }
  $.post('/done',{'entry_id': name},function(response) {
    // alert(response);
  })
  labels.parent().remove();
})
$(".card-header").on('click',event=>{
  $(event.target).closest('.card').hide();
  $('.card').toggleClass('col-md-6 mx-auto');
  $('.container').toggleClass('card-columns');
  $('.container').toggleClass('card-group');
  $(".card").toggle();
})
$(".card-header").on('mouseenter',event=>{
  $(event.target).children('img').show();
})
$(".card-header").on('mouseleave',event=>{
  $(event.target).children('img').hide();
})
$('.card').on('mouseenter',".list-group-item",event=>{
  $(event.target).children('img').show();
})
$('.card').on('mouseleave',".list-group-item",event=>{
  $(event.target).children('img').hide();
})
$('.card').on('submit',event=>{
  event.preventDefault();
  let form = $(event.target);
  // let url = form.attr('action')
  let data = form.serialize();
  let tag = form.prop('id');
  let entry = form.children('input[name="entry"]').val();
  $.post('/newentry',data,function (entry_id) {
    // console.log(tag);
    // console.log(entry);
    var new_line = new_entry(entry,entry_id,tag);
    form.children('.list-group').append(new_line);
    form.children('input[name="entry"]').val('');
  })
})

function decouple() {
  let id = $(event.target).siblings('input').prop('id');
  $.post('/decouple',{'joined_id': id},function(response) {
      // alert(response)
  })
  $(event.target).parent().remove();
}

$('#new').on('submit',event=>{
  console.log('yes');
})
