<?php

    use \Psr\Http\Message\ServerRequestInterface as Request;
    use \Psr\Http\Message\ResponseInterface as Response;

    $app = new \Slim\App;



    /***__________________________________________  Allelica API's  __________________________________________***/


    ###________________________________ User API's ________________________________###

    // Add User
    $app->post('/api/user/add', function(Request $request, Response $response){
        $context = array();
        $email     = str_replace(' ', '', $request->getParam('email'));
        $password  = str_replace(' ', '', $request->getParam('password'));
        $name      = str_replace(' ', '', $request->getParam('name'));
        $last_name = str_replace(' ', '', $request->getParam('last_name'));
        $address   = trim($request->getParam('address'));
        $city      = str_replace(' ', '', $request->getParam('city'));
        $zip_code  = str_replace(' ', '', $request->getParam('zip_code'));
        $note      = str_replace(' ', '', $request->getParam('note'));
        $mobile    = trim($request->getParam('mobile'));

        if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
            $context["status"] = "error";
            $context["message"] = "The email address is not valid";
            $context["values"] = '';

            return $response->withStatus(501, 'Not Implemented')
                ->withHeader('Content-Type', 'application/json')
                ->write(json_encode($context));

        } elseif (strlen($password) < 5) {
            $context["status"] = "error";
            $context["message"] = "This password length is not long enough";
            $context["values"] = '';

            return $response->withStatus(501, 'Not Implemented')
                ->withHeader('Content-Type', 'application/json')
                ->write(json_encode($context));
        }

        // If user already exists or not
        $sql = "SELECT `email` FROM `user` WHERE `user`.`email` = :email";
        try {
            $db = new db();
            $db1 = $db->connect();

            $stmt = $db1->prepare($sql);
            $stmt->execute(array('email' => $email));

            if ($stmt->rowCount() > 0) {
                $context["status"] = "error";
                $context["message"] = "The user with email address: '$email' already exists";
                $context["values"] = '';

                $db1 = $db->connect(false);

                return $response->withStatus(501, 'Not Implemented')
                    ->withHeader('Content-Type', 'application/json')
                    ->write(json_encode($context));
            }

            // If salt already exists or not
            $pSalt = "";
            while(true) {
                try {
                    $salt = mt_rand(100, 1000000000000000);    #Generate salt and save
                    $sql = "SELECT `salt` FROM `user` WHERE `user`.`salt` = :salt";

                    $stmt = $db1->prepare($sql);
                    $stmt->execute(array('salt' => $salt));

                    if ($stmt->rowCount() == 0) {
                        $pSalt = $salt;
                        break;
                    }
                } catch (PDOException $e) {
                    $context["status"] = "error";
                    $context["message"] = $e->getMessage();
                    $context["values"] = "";

                    $db1 = $db->connect(false);

                    return $response->withStatus(501, 'Not Implemented')
                        ->withHeader('Content-Type', 'application/json')
                        ->write(json_encode($context));
                }
            }

            // Add user to the database
            $sql = "INSERT INTO `user` (`email`, `password`, `salt`, `name`, `last_name`, `address`, `city`, `zip_code`, `note`, `mobile`)
                    VALUES (:email, :password, :salt, :name, :last_name, :address, :city, :zip_code, :note, :mobile) ";
            try {
                $hashPassword = sha1($password.$pSalt);

                $stmt = $db1->prepare($sql);
                if(!$stmt->execute(array('email' => $email, 'password' => $hashPassword, 'salt' => $pSalt, 'name' => $name, 'name' => $name,
                    'last_name' => $last_name, 'address' => $address, 'city' => $city, 'zip_code' => $zip_code, 'note' => $note, 'mobile' => $mobile))) {
                    $context["status"] = "error";
                    $context["message"] = "Insert is not performed on user table";
                    $context["values"] = '';

                    $db1 = $db->connect(false);

                    return $response->withStatus(501, 'Not Implemented')
                        ->withHeader('Content-Type', 'application/json')
                        ->write(json_encode($context));
                }

                $context["status"] = "success";
                $context["message"] = "User with email address: '$email' was added";
                $context["values"] = '';

                $db1 = $db->connect(false);

                return $response->withStatus(200, 'OK')
                    ->withHeader('Content-Type', 'application/json')
                    ->write(json_encode($context));

            } catch (PDOException $e) {
                $context["status"] = "error";
                $context["message"] = $e->getMessage();
                $context["values"] = "";

                $db1 = $db->connect(false);

                return $response->withStatus(501, 'Not Implemented')
                    ->withHeader('Content-Type', 'application/json')
                    ->write(json_encode($context));
            }

        } catch (PDOException $e) {
            $context["status"] = "error";
            $context["message"] = $e->getMessage();
            $context["values"] = "";

            $db1 = $db->connect(false);

            return $response->withStatus(501, 'Not Implemented')
                ->withHeader('Content-Type', 'application/json')
                ->write(json_encode($context));
        }
    });



    // User Authentication (then barcode registration)
    $app->post('/api/user/login', function(Request $request, Response $response) {
        $context   = array();
        $email     = str_replace(' ', '', $request->getParam('email'));
        $password  = str_replace(' ', '', $request->getParam('password'));

        if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
            $context["status"] = "error";
            $context["message"] = "The email address is not valid";
            $context["values"] = "";

            return $response->withStatus(501, 'Not Implemented')
                            ->withHeader('Content-Type', 'application/json')
                            ->write(json_encode($context));

        } elseif (strlen($password) < 5) {
            $context["status"] = "error";
            $context["message"] = "The password is not long enough";
            $context["values"] = "";

            return $response->withStatus(501, 'Not Implemented')
                ->withHeader('Content-Type', 'application/json')
                ->write(json_encode($context));
        }

        $sql = "SELECT `salt` FROM `user` WHERE `user`.`email` = :email ";
        try {
            $db = new db();
            $db1 = $db->connect();

            $stmt = $db1->prepare($sql);
            $stmt->execute(array('email' => $email));
            $product = $stmt->fetchAll(PDO::FETCH_ASSOC);

            if(isset($product[0])) {
                $salt = $product[0]["salt"];
            } else {
                $salt = '';
            }

            if ($salt == '') {
                $context["status"] = "error";
                $context["message"] = "Empty salt for current user";
                $context["values"] = "";

                $db1 = $db->connect(false);

                return $response->withStatus(501, 'Not Implemented')
                    ->withHeader('Content-Type', 'application/json')
                    ->write(json_encode($context));

            }

            $hashPassword = sha1($password.$salt);
            $sqlCheckHashPassword = "SELECT `id` FROM `user` WHERE `user`.`password` = :hashPassword AND `user`.`email` = :email ";
            try {
                $stmt = $db1->prepare($sqlCheckHashPassword);
                $stmt->execute(array('hashPassword' => $hashPassword, 'email' => $email));
                $result = $stmt->fetchAll(PDO::FETCH_ASSOC);

                if ($stmt->rowCount() == 0) {
                    $context["status"] = "error";
                    $context["message"] = "Password does not match";
                    $context["values"] = "";

                    $db1 = $db->connect(false);

                    return $response->withStatus(501, 'Not Implemented')
                        ->withHeader('Content-Type', 'application/json')
                        ->write(json_encode($context));
                }

                $context["status"] = "success";
                $context["message"] = "OK";
                $context["values"]["userId"] = (int)$result[0]["id"];

                $db1 = $db->connect(false);

                return $response->withStatus(200, 'OK')
                    ->withHeader('Content-Type', 'application/json')
                    ->write(json_encode($context));

            } catch(PDOException $e) {
                $context["status"] = "error";
                $context["message"] = $e->getMessage();
                $context["values"] = "";

                $db1 = $db->connect(false);

                return $response->withStatus(501, 'Not Implemented')
                    ->withHeader('Content-Type', 'application/json')
                    ->write(json_encode($context));
            }

        } catch (PDOException $e) {
            $context["status"] = "error";
            $context["message"] = $e->getMessage();
            $context["values"] = "";

            $db1 = $db->connect(false);

            return $response->withStatus(501, 'Not Implemented')
                ->withHeader('Content-Type', 'application/json')
                ->write(json_encode($context));
        }

    });



    //Barcode registration
    $app->post('/api/user/barcode', function(Request $request, Response $response){
        $context = array();
        $barcode = str_replace(' ', '', $request->getParam('barcode'));
        $barcode = str_replace('Allelica', '', $barcode);
        $barcode = str_replace('ALLELICA', '', $barcode);
        $barcode = strtoupper($barcode);
        $userId  = str_replace(' ', '', $request->getParam('userId'));

        // Does barcode exist? and is it ready?
        $sql = "SELECT `status` FROM `barcode` WHERE `barcode`.`code` = :barcode ";
        try {
            $db = new db();
            $db1 = $db->connect();

            $stmt = $db1->prepare($sql);
            $stmt->execute(array('barcode' => $barcode));
            $result = $stmt->fetchAll(PDO::FETCH_ASSOC);

            if ($stmt->rowCount() == 0) {
                $context["status"] = "error";
                $context["message"] = "This barcode does not exist";
                $context["values"] = "";

                $db1 = $db->connect(false);

                return $response->withStatus(501, 'Not Implemented')
                    ->withHeader('Content-Type', 'application/json')
                    ->write(json_encode($context));
            }

            if($result[0]["status"] == 'registred') {
                $context["status"] = "error";
                $context["message"] = "The barcode: '$barcode', already registered";
                $context["values"] = "";

                $db1 = $db->connect(false);

                return $response->withStatus(501, 'Not Implemented')
                    ->withHeader('Content-Type', 'application/json')
                    ->write(json_encode($context));
            }


            // Add to join user barcode and user id
            $sql = "INSERT INTO `join_user_barcode` (`user`, `barcode`, `date`) VALUES (:user, :barcode, :date) ";
            try {
                $stmt = $db1->prepare($sql);
                if(!$stmt->execute(array('user' => $userId, 'barcode' => $barcode, 'date' => date("Y-m-d H:i:s")))) {
                    $context["status"] = "error";
                    $context["message"] = "Insert is not performed on join_user_barcode table";
                    $context["values"] = "";

                    $db1 = $db->connect(false);

                    return $response->withStatus(501, 'Not Implemented')
                        ->withHeader('Content-Type', 'application/json')
                        ->write(json_encode($context));
                }

                // Update barcode table setting the status to the register
                $sql = "UPDATE `barcode` SET  `status` = 'registred' WHERE `barcode`.`code` = :code ";
                try {
                    $stmt = $db1->prepare($sql);
                    if(!$stmt->execute(array('code' => $barcode))) {
                        $context["status"] = "error";
                        $context["message"] = "Insert is not performed on barcode table";
                        $context["values"] = "";

                        $db1 = $db->connect(false);

                        return $response->withStatus(501, 'Not Implemented')
                            ->withHeader('Content-Type', 'application/json')
                            ->write(json_encode($context));
                    }

                    $context["status"] = "success";
                    $context["message"] = "Information added to the join user barcode table and also barcode table is updated";
                    $context["values"] = "";

                    $db1 = $db->connect(false);

                    return $response->withStatus(200, 'OK')
                        ->withHeader('Content-Type', 'application/json')
                        ->write(json_encode($context));

                } catch (PDOException $e) {
                    $context["status"] = "error";
                    $context["message"] = $e->getMessage();
                    $context["values"] = "";

                    $db1 = $db->connect(false);

                    return $response->withStatus(501, 'Not Implemented')
                        ->withHeader('Content-Type', 'application/json')
                        ->write(json_encode($context));
                }

            } catch (PDOException $e) {
                $context["status"] = "error";
                $context["message"] = $e->getMessage();
                $context["values"] = "";

                $db1 = $db->connect(false);

                return $response->withStatus(501, 'Not Implemented')
                    ->withHeader('Content-Type', 'application/json')
                    ->write(json_encode($context));
            }

        } catch (PDOException $e) {
            $context["status"] = "error";
            $context["message"] = $e->getMessage();
            $context["values"] = "";

            $db1 = $db->connect(false);

            return $response->withStatus(501, 'Not Implemented')
                ->withHeader('Content-Type', 'application/json')
                ->write(json_encode($context));
        }

    });





    /***__________________________________________  Allelica Landing Pages API's  __________________________________________***/

    // Contacts
    $app->post('/api/contact', function(Request $request, Response $response){
        $context = array();
        $email    = str_replace(' ', '', $request->getParam('email'));
        $name     = str_replace(' ', '', $request->getParam('name'));
        $message  = trim($request->getParam('message'));

        if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
            $context["status"] = "error";
            $context["message"] = "The email address: '.$email.' invalid";
            $context["values"] = "";

            return $response->withStatus(501, 'Not Implemented')
                ->withHeader('Content-Type', 'application/json')
                ->write(json_encode($context));

        } elseif(strlen($name) < 3) {
            $context["status"] = "error";
            $context["message"] = "The name: '.$name.' is too short";
            $context["values"] = "";

            return $response->withStatus(501, 'Not Implemented')
                ->withHeader('Content-Type', 'application/json')
                ->write(json_encode($context));

        } elseif(strlen($message) < 5) {
            $context["status"] = "error";
            $context["message"] = "The message is too short";
            $context["values"] = "";

            return $response->withStatus(501, 'Not Implemented')
                ->withHeader('Content-Type', 'application/json')
                ->write(json_encode($context));
        }
    });




    /***__________________________________________  Tests API's  __________________________________________***/


    //Get All Prodcuts
    $app->get('/api/prodcut', function(Request $request, Response $response){
        $sql = "SELECT * FROM `prodcut`";

        try {
            //Get Db Object
            $db = new db();
            //Connect
            $db = $db->connect();

            $stmt = $db->query($sql);
            $products = $stmt->fetchAll(PDO::FETCH_OBJ);
            $db = null;

            echo json_encode($products);

        } catch (PDOException $e) {
            echo '{"error": {"text": '.$e->getMessage().'}';
        }
    });


    //Get Single Prodcut
    $app->get('/api/prodcut/{id}', function(Request $request, Response $response){
        $id = $request->getAttribute('id');
        $sql = "SELECT * FROM `prodcut` WHERE `prodcut`.`id` = '".$id."' ";

        try {
            //Get Db Object
            $db = new db();
            //Connect
            $db = $db->connect();

            $stmt = $db->query($sql);
            $product = $stmt->fetchAll(PDO::FETCH_OBJ);
            $db = null;

            echo json_encode($product);

        } catch (PDOException $e) {
            echo '{"error": {"text": '.$e->getMessage().'}';
        }
    });


    //Post Add Prodcut
    $app->post('/api/prodcut/add', function(Request $request, Response $response){
        $label = $request->getParam('label');
        $sql = "INSERT INTO `prodcut` (`label`) VALUES (:label) ";

        try {
            //Get Db Object
            $db = new db();
            //Connect
            $db = $db->connect();

            $stmt = $db->prepare($sql);
            $stmt->bindParam(':label', $label);
            $stmt->execute();

            echo '{"notice": {"text": "Prodcut Added"}';

        } catch (PDOException $e) {
            echo '{"error": {"text": '.$e->getMessage().'}';
        }
    });


    //Post Update Prodcut
    $app->put('/api/prodcut/update/{id}', function(Request $request, Response $response){
        $id = $request->getAttribute('id');
        $label = $request->getParam('label');

        $sql = "UPDATE `prodcut` SET  `label` = :label WHERE `prodcut`.`id` = '".$id."' ";

        try {
            //Get Db Object
            $db = new db();
            //Connect
            $db = $db->connect();

            $stmt = $db->prepare($sql);
            $stmt->bindParam(':label', $label);
            $stmt->execute();

            echo '{"notice": {"text": "Prodcut Updated"}';

        } catch (PDOException $e) {
            echo '{"error": {"text": '.$e->getMessage().'}';
        }
    });


    // Delete Single Prodcut
    $app->delete('/api/prodcut/delete/{id}', function(Request $request, Response $response){
        $id = $request->getAttribute('id');
        $sql = "DELETE FROM `prodcut` WHERE `prodcut`.`id` = '".$id."' ";

        try {
            //Get Db Object
            $db = new db();
            //Connect
            $db = $db->connect();

            $stmt = $db->prepare($sql);
            $stmt->execute();
            $db = null;

            echo '{"notice": {"text": "Prodcut With Id:'.$id.' is Deleted"}';

        } catch (PDOException $e) {
            echo '{"error": {"text": '.$e->getMessage().'}';
        }
    });









