<?php
        $mes="010";
        $retval=0;
        $last_line=0;
        $SndMsg = "/var/www/c/SendUART ".$mes;
        $last_line = system($SndMsg, $retval);
        header("Location:/../index.php");
?>
