<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html>

	<head>
	<meta http-equiv="content-type" content="text/html; charset=UTF-8" />
	<link href="style.css" rel="stylesheet" type="text/css" media="all" />
	<link href='http://fonts.googleapis.com/css?family=Open+Sans:400,300,300italic,400italic,600,600italic,700,700italic,800,800italic' rel='stylesheet' type='text/css'>
	<title>Pygmysnip</title>
	</head>
	
	<body>

	<div id="content">
	<p class="content"></p>
	<h1>
	Pygmysnips
	</h1>
	<?php
	$db = new PDO('sqlite:pygmynote.sqlite');
	print "<hr>";
	print "<table border=0>";
	$result = $db->prepare("SELECT id, note, tags FROM notes WHERE tags LIKE '%snip%' AND type='1' ORDER BY id ASC");
	$result->execute();
	foreach($result as $row)
	{
		print "<tr><td><p>".$row['note']."</p></td></tr>";
		print "<tr><td><small>Tags:<em> ".$row['tags']."</small></em></td></tr>";
	}
	print "</table>";
	
	$result->closeCursor();
	$db = NULL;
	print "<hr>";
	
	?>
	
	<center><div class="footer">Pygmysnip is based on <a href="https://github.com/dmpop/pygmynote">Pygmynote</a></div></center>
	
	</body>
</html>