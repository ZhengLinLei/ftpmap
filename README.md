> #### Bruteforce tool for low security FTP server
> - Use this tool in your own risk.
> - Illegal use is prohibited.
> - The author is not responsible for any damage caused by this tool.

<br>
<br>
<h1 align="center">FTPMAP</h1>
<br>
<br>
<br>
<br>
<p align="center">
    <a href="./CONTRIBUTING.md">Contributing</a>
    ·
    <a href="https://github.com/ZhengLinLei/ftpmap/issues">Issues</a>
</p>
<p align="center">
    <a href="https://opensource.org/licenses/Apache-2.0">
        <img src="https://img.shields.io/badge/License-Apache%202.0-blue.svg" alt="License" />
    </a>&nbsp;
    <a>
        <img src="https://img.shields.io/badge/version-1.0-brightgreen" alt="Version" />
    </a>
</p>
<hr>


```
    ______ ______________  ___  ___  ______ 
    |  ___|_   _| ___ \  \/  | / _ \ | ___ |
    | |_    | | | |_/ / .  . |/ /_\ \| |_/ /
    |  _|   | | |  __/| |\/| ||  _  ||  __/ 
    | |     | | | |   | |  | || | | || |    
    \_|     \_/ \_|   \_|  |_/\_| |_/\_|

    ---------------------------------------
    GitHub: https://github.com/ZhengLinLei/ftpmap
    Documentation: https://ZhengLinLei.github.io/ftpmap

    Type 'help' or '?' for help
    ---------------------------------------

    ftpmap @ip> 0.0.0.0
    ftpmap @username> ftp
    ftpmap> help

        help                                         | Show this help message
        exit                                         | Exit the program
        version                                      | Show the version of the program
        probe                                        | Probe to connect to the FTP server
            -psw, --password   =<password>           + Password to connect to the FTP server
            -u,   --username   =<username>           + Username to connect to the FTP server (default: anonymous)
        brute                                        | Brute force the FTP server
            start                                    * Start brute forcing
            stop                                     * Stop brute forcing
            all                                      * Brute force all the passwords and users in the ./dictionary file
            -kf,  --keyfile    =<keyfile>            + Key file to brute force the FTP server (default: ./keyfile)
            -u,   --username   =<username>           + Username to brute force the FTP server (default: anonymous)
            -s,   --show                             + Show every attempt (default: false)
            -c,   --continue                         + Continue to ./keyfile after the user provided key file is not found or EOF (default: false)
        key                                          | Set the key file
            -a,   --add        =<password>|<file>    + Add a key to the key file
            -r,   --remove     =<password>|<file>    + Remove a key from the key file
            -l,   --list                             + Show all the keys (default: false)
        host                                         | Set the host
            -s,   --show                             + Show the host (default: true)
            -i,   --ip         =<host>               + Set the host
            -u,   --username   =<username>           + Set the username (default: anonymous)
            

        Example: brute start -kf=./keyfile -u=anonymous -s -c
```


## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)


## Installation

### From Source

```bash
git clone https://github.com/ZhengLinLei/ftpmap.git

cd ftpmap
```

For Linux & MacOS users:
```bash
python3 ./src/ftp.py
```

For Windows users:
```bash
py | python ./src/ftp.py
```


### From PyPI (Not available yet)

```bash
pip install ftpmap
```

Run the program with the following command:
```bash
python -m ftpmap
```

### From release

Download the latest release from [here]()

1. Unzip the file
2. Open the executable
3. Enjoy!

For MacOS users:
```bash
unzip ftpmap-macos.zip
```

```bash
./ftpmap
```

For Windows users:
```bash
unzip ftpmap-windows.zip
```

```bash
ftpmap.exe
```


## Usage

### List of commands

| Command | Description |
| ------- | ----------- |
| `help` | Show this help message |
| `exit` | Exit the program |
| `version` | Show the version of the program |
| `probe` | Probe to connect to the FTP server |
| `brute` | Brute force the FTP server |
| `key` | Set the key file |
| `host` | Set the host |

### Probe

To use the program, you need to know the IP address of the FTP server you want to connect to. After running the program, you will be asked to enter the IP address of the FTP server. You can also use the `host` command to set the IP address of the FTP server.

```
ftpmap @ip> 0.0.0.0
ftpmap @username> ftp
```

After setting the IP address, you will be asked to enter the username of the FTP server. You can also use the `probe` command to probe the FTP server.
> Note: The default username is `anonymous`.
>
> Argument: -pws, --password (required)
> Argument: -u, --username (optional, the default username is the username you have set before. Default value: anonymous)
> Example: probe -psw=123456 -u=ftp
>
```
ftpmap> probe -psw=123
----------------------------
Connecting to FTP server...
HOST:            0.0.0.0
USERNAME:        ftp
PASSWORD:        123
--------------------------
----------------------------
Failed connecting to FTP
HOST:            0.0.0.0
USERNAME:        ftp
PASSWORD:        123
--------------------------


ftpmap> probe -psw=ftp -u=otheruser
----------------------------
Connecting to FTP server...
HOST:            0.0.0.0
USERNAME:        otheruser
PASSWORD:        ftp
--------------------------
----------------------------
Failed connecting to FTP
HOST:            0.0.0.0
USERNAME:        otheruser
PASSWORD:        ftp
--------------------------


ftpmap> probe
Empty argument for: probe

ftpmap> probe --password=ftp --username=ftp
----------------------------
Connecting to FTP server...
HOST:            0.0.0.0
USERNAME:        ftp
PASSWORD:        ftp
--------------------------
----------------------------
Connected to FTP server!
HOST:            0.0.0.0
USERNAME:        ftp
PASSWORD:        ftp
--------------------------
```

