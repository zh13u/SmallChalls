<?php
error_reporting(0);

$deniedExts = array("php", "php3", "php4", "php5", "pht", "phtml");

if (isset($_FILES["file"])) {
    $file = $_FILES["file"];
    $error = $file["error"];
    $name = basename($file["name"]);
    $tmp_name = $file["tmp_name"];

    if ($error > 0) {
        echo "Error: " . $error . "<br>";
    } else {
        $temp = explode(".", $name);
        $extension = strtolower(end($temp));

        if (in_array($extension, $deniedExts)) {
            die($extension . " extension file is not allowed to upload!");
        } else {
            if (!is_dir("upload")) {
                mkdir("upload");
            }
            move_uploaded_file($tmp_name, "upload/" . $name);
            echo "Stored in: <a href='/upload/{$name}'>/upload/{$name}</a>";
        }
    }
} else {
    echo "File is not selected";
}
?>
