# Desc: FTP connection library
# @auther: ZhengLinLei
# @version: 1

# This library is used to connect to a FTP server


# Imports

import ftplib, os
from typing import Any # FTP library


class FTPConn:
    
    HOST = None
    PORT = 21 # Default port, 22 for SFTP
    USERNAME = None

    # Constructor
    def __init__(self, host, username):
        self.HOST = host

        # check if username is valid
        self.USERNAME = username if username else "anonymous"

    def __setattr__(self, __name: str, __value: Any) -> None:
        # Set the attribute
        self.__dict__[__name] = __value

    # ----------------------------------


    # Set attributes with params
    def setAttr(self, **attributes):
        for attr in attributes:
            self.__setattr__(attr, attributes[attr])


    # Connect to the FTP server
    def connect(self, password, username=None, show=False) -> bool:
        # Check
        password, username = password.strip(), username.strip() if username else self.USERNAME
        try:
            if show:
                print("----------------------------")
                print("Connecting to FTP server...")
                print("HOST:            " + self.HOST)
                print("USERNAME:        " + username)
                print("PASSWORD:        " + password)
                print("--------------------------")

            # ftp = ftplib.FTP(self.HOST)
            # ftp.login(username, password)
            # ftp.quit()

            return True if username=='ftp' and password=='ftp' else False
        except:
            return False
        
    
        

    # Bruteforce the FTP server
    def bruteforce(self, array, username=None, show=False) -> any:

        # Check
        username = username.strip() if username else self.USERNAME

        for password in array:
            # Strip the password
            password = password.strip()

            if self.connect(password, username, show):
                return [username, password]
            
        return False
            
    # Bruteforce all
    def bruteforceAll(self, array, show=False) -> any:
        
        for row in array:
            username, password = row[0], row[1]
            if self.connect(password, username, show):
                return [username, password]