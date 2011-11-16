<?php

print "<h1>Pygmynote</h1>";
print "<a href='https://github.com/dmpop/pygmynote'>https://github.com/dmpop/pygmynote</a>";
print "<br>";

$db = new PDO('sqlite:pygmynote.db');

print "<h2>Tasks</h2>";
print "<hr>";
print "<table border=0>";
print "<tr><td><strong>ID</strong></td><td><strong>Note</strong></td><td><strong>Tags</strong></td><td><strong>Deadline</strong></td></tr>";
$result = $db->query("SELECT due, id, note, tags FROM notes WHERE due <> '' AND tags NOT LIKE '%private%' AND type = 'A' ORDER BY due ASC");
foreach($result as $row)
{
print "<tr><td><strong><font color='green'>".$row['id']."</strong></font> -- </td>";
print "<td>".$row['note']."</td>";
print "<td><em>".$row['tags']."</em></td>";
print "<td><font color='orange'>".$row['due']."</font></td></tr>";
}
print "</table>";

$db = NULL;

print "<hr>";

#echo sqlite_libversion();
#echo "<br>";
#echo phpversion();

?>