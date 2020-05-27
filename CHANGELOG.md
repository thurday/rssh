# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2020-05-27
### Added
### Classes
### SSH Server
### OS Support
- **Linux** - Ok
- **Windows** - No
- **Mac** - Not tested
### Functions
- __ init __ 
    - Arguments
        - **ip** - Your IP
        - **port** - Port to Listen
        - **public_key** - Define a public_key to use, see [examples](https://github.com/ReddyyZ/rssh/tree/master/examples)
        - **private_key** - Define a public_key to use, see [examples](https://github.com/ReddyyZ/rssh/tree/master/examples)
        - **key_bits** - Bits length of key (Default: 4096)
        - **max_connections** - Max connections to listen
- start
    - Arguments
        - None
    - Function
        - Listen on the defined ip and port, accept all connections and create a new thread to handle the new client.
- kill
    - Arguments
        - **addr** - Address of client
    - Function
        - Kill the client connection and remove from the dict.

### SSH Client
### OS Support
- **Linux** - Ok
- **Windows** - Ok
- **Mac** - Not tested
### Functions
- __ init __
    - Arguments
        - **user** - User to login in the server machine
        - **passwd** - Password to login in the server machine
        - **ip** - Server IP
        - **port** - Port IP
        - **public_key** - Define a public_key to use, see [examples](https://github.com/ReddyyZ/rssh/tree/master/examples)
        - **private_key** - Define a public_key to use, see [examples](https://github.com/ReddyyZ/rssh/tree/master/examples)
    - Function
        - Set class variables and load/create RSA key.
- connect
    - Arguments
        - None
    - Function
        - Connects to the server, send and receive public RSA key, and login.
- send
    - Arguments
        - **text** - Command to send to the server
    - Function
        - Sends a command to the server
- kill
    - Arguments
        - None
    - Function
        - Kill the connection