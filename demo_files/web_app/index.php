<?php
?>
<html>
<head>
  <title>Measuring impact of natural calamities using satellite images</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link href="https://fonts.googleapis.com/css?family=Open+Sans:300,400,600" rel="stylesheet">
  <link rel="stylesheet" href="css/main.css">
</head>
<body>
  <section id="intro">
    <h1 class="title">Measuring impact of natural calamities using satellite images</h1>
    <p class="intro-text">Using deep learning based segmentation models to predict the impact of natural calamities using satellite images.</p>
  </section>
  <div class="cont">
  <section id="images-n-data" class="clearfix">
    <div class="images">
      <div class="window">
        <div class="window-header">
          <div class="bullet bullet_red"></div>
          <div class="bullet bullet_yellow"></div>
          <div class="bullet bullet_green"></div>
          <div class="title">Input Window</div>
        </div>
        <div class="menu">
          <ul class="tabs">
            <li class="current" data-tab="data_upload">Data Upload</li>
            <li data-tab="live_progress" class="disabled">Live Progress</li>
          <ul>
        </div>
        <div class="window_body">
          <div id="data_upload" class="tab_content current">
            <form id="file_uploads" enctype="multipart/form-data">
              <b>Pre Image:</b> <input id="pre_image" name="pre_image" type="file"/>
              <b>Post Image:</b> <input id="post_image" name="post_image" type="file"/> <br />
              <input type="submit" value="Upload Image" name="submit">
            </form>
          </div>
          <div id="live_progress" class="tab_content">
            <div id="progress_data"></div>
          </div>
      	</div>
	    </div>
    </div>
    
    <div class="data">
      <div class="window">
        <div class="window-header">
          <div class="bullet bullet_red"></div>
          <div class="bullet bullet_yellow"></div>
          <div class="bullet bullet_green"></div>
          <div class="title">Output Window</div>
        </div>
        <div class="menu">
          <ul class="tabs">
            <li class="disabled" data-tab="output_image">Image</li>
            <li data-tab="output_json" class="disabled">JSON</li>
          <ul>
        </div>
        <div class="window_body">
          <div id="output_image" class="tab_content">
            <p>Image Output</p>
          </div>
	        <div id="output_json" class="tab_content">
            <p>JSON Output</p>
          </div>
        </div >
      </div>
    </div>
  </section>
  <!-- <div class="madeby">Made with ♥ by <a href="https://cskanani.github.io"/>Chandresh Kanani</a></div> -->
</div>
  <script src="js/jquery.js"></script>
  <script src="js/main.js"></script>
  <script>

    $(document).ready(function(){

      $('ul.tabs li').click(function(){
        if(!$(event.target).hasClass('disabled')){
          var tab_id = $(this).attr('data-tab');

          $(event.target).closest('.menu').find('ul.tabs li').removeClass('current');
          $(event.target).closest('.window').find('.tab_content').removeClass('current');

          $(this).addClass('current');
          $("#"+tab_id).addClass('current');
        }
      })

    })

  </script>

</body>
</html>