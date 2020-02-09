// upload files and start processing data
$('#file_uploads').submit(function(e){
  e.preventDefault();
  $.ajax({
      url:'upload.php',
      type:'post',
      data:new FormData($('#file_uploads')[0]),
      processData: false,
      contentType: false,
      success:function(response){
        response_prefix = response.slice(0, 7)
        if (response_prefix == 'Error:') {
          alert(response);
        } else {
          start_task(response);
        }
      }
  });
});

// get live messages from python file
function start_task(data) {
  source = new EventSource('co.php?fname=' + data);
  var r = document.getElementById('progress_data');
  r.innerHTML = '';
  $('#live_progress').addClass('current');
  $('#data_upload').removeClass('current');
  $('*[data-tab="data_upload"]').addClass('disabled');
  $('*[data-tab="data_upload"]').removeClass('current');
  $('*[data-tab="live_progress"]').removeClass('disabled');
  $('*[data-tab="live_progress"]').addClass('current');

  //a message is received
  source.addEventListener('message', function(e) {
    var result = JSON.parse(e.data);
    if (result.message.substring(0, 4) == 'JSON') {
      var json_content = result.message.substring(5);
      jQuery.get(json_content, function(json_data) {
        $('#output_json').html('<pre>' + JSON.stringify(json_data, null, 4) + '</pre>');
      });
      
      $('*[data-tab="output_json"]').removeClass('disabled');
      $('*[data-tab="data_upload"]').removeClass('disabled');
      source.close();
    } else if(result.message.substring(0, 5) == 'Image') {
      var image_content = result.message.substring(6);
      $('#output_image').html('<img src="' + image_content + '" alt="Mask Image" />');
      $('#output_image').addClass('current');
      $('*[data-tab="output_image"]').removeClass('disabled');
      $('*[data-tab="output_image"]').addClass('current');
    } else {
      add_log(result.message);
    }
  });

  source.addEventListener('error', function(e) {
    add_log('Error occured! Please report to admin.');
    $('*[data-tab="data_upload"]').removeClass('disabled');
    $('*[data-tab="live_progress"]').addClass('disabled');
    source.close();
  });
}

function stop_task() {
  add_log('Interrupted');
  $('*[data-tab="data_upload"]').removeClass('disabled');
  $('*[data-tab="live_progress"]').addClass('disabled');
  source.close();
}

function add_log(message) {
  var r = document.getElementById('progress_data');
  r.innerHTML += message + '<br>';
  r.scrollTop = r.scrollHeight;
}
