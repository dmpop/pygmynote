<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html>

	<head>
	<meta http-equiv="content-type" content="text/html; charset=UTF-8" />
	<link href="style.css" rel="stylesheet" type="text/css" media="all" />
	<link href="http://fonts.googleapis.com/css?family=Droid+Serif:regular,italic,bold,bolditalic&v1" rel="stylesheet" type="text/css">
	<title>Pygmysnip</title>
	</head>
	
	<body>
	<center><div class="sidebar">
	<div class="sidetext">&#10031; One Snip At A Time &#10031;</div>
	</div></center>
	
	<div id="content">
	<p class="content"></p>
	<h2>
	Pygmysnips
	</h2>

<?php

$db = new PDO('sqlite:pygmynote.db');
print "<hr>";
print "<table border=0>";
$result = $db->query("SELECT id, note, tags FROM notes WHERE tags LIKE '%snip%' AND type='A' ORDER BY id ASC");
foreach($result as $row)
{
print "<tr><td><p>".$row['note']."</p></td></tr>";
print "<tr><td><small>Tags:<em> ".$row['tags']."</small></em></td></tr>";
}
print "</table>";

$db = NULL;

print "<hr>";

?>
	<center><div class="footer">Pygmysnip is based on <a href="https://github.com/dmpop/pygmynote">Pygmynote</a>.</div></center>
	
	<script type="text/javascript" src="/slimstat/?js"></script>
	</body>
</html>