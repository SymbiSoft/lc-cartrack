<?php
// This file is part of LcCarTrack project by Luca Cassioli
//
// This file receives data from an URL and stores them into a KML file
// for vieweing in GooglEarth compatible programs.
//
// URL example:
// http://jumpjack.altervista.org/lccartrack/upload.php?pos=12.0,42.01&name=Auto&speed=12&time=2008-10-22_10:10:10



// Single position kml file
$filename = 'lccartrack.kml';
$handle = fopen($filename, 'w');

// Logger file
$history = 'lccartrack.txt';
$handle2 = fopen($history, 'a+');

// Get the data from the POST request
$time = date('Y-m-d H:i:s');
$name = $_GET['name'];   
$pos = $_GET['pos'];   
$speed = $_GET['speed']; 
$GPSTime = $_GET['time'];
		 
// Setup kml portions
$kmlHeader='<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://earth.google.com/kml/2.0"><Folder><description>MGMaps Favorites</description><name>MGMaps Favorites</name><visibility>1</visibility><open>1</open><Placemark>';
$kmlNameHeader='<name>';
$kmlName=$name;
$kmlNameFooter='</name>';
$kmlDescriptionHeader='<description>';
$kmlDescription='Phone:' . $time . "\nGPS:" . $GPSTime;
$kmlDescriptionFooter='</description>';
$kmlPositionHeader='<Point><coordinates>';
$kmlPosition=$pos.substr(5,$pos.length-1);
$kmlPositionFooter=',0</coordinates></Point>';
$kmlFooter='</Placemark></Folder></kml>';

// Send data back to the phone
echo 'Dati ricevuti:<br>';
echo $name . '<br>';
echo $pos . '<br>';
echo $speed . '<br>';
echo $GPSTime . '<br>';
$output = $name . ',' . $pos . ',' . $speed . ',' . $GPSTime .chr(13) . chr(10);
echo '>>>>>>' . $output . '<<<<<<';

// Write data to log file
fwrite($handle2, $output, strlen($output));



// Write data to KML file
fwrite($handle, $kmlHeader, strlen($kmlHeader));
fwrite($handle, $kmlNameHeader, strlen($kmlNameHeader));
fwrite($handle, $kmlName, strlen($kmlName));
fwrite($handle, " - ", 3);
fwrite($handle, $speed, strlen($speed));
fwrite($handle, " Km/h", 5);
fwrite($handle, $kmlNameFooter, strlen($kmlNameFooter));
fwrite($handle, $kmlDescriptionHeader, strlen($kmlDescriptionHeader));
fwrite($handle, $kmlDescription, strlen($kmlDescription));
fwrite($handle, $kmlDescriptionFooter, strlen($kmlDescriptionFooter));
fwrite($handle, $kmlPositionHeader, strlen($kmlPositionHeader));
fwrite($handle, $kmlPosition, strlen($kmlPosition));
fwrite($handle, $kmlPositionFooter, strlen($kmlPositionFooter));
fwrite($handle, $kmlFooter, strlen($kmlFooter));

fwrite($handle, "\n");
fclose($handle);  
    ?>
