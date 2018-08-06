$("input[type='search']").on('input', event => {
  console.log(event.target.value);
})
// $(":checkbox").change(event=>{
//   let id = event.target.id;
//   $(`label[for=${id}]`).toggleClass('strike');
// })
// $(".form-check").click(event=>{
//   let toggle = $(event.target).children('input').prop('checked');
//   $(event.target).children('input').prop('checked',!toggle);
//   $(event.target).children('label').toggleClass('strike');
// })
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
