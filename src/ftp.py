
# ______ ______________  ___  ___  ______ 
# |  ___|_   _| ___ \  \/  | / _ \ | ___ |
# | |_    | | | |_/ / .  . |/ /_\ \| |_/ /
# |  _|   | | |  __/| |\/| ||  _  ||  __/ 
# | |     | | | |   | |  | || | | || |    
# \_|     \_/ \_|   \_|  |_/\_| |_/\_|


# FTPMap is a FTP Bruteforce console program written in Python
# It is designed to be fast and easy to use

# GitHub: https://github.com/ZhengLinLei/ftpmap
# Documentation: https://ZhengLinLei.github.io/ftpmap

# Type 'help' or '?' for help


# @author: ZhengLinLei
version = '1.0.0b'





import sys, re, os, requests
from colorama import Fore, init

try:
    import gnureadline as readline
except ImportError:
    import readline

# Add lib ./libs/conn.py
import libs.conn as conn

# print(repr(conn))
# Global variables

info = '''
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
'''


COMMANDS = [['?', 'help', 'exit', 'probe', 'brute', 'key', 'version', 'host']]
COMMANDS_FNC = {
    'help': lambda x, ftp: print(info),
    '?': lambda x, ftp: print(info),
    'version': lambda x, ftp: print(version),
    'exit': lambda x, ftp: sys.exit(0),
}
PATH = os.path.dirname(__file__)


# Main function to be executed when the program starts
def main():

    # Print the banner
    print(Fore.GREEN + "\n\n\n______ ______________  ___  ___  ______ \n|  ___|_   _| ___ \  \/  | / _ \ | ___ |\n| |_    | | | |_/ / .  . |/ /_\ \| |_/ /\n|  _|   | | |  __/| |\/| ||  _  ||  __/ \n| |     | | | |   | |  | || | | || |    \n\_|     \_/ \_|   \_|  |_/\_| |_/\_|\n" + Fore.RESET)
    print("---------------------------------------")
    print("GitHub: https://github.com/ZhengLinLei/ftpmap")
    print("Documentation: https://ZhengLinLei.github.io/ftpmap\n")
    print("Type 'help' or '?' for help")
    print("---------------------------------------")

    # Start the console

    # ----> 1. Ask for IP or Domain
    ip, username = None, None

    
    while (not ip):
        ip = input(Fore.YELLOW + "ftpmap @ip> " + Fore.RESET)

        # Check if the input is a valid IP or Domain
        ip = is_valid_ip(ip)
        if not ip:
            print(Fore.RED + "Invalid IP or Domain" + Fore.RESET)

    # ----> 2. Ask for username
    while (not username):
        username = input(Fore.YELLOW + "ftpmap @username> " + Fore.RESET)


    # Create a FTPConn object
    FTP = conn.FTPConn(ip, username)

    # ----> 3. Start console
    while True:
        print(Fore.YELLOW + "ftpmap> " + Fore.RESET, end="")
        cmd = input()

        # Empty command
        if not cmd:
            continue

        # Split the command
        cmd = [x for x in cmd.strip().split(" ") if x]

        # Check if the command is valid
        if cmd[0] not in COMMANDS[0]:
            print(Fore.RED + "Invalid command: " + cmd[0] + Fore.RESET)
            continue
        
        # Execute the command
        COMMANDS_FNC[cmd[0]](cmd, FTP)



# ----------------------------------------------

# ========================
# @params: cmd, ftp
# @return: None
# 
# @description: Probe to connect to the FTP server
# ========================
def probe(cmd, ftp) -> None:
    # Check if the command is valid
    if len(cmd) > 1:
        # Arguments -psw, --password and -u, --username
        password, username = None, None

        # Check if the arguments are valid
        for arg in cmd[1:]:
            # Check if the argument is -psw, --password
            if arg.startswith("-psw=") or arg.startswith("--password="):
                password = arg.split("=")[1]
            
            # Check if the argument is -u, --username
            elif arg.startswith("-u=") or arg.startswith("--username="):
                username = arg.split("=")[1]
            
            # Invalid argument
            else:
                print(Fore.RED + "Invalid argument: " + arg + Fore.RESET)
                return
            
        # Check if password is empty
        if not password:
            print(Fore.RED + "Password required for: " + cmd[0] + Fore.RESET)
            return
        
        if not username:
            username = ftp.USERNAME

        # Probe connection
        if ftp.connect(password, username, show=True):
            print(Fore.GREEN + "----------------------------")
            print("Connected to FTP server!")
        else:
            print(Fore.RED + "----------------------------")
            print("Failed connecting to FTP")

        # For Both
        print("HOST:            " + ftp.HOST)
        print("USERNAME:        " + username)
        print("PASSWORD:        " + password)
        print("--------------------------" + Fore.RESET)

    else:
        print(Fore.RED + "Empty argument for: " + cmd[0] + Fore.RESET)

