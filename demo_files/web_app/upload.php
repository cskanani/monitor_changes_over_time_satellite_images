<?php
    if (isset($_FILES['pre_image']) 
    and isset($_FILES['post_image']) 
    and (!$_FILES['pre_image']['error']) 
    and (!$_FILES['post_image']['error'])) {
        try {
            $target_dir = "uploads/";
            $fname = uniqid();
            $pre_target_file = $target_dir . $fname . "_pre.jpg";
            $post_target_file = $target_dir . $fname . "_post.jpg";
            move_uploaded_file($_FILES['pre_image']['tmp_name'], $pre_target_file);
            move_uploaded_file($_FILES['post_image']['tmp_name'], $post_target_file);
            echo $fname;
        } catch (Exception $e) {
            echo "Error: Unable to upload files, Please try again!";
        }
    } else {
        echo "Error: Unable to upload files, Please try again!";
    }
?>