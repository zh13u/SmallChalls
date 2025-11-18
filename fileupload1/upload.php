<?php
session_start();

/*
 upload.php (CTF) - yêu cầu: nếu file không có extension => từ chối upload (yêu cầu upload lại)
 - Giữ session để chỉ hiển thị file cho session hiện tại
 - Chặn đúng extension 'php'
 - Sanitize tên
*/

$uploadDir = __DIR__ . DIRECTORY_SEPARATOR . 'uploads';
if (!is_dir($uploadDir)) {
    mkdir($uploadDir, 0775, true);
}

// Kiểm tra upload basic
if (!isset($_FILES['file']) || $_FILES['file']['error'] !== UPLOAD_ERR_OK) {
    header('Location: index.php');
    exit;
}

$originalName = $_FILES['file']['name'];
$tmpPath = $_FILES['file']['tmp_name'];

// sanitize tên (loại bỏ control chars, slashes, etc.)
$originalName = preg_replace('/[\\x00-\\x1F\\\\\\/\\:\\*\\?"<>\\|]+/', '_', $originalName);
$originalName = trim($originalName);

// Lấy phần extension (nếu có)
$ext = pathinfo($originalName, PATHINFO_EXTENSION);
$extLower = strtolower($ext);

// Nếu không có extension => yêu cầu upload lại
if ($ext === '' || $ext === null) {
    header('Content-Type: text/html; charset=UTF-8');
    echo '<!doctype html><html><head><meta charset="utf-8"><title>Upload lỗi</title></head><body style="font-family: system-ui, -apple-system,Segoe UI, Roboto, Arial;"><div style="max-width:800px;margin:40px auto;">';
    echo '<h2 style="color:#b91c1c">Upload thất bại</h2>';
    echo '<p>File bạn gửi <strong>không có phần mở rộng (extension)</strong>. Vui lòng đổi tên file và thử lại (ví dụ <code>exploit.phtml</code> hoặc <code>payload.php.jpg</code>).</p>';
    echo '<p><a href="index.php">Quay lại trang upload</a></p>';
    echo '</div></body></html>';
    exit;
}

// Chặn chính xác .php (lowercase)
if ($extLower === 'php') {
    header('Content-Type: text/html; charset=UTF-8');
    echo '<!doctype html><html><head><meta charset="utf-8"><title>Upload lỗi</title></head><body style="font-family: system-ui, -apple-system,Segoe UI, Roboto, Arial;">';
    echo '<div style="max-width:800px;margin:40px auto;">';
    echo '<h2 style="color:#b91c1c">Upload thất bại</h2>';
    echo '<p>Đuôi <code>.php</code> bị chặn. Vui lòng đổi tên file (ví dụ dùng <code>.phtml</code> hoặc double-extension như <code>shell.php.jpg</code>).</p>';
    echo '<p><a href="index.php">Quay lại trang upload</a></p>';
    echo '</div></body></html>';
    exit;
}

// Tạo tên file lưu trên server: giữ phần basename (có extension), thêm prefix ngẫu nhiên
$uniquePrefix = bin2hex(random_bytes(4)); // 8 hex chars
$targetBase = basename($originalName);
$targetName = $uniquePrefix . '_' . $targetBase;
$targetPath = $uploadDir . DIRECTORY_SEPARATOR . $targetName;

// Move file
if (!move_uploaded_file($tmpPath, $targetPath)) {
    header('Content-Type: text/html; charset=UTF-8');
    echo '<!doctype html><html><head><meta charset="utf-8"><title>Upload lỗi</title></head><body style="font-family: system-ui, -apple-system,Segoe UI, Roboto, Arial;">';
    echo '<div style="max-width:800px;margin:40px auto;">';
    echo '<h2 style="color:#b91c1c">Upload thất bại</h2>';
    echo '<p>Không thể lưu file lên server.</p>';
    echo '<p><a href="index.php">Quay lại trang upload</a></p>';
    echo '</div></body></html>';
    exit;
}

// Ghi record vào session để chỉ hiển thị cho session hiện tại
if (!isset($_SESSION['uploads']) || !is_array($_SESSION['uploads'])) {
    $_SESSION['uploads'] = [];
}
$_SESSION['uploads'][] = ['name' => $targetName, 'ts' => time()];

// set permissive perms
@chmod($targetPath, 0664);
@chown($targetPath, 'www-data');

// Redirect về index
header('Location: index.php');
exit;
