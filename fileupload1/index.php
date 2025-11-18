<?php
session_start();

$uploadDir = __DIR__ . DIRECTORY_SEPARATOR . 'uploads';
if (!is_dir($uploadDir)) mkdir($uploadDir, 0775, true);

// Garbage-collect old files
function gc_old_uploads($uploadDir, $ttl_seconds = 3600) {
    foreach (glob($uploadDir . '/*') as $f) {
        if (is_file($f) && (time() - filemtime($f) > $ttl_seconds)) {
            @unlink($f);
        }
    }
}
gc_old_uploads($uploadDir, 24 * 3600);

$files = [];
if (!empty($_SESSION['uploads']) && is_array($_SESSION['uploads'])) {
    foreach ($_SESSION['uploads'] as $item) {
        $path = $uploadDir . DIRECTORY_SEPARATOR . $item['name'];
        if (is_file($path)) $files[] = $item['name'];
    }
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Upload</title>
    <style>
        body { font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif; margin: 40px; }
        .container { max-width: 820px; margin: 0 auto; }
        .card { border: 1px solid #e5e7eb; border-radius: 10px; padding: 20px; margin-bottom: 20px; }
        h1 { margin-top: 0; }
        .input { padding: 10px; border: 1px solid #d1d5db; border-radius: 8px; }
        .button { padding: 10px 14px; background: #111827; color: white; border: 0; border-radius: 8px; cursor: pointer; }
        .list li { margin: 6px 0; }
        .view { display: inline-block; margin-left: 10px; font-size: 12px; }
        .bad { color: #b91c1c; }
    </style>
</head>
<body>
<div class="container">

    <div class="card">
        <h1>Upload</h1>
        <form action="upload.php" method="post" enctype="multipart/form-data">
            <input class="input" type="file" name="file" required>
            <button class="button" type="submit">Submit</button>
        </form>
    </div>

    <div class="card">
        <h2>Files</h2>
        <ul class="list">
        <?php
        if (empty($files)) {
            echo '<li>No files</li>';
        } else {
            foreach ($files as $f) {
                $encoded = htmlspecialchars($f, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
                echo '<li><strong>' . $encoded . '</strong> '
                   . '<a class="view" href="uploads/' . rawurlencode($f) . '" target="_blank">open</a>'
                   . ' <a class="view" href="?view=' . rawurlencode($f) . '">render</a>'
                   . '</li>';
            }
        }
        ?>
        </ul>
    </div>

    <div class="card">
        <?php
        if (isset($_GET['view'])) {
            $target = $_GET['view'];
            $target = str_replace('..', '', $target);
            $full = $uploadDir . DIRECTORY_SEPARATOR . $target;
            if (is_file($full)) {
                include $full;
            } else {
                echo '<p class="bad">Not found.</p>';
            }
        }
        ?>
    </div>

</div>
</body>
</html>
