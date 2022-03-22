jQuery(document).ready(function ($) {
  var start = $('.start-btn');

  start.on('click', function (e) {
    if(document.getElementById('sdate').value == '' || document.getElementById('edate').value == ''){
      alert("Please Input Date")
    }

    else{
      e.preventDefault();
      e.stopPropagation();
  
      var url = '/invoice';
      var data = {sdate: document.getElementById('sdate').value, edate:document.getElementById('edate').value};
  
      $.ajax({
        url: url,
        data: data,
        type: 'GET',
        beforeSend: function () {
          Swal.fire({
            title: 'Auto close alert!',
            html: 'Please Hold on as Invoice is being generated',
            timer: 400000,
            timerProgressBar: true,
            showConfirmButton: false,
            allowOutsideClick: false,
          });
        },
        success: function (data) {
          console.log(data['success']);
          if (data.code === true || data.code == 'true') {
            Swal.fire(
              data.success,
              'Click OK to proceed to List',
              'success'
            ).then(function () {
              $('.box-area').addClass('deactivated');
              $('.list').removeClass('deactivated');
  
              var list_html = '';
              var p = data.paths;
              console.log(p)
              for (var t = 0; t < p.length; t++) {
                list_html +=
                  `<li class="text-center"><a href="/static/files/invoice-` +
                  (t + 1).toString() +
                  `.pdf">Invoice - ` +
                  (t + 1).toString() +
                  `</a></li>`;
              }
              console.log(list_html);
              $('.invoice').append(list_html);
            });
          } 
          
          else {
            Swal.fire({
              icon: 'error',
              title: 'Oops...',
              text: data.error,
            })
            //   msg = "<span class='alert alert-success'>" + data.error + '</span>';
            //   error.html(msg);
          }
        },
      });
    }
  });
});