COMMANDS_FNC['probe'] = probe


# ----------------------------------------------


# ========================
# @params: cmd, ftp
# @return: None
# 
# @description: Brute force the FTP server
# ========================
def brute(cmd, ftp) -> None:
    keyfile, username, show, continue_ = None, None, False, False

    # Check if the command is valid
    if len(cmd) > 1:
        # Check subcommands
        if cmd[1] in ["start", "stop", "all"]:
            # Arguments -kf, --keyfile, -u, --username, -s, --show and -c, --continue
            for arg in cmd[2:]:
                if arg.startswith("-kf=") or arg.startswith("--keyfile="):
                    keyfile = arg.split("=")[1].strip()
                    if os.path.exists(keyfile):
                        # Read the file
                        with open(keyfile, "r") as f:
                            keys = f.read().split("\n")
                            f.close()

                    else:
                        print(Fore.RED + "Key file not found: " + keyfile + Fore.RESET)
                        return

                elif arg.startswith("-u=") or arg.startswith("--username="):
                    username = arg.split("=")[1].strip()
                elif arg.startswith("-s") or arg.startswith("--show"):
                    show = True
                elif arg.startswith("-c") or arg.startswith("--continue"):
                    continue_ = True
                else:
                    print(Fore.RED + "Invalid argument: " + arg + Fore.RESET)
                    return

            if not username:
                username = ftp.USERNAME

            # Check if the subcommand is start
            if cmd[1] == "start":
                # Keyfile not specified
                with open(PATH+'/keyfile', "r") as f:
                    keys_d = f.read().split("\n")
                    f.close()

                # Check if the keyfile is valid
                keysarr = []
                if keyfile:
                    keysarr.append(keys)
                if continue_ or not keyfile:
                    keysarr.append(keys_d)

                
                for i, keys in enumerate(keysarr):
                    # Brute force the FTP server
                    response = ftp.bruteforce(keys, username, show)

                    # Check if the brute force is successful
                    if response:
                        print(Fore.GREEN + "----------------------------")
                        print("Connected to FTP server!")
                        print("HOST:            " + ftp.HOST)
                        print("USERNAME:        " + response[0])
                        print("PASSWORD:        " + response[1])
                        print("--------------------------" + Fore.RESET)

                        return
                    
                    else:
                        if not continue_ or i == len(keysarr)-1:
                            print(Fore.RED + "Finished with no results" + Fore.RESET)
                            return

            elif cmd[1] == "all":
                 # Keyfile not specified
                with open(PATH+'/dictionary', "r") as f:
                    keys_d = [x.split(':') for x in f.read().split("\n")]
                    f.close()

                # Check if the keyfile is valid
                keysarr = []
                if keyfile:
                    keys = [x.split(':') for x in keys]
                    keysarr.append(keys)
                if continue_ or not keyfile:
                    keysarr.append(keys_d)

                
                for i, keys in enumerate(keysarr):
                    # Brute force the FTP server
                    response = ftp.bruteforceAll(keys, show)

                    # Check if the brute force is successful
                    if response:
                        print(Fore.GREEN + "----------------------------")
                        print("Connected to FTP server!")
                        print("HOST:            " + ftp.HOST)
                        print("USERNAME:        " + response[0])
                        print("PASSWORD:        " + response[1])
                        print("--------------------------" + Fore.RESET)

                        return
                    
                    else:
                        if not continue_ or i == len(keysarr)-1:
                            print(Fore.RED + "Finished with no results" + Fore.RESET)
                            return

            
        else:
            print(Fore.RED + "Invalid subcommand: " + cmd[1] + Fore.RESET)
    else:
        print(Fore.RED + "Empty argument for: " + cmd[0] + Fore.RESET)

COMMANDS_FNC['brute'] = brute

# ----------------------------------------------


