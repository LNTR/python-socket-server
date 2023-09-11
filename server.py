from subprocess import Popen, PIPE
import socket
import os
import json

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
PORT_NUMBER=2728
RESOURCE_DIRECTORY="htdocs"
PHP_SUPPORTED_EXTENSTION_LIST=["php","html"]
SERVER_URL=f"http://localhost:{PORT_NUMBER}"

SUPPORTED_RESPONSE_CONTENT_TYPES={
    "js":"text/javascript",
    "css":"text/css",
    "html":"text/html",
    "php":"text/html",
    "txt":"text/plain",
}



def main():
    server_socket.bind(('', PORT_NUMBER))
    server_socket.listen()
    while True:
        connection, client_address = server_socket.accept()
        handle_client(connection,client_address)


def handle_client(connection,client_address):
    try:
        data = connection.recv(4096).decode("utf-8")
        print(data)
        if len(data):
            
            request_header_details_dict = get_request_header_details_dict( data ) # Get header details from recived data. 

            status_details_dict = get_status_details_dict( request_header_details_dict["resource_path"] ) # Geting the status details for response header
            
            resource,content_type=fetch_resource_and_type(**request_header_details_dict,**status_details_dict) # if the resource is available, get the byte version of it. Else it will return the 404.html
            
            response=create_new_response(request_header_details_dict["protocol"],status_details_dict,resource,content_type) #creating a new response: Basically this combines the response headers with resource data

            connection.send(response)
            connection.close()

    except Exception as error:
        print(f"{error}")
    
    print("Client disconnected...")


def get_request_header_details_dict(data):
    request_line = data.split('\r\n')[0]
    method, resource_path, protocol = request_line.split()
    parameters={}

    #Depending on the request method, the following lines will get the query string which holds our request parameters
    if method=="GET":
        resource_path+="?"
        query_string=resource_path.split("?")[1]
        resource_path=resource_path.split("?")[0] 
    else:
        query_string=data.splitlines()[-1] 

    parameters=parse_parameters_from_query_string(query_string) # This will return the query_string (I.E : "a=1&b=2") as a dictonary (I.E : {"a":1,"b":2})
    resource_path=resource_path.replace("//","/") # turn /test// into /test/
    
    resource_path=decide_resource_file_path(resource_path) # if there isn't a specific resource path, the resource path will be set to "resource_path/index.(html or php)"
    # Note that in this server.py, we gave a higher precidency to index.php than index.html

    resource_path=resource_path.replace("//","/") # to turn "D://" to "D:/" etc. because it messes the resource path while executing in php

    return {
        "method":method,
        "resource_path":resource_path[1:],# To avoid getting a "/" at the start of the resource path
        "protocol":protocol,
        "parameters":parameters
    }

def parse_parameters_from_query_string(path):
     # This will return the query_string (I.E : "a=1&b=2") as a dictonary (I.E : {"a":1,"b":2})
    parameters={}
    if path.count("="):

        for single_query in path.split("&"):
            variable,value=single_query.split("=")
            parameters[variable]=value

    return parameters

def decide_resource_file_path(resource_path):
    """
        Will make sure that the resource_path is in a default format
    """
    if not resource_path.count("."):
        if os.path.exists(f"{RESOURCE_DIRECTORY}/{resource_path}/index.php"):
            return resource_path+"/index.php"
        return resource_path+"/index.html"
    return resource_path
    


def get_status_details_dict(resource_path):

    status_details_dict={"status_code":0,"message":"NULL"}

    if os.path.exists(f"./{RESOURCE_DIRECTORY}/{resource_path}"):
        status_details_dict["status_code"]=200
        status_details_dict["message"]="OK"
    else:
        status_details_dict["status_code"]=404
        status_details_dict["message"]="Not Found"
    
    return status_details_dict

def fetch_resource_and_type(**kwargs):
    method=kwargs["method"]
    path=kwargs["resource_path"]
    parameters=kwargs["parameters"]

    content_type_type=get_content_type(path) #getting the valid content type

    if kwargs["status_code"]==404:
        with open(f"./{RESOURCE_DIRECTORY}/404.html","rb") as resource:
            return (resource.read(),content_type_type)


    if path.split(".")[-1] in PHP_SUPPORTED_EXTENSTION_LIST:
        #if the resource is a php or html file, we will treat it differently compared to other resources
        output=fetch_php_output(method,path,parameters)
        return (output,content_type_type)
    else:

        # if the resource isn't a php or html, it only needs to return the byte encoded data
        with open(f"./{RESOURCE_DIRECTORY}/{path}","rb") as resource:
            return (resource.read(),content_type_type)

def get_content_type(path):
    content_type="*/*"
    extention=path.split(".")[-1].lower()
    for key in SUPPORTED_RESPONSE_CONTENT_TYPES.keys():
        if key==extention.lower():
            content_type=SUPPORTED_RESPONSE_CONTENT_TYPES[key]

    return content_type


def fetch_php_output(method,resource_path,parameters):
    
    payload=json.dumps({
        "method":method,
        "resource_path":resource_path,
        "parameters":parameters
    })
    #The above payload contains the meta data from the client as a json string object. This will be passed into the wrapper.php which in
    # turns execute the resource path

    #passing the meta data to the wrapper.php as a command line argument 
    process = Popen(["./php/php",f"./{RESOURCE_DIRECTORY}/wrapper.php",payload], stdout=PIPE,cwd="./")

    (output, error) = process.communicate() #getting and returning the data from the subprocess. This is already encoded in byte format

    process.wait()

    print(output.decode("utf-8"))
    
    return output

def create_new_response(protocol,status_details_dict,resource,content_type):
    print(status_details_dict)
    response = f"{protocol} {status_details_dict['status_code']} {status_details_dict['message']}".encode("utf-8")+b'\r\n'
    response += f"Content-Type: {content_type}".encode("utf-8")+b'\r\n'
    response += b"\r\n"
    
    if status_details_dict["status_code"]==200:
        response+=resource
    else:
        response+=resource

    return response


if __name__=="__main__":
    print(f"Server running on {SERVER_URL}")
    main()


