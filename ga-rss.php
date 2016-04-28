<?php
/*
 * Garfield comic by Jim Davis
 * RSS wrapper by fishy ( http://yhsif.com )
 * RSS wrapper source (what you are reading now) released under GPL v3
 */

function shift_days($date, $days) {
	return mktime(0, 0, 0, date("m", $date), date("d", $date) + $days, date("Y", $date));
}

function date2img($date) {
	return 'http://images.ucomics.com/comics/ga/' . date("Y", $date) . '/ga' . date("ymd", $date) . '.gif';
}

function date2url($date) {
	return 'http://www.gocomics.com/garfield/' . date("Y", $date) . '/' . date("m", $date) . '/' . date("d", $date);
}

function find_next_available_date($date, $cachedate) {
	$day = $date;
	$fp = fopen("/dev/null", "w");
	$i = 0;
	while(1) {
		if($day <= $cachedate)
			break;
		$i++;
		if($i > 3) {
			$i--;
			break;
		}
		$ch = curl_init(date2img($day));
		curl_setopt($ch, CURLOPT_FAILONERROR, TRUE);
		curl_setopt($ch, CURLOPT_FILE, $fp);
		curl_exec($ch);
		$code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
		curl_close($ch);
		if($code == 200)
			break;
		$day = shift_days($day, -1);
	}
	fclose($fp);
	print("<!-- fetched $i url(s) -->\n");
	return $day;
}

header("Content-Type: application/xml");
header('Content-Disposition: inline; filename="rss2.xml"');
print("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n");

$cache_file = ".rss-cache";
$count = intval($_REQUEST['n']);
if($count == 0)
	$count = 10;
$lastcheck = 0;
$cacheday = 0;
if(file_exists($cache_file)) {
	$handle = fopen($cache_file, "r");
	list($lastcheck, $cacheday) = fscanf($handle, "%u\t%u\n");
	fclose($handle);
}
$lastday = $cacheday;
if($cacheday == 0 || $lastcheck == 0 || (time() - $lastcheck) > 60*30) {
	$lastday = mktime(0, 0, 0, date("m"), date("d") + 1, date("Y"));
	$lastday = find_next_available_date($lastday, $cacheday);
	$handle = fopen($cache_file, "w");
	fwrite($handle, sprintf("%u\t%u\n", time(), $lastday));
	fclose($handle);
} else
	print("<!-- cache hit -->\n");
?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
<title>Garfield daily comic</title>
<link>http://www.garfield.com/comics/comics_todays.html</link>
<description>The daily comic of Garfield, from ucomics.com</description>
<docs>http://blogs.law.harvard.edu/tech/rss</docs>
<atom:link href="http://selif.yhsif.com/ga-rss.php" rel="self" type="application/rss+xml" />
<?php
for($i = 0; $i < $count; $i++) {
	$img = date2img($lastday);
	$url = date2url($lastday);
	$title = "Garfield comic " . date("Y-m-d", $lastday);
	$date = date("r", $lastday);
	$desc = "<![CDATA[<img src=\"$img\" />]]>";
	print <<<EOLAST
<item>
<title>$title</title>
<link>$url</link>
<guid>$url</guid>
<pubDate>$date</pubDate>
<description>$desc</description>
</item>

EOLAST;
	$lastday = shift_days($lastday, -1);
}
?>
</channel>
</rss>