# ========================
# @params: cmd, ftp
# @return: None
# 
# @description: Set new keys file
# ========================
def key(cmd, ftp) -> None:
    list = False

    # Check if the command is valid
    if len(cmd) > 1:
        # Check arguments -a, --add, -r, --remove and -l, --list
        for arg in cmd[1:]:
            if arg.startswith("-a=") or arg.startswith("--add="):
                # Add the key or file content to the key file
                key = arg.split("=")[1]

                # Check if the key is a filename
                if os.path.exists(key):
                    # Read the file
                    with open(key, "r") as f:
                        keys = f.read()
                        f.close()
                else:
                    keys = key

                # Append the key to the key file
                with open(PATH+"/keyfile", "a") as f:
                    f.write("\n"+keys)
                    f.close()

                print(Fore.GREEN + "Key added to keyfile" + Fore.RESET)
            
            elif arg.startswith("-r=") or arg.startswith("--remove="):
                #Add the key or file content to the key file
                key = arg.split("=")[1]


                # Check if the key is a filename
                if os.path.exists(key):
                    # Read the file
                    with open(key, "r") as f:
                        keys = f.read().split("\n")
                        f.close()
                else:
                    keys = [key]

                # Append the key to the key file    
                with open(PATH+"/keyfile", "r") as f:
                    # Get text
                    text = f.read()
                    f.close()

                with open(PATH+"/keyfile", "w") as f:
                    # Write
                    for key in keys:
                        # Remove the key
                        text = re.sub(r'^'+key+'$', '', text, flags=re.MULTILINE)

                    f.write(text)
                    # The text saved may have empty lines,
                    # this empty lines will be removed when the user run brute command

                    f.close()

                print(Fore.GREEN + "Key removed from keyfile" + Fore.RESET)

            elif arg.startswith("-l") or arg.startswith("--list"):
                list = True

            # Invalid argument
            else:
                print(Fore.RED + "Invalid argument: " + arg + Fore.RESET)
                return
            
        # list == True
        if list:
            # Open file with default text editor
            os.system(PATH+"/keyfile")
            
    else:
        print(Fore.RED + "Empty argument for: " + cmd[0] + Fore.RESET)

COMMANDS_FNC['key'] = key


# ----------------------------------------------


# ========================
# @params: cmd, ftp
# @return: None
# 
# @description: Change host IP or domain
# ========================
def host(cmd, ftp) -> None:
    show = True
    # Check if the command is valid
    if len(cmd) > 1:
        # Check if the argument is -s, --show or -i, --ip is valid
        for arg in cmd[1:]:
            # Check if the argument is -s, --show
            if arg.startswith("-s") or arg.startswith("--show"):
                show = True if cmd[1].split("=")[1] == "true" else False

            # Check if the argument is -i, --ip
            elif arg.startswith("-i=") or arg.startswith("--ip="):
                ip = arg.split("=")[1]

                # Check if the IP or Domain is valid
                ip = is_valid_ip(ip)
                if not ip:
                    print(Fore.RED + "Invalid IP or Domain" + Fore.RESET)
                    return
                else:
                    ftp.setAttr(HOST=ip)

            # Check if the argument is -u, --username
            elif arg.startswith("-u=") or arg.startswith("--username="):
                username = arg.split("=")[1].strip()

                # Check if the username is valid
                if not username:
                    print(Fore.RED + "Invalid username" + Fore.RESET)
                    return
                else:
                    ftp.setAttr(USERNAME=username)

            # Invalid argument
            else:
                print(Fore.RED + "Invalid argument: " + arg + Fore.RESET)
                return

    print(Fore.GREEN + "HOST:            " + ftp.HOST + "\nUSERNAME:        " + ftp.USERNAME + Fore.RESET) if show else None

COMMANDS_FNC['host'] = host
    

# Check if var is a valid IP or Domain
def is_valid_ip(ip):
    # Remove blank
    ip = ip.strip()
    # Check if the var is a valid IP or Domain with regex
    valid = (re.search(r"^((^\s*((([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))\s*$)|(^\s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?\s*$))$", ip) 
            or
            re.search(r"^((?!-))(xn--)?[a-z0-9][a-z0-9-_]{0,61}[a-z0-9]{0,1}\.(xn--)?([a-z0-9\-]{1,61}|[a-z0-9-]{1,30}\.[a-z]{2,})$", ip))
    
    return valid.string if valid else valid


# Check main file
if __name__  == "__main__":

    # Init the console for colors (Windows)
    # Check Windows OS or other
    if os.name == 'nt':
        init()


    # Download the key file from https://github.com/ZhengLinLei/ftpmap.git
    # Fetch request
    # Save the key file to ./keyfile
    URL = "https://raw.githubusercontent.com/ZhengLinLei/ftpmap/main/docs"
    # Download the key file from the server if it does not exist ./keyfile

    for path in ['/keyfile', '/dictionary']:
        if not os.path.exists(PATH+path):
            data = requests.get(url = URL+path).text

            # Save the key file to ./keyfile
            with open(PATH+path, "w") as f:
                f.write(data)
                f.close()

        
    # Execute main function
    main()