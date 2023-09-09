<?php 
    
    $payload=$argv[1];
    $json_object=json_decode($payload);
    
    $method=$json_object->method;
    $path=$json_object->path;
    $parameters=(array)$json_object->parameters;


    if ($method=="GET") {
        $_GET=$parameters;
    } else if ($method=="POST"){
        $_POST=$parameters;
    };

    include $path;
?>