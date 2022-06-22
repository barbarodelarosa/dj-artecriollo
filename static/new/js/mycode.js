

$('#myModal').on('shown.bs.modal', function () {
    $('#myInput').focus()
  })


  // $('#myModalAuction').on('shown.bs.modal', function () {
  //   $('#myInputAuction').focus()
  // })


  $('#myTabs a').click(function (e) {
    e.preventDefault()
    $(this).tab('show')
  })

  $('#example').DataTable();



  $('#myTabs a').click(function (e) {
    e.preventDefault()
    $(this).tab('show')
  })


  function updateIndicator() {
    console.log(window.navigator.onLine);
	  alert(window.navigator.onLine);
  }
  window.addEventListener('online',  updateIndicator);
  window.addEventListener('offline', updateIndicator);


//   function load() {
//     var el = document.getElementById("t");
//     el.addEventListener("click", modifyText, false);
//   }

  all_a = document.getElementsByTagName("a")
  all_button = document.getElementsByTagName("button")
  all_a.addEventListener("click", this.showLoader, false);
  all_button.addEventListener("click", this.showLoader, false);
