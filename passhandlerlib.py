"""Module for store and read passwords"""
import configparser
import base64
import random
import string
import sys

class PassHandler:
    """Main pass handler"""
    def __init__(self, config_file, log):
        self.__logger = log.get_logger('PassHandler')
        self.config_file = config_file
        self.__logger.debug("Config file name: %s", config_file)
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file)
        self._encoded_passwd = None

    def store_password(self, password):
        """Encode and store password"""
        letters = string.ascii_letters + string.digits
        string_length = 64
        random_string1 = ''.join(random.choice(letters) for i in range(string_length))
        random_string2 = ''.join(random.choice(letters) for i in range(string_length))
        salted_pass = random_string1 + password + random_string2
        encoded_pass = base64.b64encode(salted_pass.encode("utf-8")).decode("utf-8")
        try:
            self.config.set("Connection", "password", encoded_pass)
        except Exception as error:
            self.__logger.error("An error occurred while set password in config: %s", error)
            return False
        try:
            with open(self.config_file, 'w+', encoding="utf-8") as configfile:
                self.config.write(configfile)
            self.__logger.info("Password stored successfully.")
            return True
        except Exception as error:
            self.__logger.error("An error occurred while storing the password to file: %s", error)
            return False

    def read_password(self):
        """Read password from ini file"""
        try:
            self._encoded_passwd = self.config.get('Connection', 'password')
            salted_pass = base64.b64decode(self._encoded_passwd.encode("utf-8")).decode("utf-8")
            password = salted_pass[64:-64]
        except Exception as error:
            self.__logger.error("An error occurred while read the password: %s", error)
            sys.exit()
        return password

    def check_password(self, password):
        """Check if saved password is the same with saved in file"""
        if password == self.read_password():
            self.__logger.info("Password is correct")
        else:
            self.__logger.error("No password found")
