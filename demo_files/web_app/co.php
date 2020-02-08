<?php

//a new content type. make sure apache does not gzip this type, else it would get buffered
header('Content-Type: text/event-stream');
header('Cache-Control: no-cache'); // recommended to prevent caching of event data.
$fname = $_GET['fname'];

send_message('File Uploaded');
function send_message($message)
{
    $d = array('message' => $message);

    echo "data: " . json_encode($d) . PHP_EOL;
    echo PHP_EOL;

    //PUSH THE data out by all FORCE POSSIBLE
    ob_flush();
    flush();
}

function liveExecuteCommand($cmd)
{

    while (@ ob_end_flush()); // end all output buffers if any

    $proc = popen("$cmd 2>&1 ; echo Exit status : $?", 'r');

    $live_output     = "";
    $complete_output = "";
    while (!feof($proc))
    {
        $live_output     = fread($proc, 4096);
        $complete_output = $complete_output . $live_output;
        send_message($live_output);
        @ flush();
    }

    pclose($proc);
    // get exit status
    preg_match('/[0-9]+$/', $complete_output, $matches);

    // return exit status and intended output
    return array (
                    'exit_status'  => intval($matches[0]),
                    'output'       => str_replace("Exit status : " . $matches[0], '', $complete_output)
                 );
}
$result = liveExecuteCommand('python3 core/main.py '. $fname . '');
ob_end_clean();
echo "From Co";
?>