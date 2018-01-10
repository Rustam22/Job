<?php

    class db {

        //Properties
        private $dbhost = 'localhost';
        private $dbuser = 'root';
        private $dbpass = '';
        private $dbname = 'slim_db';
        private $dbConnection;

        //Connect
        public function connect($close = true) {
            $mysql_connect_str = 'mysql:host='.$this->dbhost.';dbname='.$this->dbname.'';
            $this->dbConnection = new PDO($mysql_connect_str, $this->dbuser, $this->dbpass);
            $this->dbConnection->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

            if(!$close) {
                $this->dbConnection = null;
                return $this->dbConnection;
            }

            return $this->dbConnection;
        }


        // Functions utilities
        public function isEmptyResult($stmt) {
            if ($stmt->rowCount() > 0) {
                return true;
            } else {
                return false;
            }
        }

        public function dbClose() {
            $this->dbConnection->close();
        }
    }