### Host

You can use the `host` command to set and get the IP address of the FTP server. 
> 
> Argument: -i, --ip (optional)
> Argument: -u, --username (optional)
```
ftpmap> host 
HOST:            0.0.0.0
USERNAME:        ftp


ftpmap> host -i=192.168.0.1
HOST:            192.168.0.1
USERNAME:        ftp


ftpmap> host -u=zll
HOST:            192.168.0.1
USERNAME:        zll


ftpmap> host -i=0.0.0.0 -u=zll
HOST:            0.0.0.0
USERNAME:        zll
```


### Key

You can use the `key` command to set the key file. The default key file is `./keyfile`. You can also use the `key` command to add or remove keys from the key file.
> Note: The key file is a file that contains all the passwords you want to brute force. Each line in the key file is a password.
>
> Argument: -a, --add (required)
> Argument: -r, --remove (required)
> Argument: -l, --list (optional)
> Example: key -a=123456
```
ftpmap> key -a=password
Key added to keyfile


ftpmap> key -r=password
Key removed from keyfile


ftpmap> key -l
sh: File opened
```

### Brute

You can use the `brute` command to brute force the FTP server. You can also use the `brute` command to start or stop brute forcing. The default key file is `./keyfile`. You can also use the `brute all` to brute force all the passwords and users in the `./dictionary` file.
> Note: The key file is a file that contains all the passwords you want to brute force. Each line in the key file is a password.
>
> Argument: -kf, --keyfile (optional, the default key file is the key file you have set before. Default value: ./keyfile)
> Argument: -u, --username (optional, the default username is the username you have set before. Default value: anonymous)
> Argument: -s, --show (optional, show the host. Default value: false)
> Argument: -c, --continue (optional, continue brute forcing. Default value: false)
> Example: brute -kf=./keyfile -u=anonymous -s -c
>
>
> When you set -kf argument, the program will use the key file you have set before. If you set -c argument, the program will continue brute forcing with the default local keyfile ./src/keyfile after triying all the passwords in the key file you have set before.
```
ftpmap> brute start
Finished with no results


ftpmap> brute start -s
----------------------------
Connecting to FTP server...
HOST:            0.0.0.0
USERNAME:        zll
PASSWORD:        root
--------------------------
----------------------------
Connecting to FTP server...
HOST:            0.0.0.0
USERNAME:        zll
PASSWORD:        ftp
--------------------------
----------------------------
Connecting to FTP server...
HOST:            0.0.0.0
USERNAME:        zll
PASSWORD:        admin
--------------------------
Finished with no results


ftpmap> brute start -c -s -kf=./key.txt
----------------------------
Connecting to FTP server...
HOST:            0.0.0.0
USERNAME:        zll
PASSWORD:        aaa
--------------------------
----------------------------
Connecting to FTP server...
HOST:            0.0.0.0
USERNAME:        zll
PASSWORD:        root
--------------------------
----------------------------
Connecting to FTP server...
HOST:            0.0.0.0
USERNAME:        zll
PASSWORD:        ftp
--------------------------
----------------------------
Connecting to FTP server...
HOST:            0.0.0.0
USERNAME:        zll
PASSWORD:        admin
--------------------------
Finished with no results


ftpmap> brute start -u=otheruser -s
----------------------------
Connecting to FTP server...
HOST:            0.0.0.0
USERNAME:        otheruser
PASSWORD:        root
--------------------------
----------------------------
Connecting to FTP server...
HOST:            0.0.0.0
USERNAME:        otheruser
PASSWORD:        ftp
--------------------------
----------------------------
Connecting to FTP server...
HOST:            0.0.0.0
USERNAME:        otheruser
PASSWORD:        admin
--------------------------
Finished with no results


ftpmap> brute all
----------------------------
Connected to FTP server!
HOST:            0.0.0.0
USERNAME:        ftp
PASSWORD:        ftp
--------------------------


ftpmap> brute all -s
----------------------------
Connecting to FTP server...
HOST:            0.0.0.0
USERNAME:        anonymous
PASSWORD:        anonymous
--------------------------
----------------------------
Connecting to FTP server...
HOST:            0.0.0.0
USERNAME:        root
PASSWORD:        rootpasswd
--------------------------
----------------------------
Connecting to FTP server...
HOST:            0.0.0.0
USERNAME:        ftp
PASSWORD:        ftp
--------------------------
----------------------------
Connected to FTP server!
HOST:            0.0.0.0
USERNAME:        ftp
PASSWORD:        ftp
--------------------------
```


## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for details on submitting patches and the contribution workflow.


## License

This project is licensed under the Apache2.0 License - see the [LICENSE](LICENSE) file for details




