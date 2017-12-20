<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);

// Set your secret key: remember to change this to your live secret key in production
// See your keys here: https://dashboard.stripe.com/account/apikeys
require_once('stripe/init.php');

\Stripe\Stripe::setApiKey("sk_test_lbHo9VTgUGjUOMxKb1FO0NVu");

// Token is created using Checkout or Elements!
// Get the payment token ID submitted by the form:
$token = $_POST['stripeToken'];

// Charge the user's card:
$charge = \Stripe\Charge::create(array(
  "amount" => 16900,
  "currency" => "eur",
  "description" => "Example charge",
  "source" => $token,
));
?>
The payment has been processed