<?php 

    //  Do not delete this file.
    
    $payload=$argv[1]; // Get the first command line argument. This is the json string that we passed from our server.py file

    $json_object=json_decode($payload);// Decode the json string into a json object
    
    //Setting the variables and methods
    $method=$json_object->method;
    $resource_path=$json_object->resource_path;
    $parameters=(array)$json_object->parameters;

    //Setting GET and POST variables
    if ($method=="GET") {
        $_GET=$parameters;
    } else if ($method=="POST"){
        $_POST=$parameters;
    };

    //Include the resource_path to the end of the wrapper. Now the resource_file have access to all the variables that we set in wrapper
    include $resource_path;
?>