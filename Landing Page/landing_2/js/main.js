$(window).load(function() {
    $("#preloader-wrapper").fadeOut("slow");
});

$(document).ready(function(){


     
    //animated header class
    $(window).scroll(function() {    
    var scroll = $(window).scrollTop();
     //console.log(scroll);
    if (scroll > 200) {
        //console.log('a');
        $(".navigation").addClass("animated");
    } else {
        //console.log('a');
        $(".navigation").removeClass("animated");
    }});



    $(".gallery-slider").owlCarousel(
        {
        pagination : true,
        autoPlay : 5000,
        itemsDesktop  :  [1500,4],
        itemsDesktopSmall :  [979,3]
        }
    );

    // Gallery Popup
    $('.image-popup').magnificPopup({type:'image'});



});

$(document).on('click','.faq li', function ()  {
    if(!$(this).hasClass('opened')) {
        $(this).addClass('opened');
        $(this).children('p').slideDown();
    } else {
        $(this).removeClass('opened');
        $(this).children('p').slideUp();
    }
});

$(document).ready(function () {
    if($('#customButton').length > 0) {
        var handler = StripeCheckout.configure({
          key: 'pk_live_jISuAVgDyITNrh8Gs0YgWv3T',
          image: 'http://antiaging.allelica.com/img/pack.jpg',
          locale: 'auto',
          token: function(token) {
            // You can access the token ID with `token.id`.
            // Get the token ID to your server-side code for use.
          }
        });
        document.getElementById('customButton').addEventListener('click', function(e) {
            e.preventDefault(); 
            ga('send', 'event', 'pagamento');
            if(!document.getElementById('terms').checked) {
              alert("Assicurati di avere letto e accettato i termini e le condizioni di acquisto.\n");
                  $('#terms').focus();
                  $('#terms').addClass('notslected');
                  $('#terms').next('span').css('font-size','34px;');
                  $('#terms').next('span').css('color','red');
                  $('#terms').next('span').css('font-weight','bold');
                  return false;
              } else {
                  // Open Checkout with further options:
                 handler.open({
                     name: 'Allelica',
                     description: 'Test genetico',
                     currency: 'eur',
                     address: true,
                     amount: 16900,
                     token: function (token,args) {
                         $('#token').val(JSON.stringify(token));
                         $('#payment').submit();
                     }
                });
            }
        });
        
        // Close Checkout on page navigation:
        window.addEventListener('popstate', function() {
          handler.close();
        });
    }
})
 $(document).on('submit','#paypal-button', function (e) {
          ga('send', 'event', 'paypal');
          if(!document.getElementById('terms').checked) {
              alert("Assicurati di avere letto e accettato i termini e le condizioni di acquisto.\n");
              // ga('send', 'event', 'nutrizione - termini non selezionati per:'+pacchettoScelto);
              $('#terms').focus();
               $('#terms').addClass('notslected');
              $('#terms').next('span').css('font-size','34px;');
              $('#terms').next('span').css('color','red');
              $('#terms').next('span').css('font-weight','bold');
              return false;
          } else {
             //ga('send', 'event', 'nutrizione - verso paypal per il pacchetto: '+pacchettoScelto);
             return true;
          }
      });

$(document).on('click','.cta', function () {
    var id = $(this).attr('id');
    ga('send','event','call-to-action '+ id);
})

$(document).on('click','#inviaMessaggio', function (e) {
    e.preventDefault();
    var form = document.getElementById('contatti_form');
    if(form.checkValidity()) {
       var formValue = $('#contatti_form').serialize();
        $.ajax({
           url: 'email.php',
           method: 'POST',
           data: formValue,
           success: function (data) {
               alert(data);
               window.location = 'index.html';
           }
       }); 
    }
})


