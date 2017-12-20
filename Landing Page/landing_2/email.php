<?php
$email = $_POST['email'];
$text= $_POST['text'];
$name = $_POST['name'];

$toArray = ['yakkoroma@gmail.com','giordano@allelica.com'];
$subject = 'CONTATTO RICHIESTO';
$message = "L'utente:". $name ."\nCon la mail:".$email."\nCi chiede:\n".$text;
$headers = 'From: admin@allelica.com' . "\r\n" .
    'Reply-To: admin@allelica.com' . "\r\n" .
    'X-Mailer: PHP/' . phpversion();

foreach($toArray as $to) {
    mail($to, $subject, $message, $headers);
}
echo "Ti ringraziamo per averci contattato\nTi risponderemo appena possibile.";