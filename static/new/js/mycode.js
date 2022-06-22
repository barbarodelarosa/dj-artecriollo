

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


