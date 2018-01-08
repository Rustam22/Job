<?php

    use \Psr\Http\Message\ServerRequestInterface as Request;
    use \Psr\Http\Message\ResponseInterface as Response;

    $app = new \Slim\App;



    /***__________________________________________  Allelica API's  __________________________________________***/


    ###________________________________ User API's ________________________________###

    // Add User
    $app->post('/api/user/add', function(Request $request, Response $response){
        $email     = str_replace(' ', '', $request->getParam('email'));
        $password  = str_replace(' ', '', $request->getParam('password'));
        $last_name = str_replace(' ', '', $request->getParam('last_name'));
        $address   = str_replace(' ', '', $request->getParam('address'));
        $city      = str_replace(' ', '', $request->getParam('city'));
        $zip_code  = str_replace(' ', '', $request->getParam('zip_code'));
        $note      = str_replace(' ', '', $request->getParam('note'));

        if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
            echo "This ($email) email address is considered invalid.";
        } elseif (strlen($password) < 5) {
            echo "This password is not long enough.";
        }

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


    // User Authentication (then barcode registration)
    $app->post('/api/user/login', function(Request $request, Response $response){
        $email     = str_replace(' ', '', $request->getParam('email'));
        $password  = str_replace(' ', '', $request->getParam('password'));

        if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
            echo "This ($email) email address is considered invalid.";
            return false;
        } elseif (strlen($password) < 5) {
            echo "This password is not long enough.";
            return false;
        }

        $sql = "SELECT `salt` FROM `user` WHERE `user`.`email` = :email ";

        try {
            //Get Db Object
            $db = new db();
            //Connect
            $db = $db->connect();

            $stmt = $db->prepare($sql);
            $stmt->execute(array('email' => $email));

            if ($stmt->rowCount() == 0) {
                echo '{"error": {"text": Empty salt for current user "error_code": emptySalt}';
                return false;
            }

            $product = $stmt->fetchAll(PDO::FETCH_ASSOC);
            $salt = $product[0]["salt"];
            $hashPassword = sha1($password.$salt);

            $sqlCheckHashPassword = "SELECT `id` FROM `user` WHERE `user`.`password` = :hashPassword AND `user`.`email` = :email ";
            try {
                $stmt = $db->prepare($sqlCheckHashPassword);
                $stmt->execute(array('hashPassword' => $hashPassword, 'email' => $email));
                $result = $stmt->fetchAll(PDO::FETCH_ASSOC);

                if ($stmt->rowCount() == 0) {
                    echo '{"error": {"text": Password does not match "error_code": passwordDoesNotMatch}';
                    return false;
                }

                echo '{"success": {"userId": '.$result[0]["id"].' }';
                //var_dump($product, $hashPassword, $result);
            } catch(PDOException $e) {
                echo '{"error": {"text": '.$e->getMessage().' "error_code": 500}';
            }

        } catch (PDOException $e) {
            echo '{"error": {"text": '.$e->getMessage().' "error_code": 500}';
        }

    });


    //Barcode registration
    $app->post('/api/user/barcode', function(Request $request, Response $response){
        $barcode = str_replace(' ', '', $request->getParam('barcode'));
        $barcode = str_replace('Allelica', '', $barcode);
        $barcode = str_replace('ALLELICA', '', $barcode);
        $barcode = strtoupper($barcode);
        $userId  = str_replace(' ', '', $request->getParam('userId'));

        // Does barcode exist? and is it ready?
        $sql = "SELECT `status` FROM `barcode` WHERE `barcode`.`code` = :barcode ";
        try {
            //Get Db Object
            $db = new db();
            //Connect
            $db = $db->connect();

            $stmt = $db->prepare($sql);
            $stmt->execute(array('barcode' => $barcode));
            $result = $stmt->fetchAll(PDO::FETCH_ASSOC);

            if ($stmt->rowCount() == 0) {
                echo '{"error": {"text": This barcode does not exist "error_code": barcodeDoesNotExist}';
                $db = null;
                return false;
            }

            if($result[0]["status"] == 'registred') {
                echo '{"error": {"text": The barcode: '.$barcode.', already registered "error_code": barcodeRegistered}';
                $db = null;
                return false;
            }


            // Add to join user barcode and user id
            $sql = "INSERT INTO `join_user_barcode` (`user`, `barcode`, `date`) VALUES (:user, :barcode, :date) ";
            try {
                $stmt = $db->prepare($sql);
                if(!$stmt->execute(array('user' => $userId, 'barcode' => $barcode, 'date' => date("Y-m-d H:i:s")))) {
                    echo '{"error": {"text": Insert is not performed on join_user_barcode "error_code": insertErrorOnJoinUserBarcodeTable}';
                    $db = null;
                    return false;
                }

                // Update barcode table setting the status to the register
                $sql = "UPDATE `barcode` SET  `status` = 'registred' WHERE `barcode`.`code` = :code ";
                try {
                    $stmt = $db->prepare($sql);
                    if(!$stmt->execute(array('code' => $barcode))) {
                        echo '{"error": {"text": Insert is not performed on barcode table "error_code": insertErrorOnBarcodeTable}';
                        $db = null;
                        return false;
                    }

                    echo '{"success":  Information added to the join user barcode table and also barcode table is updated}';

                } catch (PDOException $e) {
                    echo '{"error": {"text": '.$e->getMessage().' "error_code": 500}';
                    $db = null;
                }

            } catch (PDOException $e) {
                echo '{"error": {"text": '.$e->getMessage().' "error_code": 500}';
                $db = null;
            }

        } catch (PDOException $e) {
            echo '{"error": {"text": '.$e->getMessage().' "error_code": 500}';
            $db = null;
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









