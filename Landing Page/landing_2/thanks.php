<?php
/*error_reporting(E_ALL);
ini_set('display_errors', 1);*/

// Set your secret key: remember to change this to your live secret key in production
// See your keys here: https://dashboard.stripe.com/account/apikeys
require_once('stripe/init.php');

\Stripe\Stripe::setApiKey("sk_live_tZPZBydcXX7pyPpJFH5ynijv");

// Token is created using Checkout or Elements!
// Get the payment token ID submitted by the form:
$token = json_decode($_POST['token']);
// Charge the user's card:
$charge = \Stripe\Charge::create(array(
  "amount" => 16900,
  "currency" => "eur",
  "description" => "Example charge",
  "source" => $token->id,
));
?>
<!DOCTYPE html>
<html class="no-js">
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <title>Acquista | Nutrizione | Allelica</title>
        <meta name="description" content="">
        <meta name="viewport" content="width=device-width, initial-scale=1">
<script>
(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
})(window,document,'script','https://www.google-analytics.com/analytics.js','ga');

ga('create', 'UA-101154194-1', 'auto');
ga('send', 'pageview');
</script>
        <!-- Place favicon.ico and apple-touch-icon.png in the root directory -->
        <link rel="icon" href="favicon.ico" type="image/x-icon">
        <!-- Fonts -->
        <!-- Source Sans Pro -->
        <link href="https://fonts.googleapis.com/css?family=Droid+Serif:400i|Source+Sans+Pro:300,400,600,700" rel="stylesheet">

        <link href="https://fonts.googleapis.com/css?family=Josefin+Sans:300,400,600,700" rel="stylesheet">
        
        <!-- CSS -->

        <!-- <link rel="stylesheet" href="css/bootstrap.min.css"> -->
        <!-- Bootstrap CDN -->
        <!--<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.5/css/bootstrap.min.css" integrity="sha384-AysaV+vQoT3kOAXZkl02PThvDr8HYKPZhNT5h/CXfBThSRXQ6jW5DO2ekP5ViFdi" crossorigin="anonymous">-->
        <link rel="stylesheet" href="css/web-bootstrap.css">
        

        <link rel="stylesheet" href="css/themefisher-fonts.css">
        <link rel="stylesheet" href="css/owl.carousel.css">
        <link rel="stylesheet" href="css/magnific-popup.css">
        <link rel="stylesheet" href="css/style.css?4">
        <!-- Responsive Stylesheet -->
        <link rel="stylesheet" href="css/responsive.css?3">
        <link rel="stylesheet" href="fonts/flaticon.css">

        <!-------------- Changes Begin-------------->
        <style type="text/css">
            .hero-area h1 {
                font-size: 40px;
            }
            .hero-area img {
                padding: 40px 0 30px;
            }
            .hero-area {
                padding-bottom: 50px;
            }
            .block li {
                margin-bottom: 5px;
            }
            .clear {
                clear: both;
            }
            @media only screen and (max-width: 1150px) {
                .hero-area h1 {
                    font-size: 30px !important;
                }
            }
            @media only screen and (max-width: 1150px) {
                .heading h2 {
                    font-size: 23px !important;
                }
            }
            @media only screen and (max-width: 800px) {
                .hero-area .btn-main {
                    display: block;
                }
            }
            @media only screen and (max-width: 1000px) {
                .chi-siamo .row .col-sm-12 {
                    margin-bottom: 40px;
                    margin-left: 50px;
                }
            }
            @media only screen and (max-width: 700px) {
                .chi-siamo .row .col-sm-12 {
                    margin-left: 5px;
                }
            }
            .chi-siamo .row .author-details img {
                margin-bottom: 10px;
            }
            .promo-details .row ul li {
                margin-bottom: 45px;
            }
            .promo-details .row ul li img {s
                margin-right: 15px;
            }
            @media only screen and (max-width: 1000px) {
                .row .testimonial-block .author-details img {
                    width: 100% !important;
                }
            }
        </style>
        <!-------------- Changes End-------------->
        <script src="https://use.fontawesome.com/bb99c802c4.js"></script>
    </head>

    <body id="body">

    	<div id="preloader-wrapper">
    		<div class="pre-loader"><i class="flaticon-null"></i></div>
    	</div>

	    <!-- 
	    Header start
	    ==================== -->
        <div class="container">
            <nav class="navbar navigation " id="top-nav">
                <a class="navbar-brand logo" href="#">
                    <img src="http://www.allelica.com/img/logo.png" width="200">
                </a>

              <button class="navbar-toggler hidden-lg-up float-lg-right" type="button" data-toggle="collapse" data-target="#navbarResponsive" >
                  <i class="tf-ion-android-menu"></i>
              </button>
              <div class="collapse navbar-toggleable-md" id="navbarResponsive">
                <ul class="nav navbar-nav menu float-lg-right" id="top-nav">
                  <li class="">
                    <a href="index.html">HOME</a>
                  </li>
                  <li class="active">
                    <a href="buy.html">ACQUISTA</a>
                  </li>
                  <li class="">
                    <a href="contact.html">CONTATTACI</a>
                  </li>
                </ul>
              </div>
            </nav>
        </div>
        <div class="clear"></div>

	    <section class="hero-area">
	        <div class="container">
	            <div class="row">
                    <div class="col-md-6 text-center">
                        <img src="http://antiaging.allelica.com/img/pack.jpg" width="400"><br><br>
                        
                              
                       
