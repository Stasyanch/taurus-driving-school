<?php
ini_set('display_errors', 0);
ini_set('log_errors', 1);
ini_set('error_log', __DIR__ . '/../logs/server-errors.log');


if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $name = trim($_POST['name'] ?? '');
    $phone = trim($_POST['phone'] ?? '');
    $email = trim($_POST['email'] ?? '');

    if (empty($name) || empty($phone) || empty($email)) {
        die("Помилка: Всі поля обов'язкові для заповнення!");
    }
    
    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        die("Помилка: Некоректний формат Email!");
    }


    echo "Заявка від $name успішно прийнята!";
}
?>