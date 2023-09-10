# Python Socket Server

This project is a web server written in Python that can serve static files and execute PHP files using the subprocess module and socket module.

## Installation

To install this project, Python 3 and PHP are required on the system. The source code can be cloned from this repository or downloaded as a zip file.

```# Clone the repository
git clone https://github.com/LNTR/python-socket-server.git
```

## Usage

To run this project, a terminal needs to be opened and navigated to the project directory. Then, the server.py file can be executed with Python.

```
# Change directory to the project folder
cd python-socket-server

# Run the server.py file
python server.py
```

The server will start running on port 2728 by default. The port number can be changed by editing the PORT_NUMBER variable in the server.py file.

To access the web server, a web browser needs to be opened and typed http://localhost:2728 in the address bar.

## Current functionalities

- Handling GET and POST requests.
- Handling Images,Javascript and css
- Handling php,html resources
- Detecting index.php/index.html files automatically.

## Dependencies

- Python

  - Socket : To connect the client with the server.
  - Json : To communicate data with the php file in a convinient manner.
  - Subprocess : To communicate with the php.exe file to fetch the results of the executed process
  - Os : To check whether the resource given is available or not.

- PHP
  - I also included the php application. So the machine that the server is running would not have to install any additional software.
  - Wrapper.php file : The sole purpose of the wrapper.php file is to accept command line arguments and load it to it's $\_GET
    and $\_POST arrays so the included resource path that the client requested can access those variables.

## How the server was made

The server was made using Python sockets and subprocess modules. The goal was to create a simple web server that can serve static files and execute PHP files.

### The steps and the logic behind the code are as follows:

- A socket object was created using the socket.socket function and bound to a port number using the socket.bind method. The socket was also set to listen for incoming connections using the socket.listen method.
- A while loop was used to accept connections from clients using the socket.accept method.
- The socket.recv method was used to receive data from the client and decoded it as a UTF-8 string. The data was parsed to get the request line, which contains the method, the resource path, and the protocol.
- Depending on the type of request, the parameters will be parsed.
- The os.path.exists function was used to check if the resource path exists in the htdocs folder, which is the root directory of the web server. If it does not exist, the status code was set to 404 and the message to “Not Found”. If it does exist, the status code was set to 200 and the message to “OK”.
- An if-else statement was used to check if the resource path is a PHP or HTML file or any other type of file. If it is a PHP or HTML file, the subprocess module was used to execute it using the php command via wrapper.php and return the output. If it is any other type of file, it was opened as a binary file and returned as a static file.
- While executing the php, the POPEN call will pass the request headers to the wrapper.php file as a Json object.
- String concatenation and byte encoding were used to create a response that contains the protocol, the status code, the message, the content type, and a blank line. The resource data was also appended to the response.
- The socket.send method was used to send the response back to the client and closed.

### A Typical request made by the web browser

```
POST /sum.php HTTP/1.1  # The default format is [Method] [Resource path]?[Arguments if method=="GET"] [Protocol]
Host: localhost:2728
Connection: keep-alive
Content-Length: 7
Cache-Control: max-age=0
sec-ch-ua: "Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
Upgrade-Insecure-Requests: 1
Origin: http://localhost:2728
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: http://localhost:2728/
Accept-Encoding: gzip, deflate, br
Accept-Language: en-US,en;q=0.9
Cookie: _xsrf=2|cfcf66f7|4f771b79d79adc8459caa06edddcb602|1693018452; pma_lang=en

a=5&b=6 # Since this is a POST Request, the argument are stored at the end of the request
```

### A Typical response made by the server.py

```
HTTP/1.1 200 OK
Content-Type: text/html
Data # The data requested by the client
```