<!--form id="paypal-button" action="https://www.paypal.com/cgi-bin/webscr" method="post" target="_top">
<input type="hidden" name="cmd" value="_s-xclick">
<input type="hidden" name="hosted_button_id" value="2RS9YXCVCALV4">
<input type="image" src="https://www.paypalobjects.com/it_IT/IT/i/btn/btn_buynowCC_LG.gif" border="0" name="submit" alt="PayPal è il metodo rapido e sicuro per pagare e farsi pagare online.">
<img alt="" border="0" src="https://www.paypalobjects.com/it_IT/i/scr/pixel.gif" width="1" height="1">
</form-->
                    </div>
	                <div class="col-md-6">
	                    <div class="block">
	                        <h1 class="subheading" style="text-transofrm:none;">Grazie per aver effettuato l'acquisto</h1>
	                        
	                    </div>
	                </div>
	            </div><!-- .row close -->
	        </div><!-- .container close -->
	    </section><!-- header close -->


        <footer>
            <div class="container text-center">
                <div class="row">
                    <div class="col-md-12">
                        <div class="block">
                            <a href="" class="footer-logo">Allelica</a>
                            <ul class="menu">
                                <li class="">
                                    <a href="/index.html">HOME</a>
                                </li>
                                <li class="active">
                                    <a href="#">ACQUISTA</a>
                                </li>
                                <li class="">
                                    <a href="/contact.html">CONTATTACI</a>
                                </li>
                            </ul>
                            <p class="copyright-text">Copyright &copy; Allelica | All right reserved.</p>
                            <p class="copyright-text">Templates is Copyright &copy; of<a href="http://www.Themefisher.com">Themefisher</a>| All right reserved.
                            <p class="copyright-text">
                            Icon made by freepick from <a href="http://www.flaticon.com" target="_blank">www.flaticon.com</a> </p>
                        </div>
                    </div>
                </div>
            </div>
        </footer>


        <!-- Js -->
        <script src="js/vendor/jquery-2.1.1.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/tether/1.3.7/js/tether.min.js" integrity="sha384-XTs3FgkjiBgo8qjEjBk0tGmf3wPrWtA6coPfQDfFEY8AnYJwjalXCiosYRBIBZX8" crossorigin="anonymous"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.5/js/bootstrap.min.js" integrity="sha384-BLiI7JTZm+JWlgKa0M0kGRpJbF2J8q+qreVrKBC47e3K6BW78kGLrCkeRX6I9RoK" crossorigin="anonymous"></script>
        <script src="js/vendor/modernizr-2.6.2.min.js"></script>
        <script src="js/owl.carousel.min.js"></script>
        <script src="js/jquery.magnific-popup.min.js"></script>
        <script src="js/main.js"></script>
        
    </body>
</html>
