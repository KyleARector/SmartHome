<?php echo "<!DOCTYPE html>" ?>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Test Page</title>
    <link rel="stylesheet" href="css/kyleStyle.css">
    <!-- <script src="script.js"></script> -->
  </head>
  <body>
	<div class="wrapper">
	    <form style="padding:5px; float:left;" action="php/Test.php" method="post">
    		<input class="button1 " type="submit" name="Button1" value="On">
	    </form>
	    <form style="padding:5px; float:right;" action="php/Test2.php" method="post">
    		<input class="button1 " type="submit" name="Button1" value="Off">
	    </form>
	</div>
  </body>
</html>