$("input[type='search']").on('input', event => {
  console.log(event.target.value);
})
$(":checkbox").change(event=>{
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
    alert(response);
  })
  labels.parent().remove();
})
$(".card-header").on('click',event=>{
  $(event.target).closest('.card').hide();
  $(".card").toggle().toggleClass('col-6 mx-auto');
})
$(".card-header").mouseenter(event=>{
  $(event.target).children('img').show();
})
$(".card-header").mouseleave(event=>{
  $(event.target).children('img').hide();
})
$(".list-group-item").mouseenter(event=>{
  $(event.target).children('img').show();
})
$(".list-group-item").mouseleave(event=>{
  $(event.target).children('img').hide();
})


function removeentry() {
  let id = $(event.target).siblings('input').prop('id');
  $.post('/decouple',{'joined_id': id},function(response) {
      // alert(response)
  })
  $(event.target).parent().remove();
}
function shownew() {
  $('#new').toggleClass('card');
  $('.card').toggle();
  $(event.target).hide()
}
$('#new').on('submit',event=>{
  console.log('yes');
})

// $("#newitem").on('submit',event=>{
//   event.preventDefault();
//   $.post('/index',this.entry,)
// })

// $( "form" ).on( "submit", function( event ) {
//   event.preventDefault();
//   let input = $( this ).children("[type='text']").val();
//   $("#list").append(`  <div class="form-check">
//       <input class="form-check-input" type="checkbox" value="" id="defaultCheck4">
//       <label class="form-check-label" for="defaultCheck4">
//           ${input}
//       </label>
//     </div>`);
//   $( this ).children("[type='text']").val('');
// });
