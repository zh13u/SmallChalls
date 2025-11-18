<?php
error_reporting(0);

$FLAG = 'flag{nonono}';

$error_msg = '';
$success = false;
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $u = @$_POST['u'];
    $p = @$_POST['p'];

    if ($u !== null && $p !== null) {
        if ($u !== $p && hash('sha256', $u) == hash('sha256', $p)) {
            $success = true;
        } else {
            $error_msg = 'Access denied';
        }
    }
}
?><!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Login</title>
<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    background: #f5f5f5;
    font-family: Arial, sans-serif;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    padding: 20px;
}

.container {
    background: white;
    padding: 40px;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    width: 100%;
    max-width: 400px;
}

h2 {
    margin-bottom: 30px;
    color: #333;
    font-size: 24px;
}

form {
    margin-bottom: 20px;
}

input {
    width: 100%;
    padding: 12px;
    margin-bottom: 15px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 14px;
    outline: none;
}

input:focus {
    border-color: #666;
}

button {
    width: 100%;
    padding: 12px;
    background: #333;
    color: white;
    border: none;
    border-radius: 4px;
    font-size: 16px;
    cursor: pointer;
}

button:hover {
    background: #555;
}

.footer {
    text-align: center;
    font-size: 12px;
    color: #999;
    margin-top: 20px;
}

.success-message {
    background: white;
    padding: 40px;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    max-width: 500px;
    text-align: center;
}

.success-message h2 {
    color: #28a745;
    margin-bottom: 20px;
}

.flag-box {
    background: #f8f9fa;
    padding: 20px;
    border-radius: 4px;
    font-family: monospace;
    font-size: 14px;
    color: #333;
    word-break: break-all;
    border: 1px solid #ddd;
    margin-top: 15px;
}

.error-message {
    background: #fff3cd;
    border: 1px solid #ffc107;
    padding: 12px;
    border-radius: 4px;
    margin-bottom: 20px;
}

.error-message p {
    color: #856404;
    margin: 0;
}
</style>
</head>
<body>
  <?php if ($success): ?>
    <div class="success-message">
      <h2>Access granted</h2>
      <div class="flag-box"><?php echo htmlspecialchars($FLAG); ?></div>
    </div>
  <?php else: ?>
    <div class="container">
      <?php if ($error_msg): ?>
        <div class="error-message">
          <p><?php echo htmlspecialchars($error_msg); ?></p>
        </div>
      <?php endif; ?>
      <h2>Login</h2>
      <form method="POST" autocomplete="off">
        <input name="u" type="text" placeholder="Username" required />
        <input name="p" type="password" placeholder="Password" required />
        <button type="submit">Submit</button>
      </form>
    </div>
  <?php endif; ?>
</body>
</html>
