"""Module for use SAP Bapi"""
import configparser
import sys
import pyrfc
from passhandlerlib import PassHandler


class SAPSystem:
    """Main class with basic functions"""
    def __init__(self, config_file, log):
        self.__log = log
        self.__logger = self.__log.get_logger('SAPSystem')
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file)
        self.ashost = self.config.get('Connection', 'ashost')
        self.sysnr = self.config.get('Connection', 'sysnr')
        self.client = self.config.get('Connection', 'client')
        self.user = self.config.get('Connection', 'user')
        self._encoded_passwd = self.config.get('Connection', 'password')
        self.conn = None
        self.logondata ={
            "GLTGV": "",
            "GLTGB": "",
            "USTYP": "",
            "TZONE": ""
        }
        self.logondata_x = {
            "GLTGV": "",
            "GLTGB": "",
            "USTYP": "",
            "TZONE": ""
        }

        self.defaults = {
            "STCOD": "",
            "SPLD": "",
            "DATFM": "",
            "DCPFM": "",
            "LANGU": "",
            "START_MENU": "",
            "TIMEFM": ""
        }
        self.defaults_x = {
            "STCOD": "",
            "SPLD": "",
            "DATFM": "",
            "DCPFM": "",
            "LANGU": "",
            "START_MENU": "",
            "TIMEFM": ""
        }
        self.address = {
            "FIRSTNAME": "",
            "LASTNAME": "",
            "DEPARTMENT": "",
            "FUNCTION": "",
            "CITY": "",
            "TEL1_NUMBR": "",
            "TEL1_EXT": "",
            "E_MAIL": ""
        }
        self.address_x = {
            "FIRSTNAME": "",
            "LASTNAME": "",
            "DEPARTMENT": "",
            "FUNCTION": "",
            "CITY": "",
            "TEL1_NUMBR": "",
            "TEL1_EXT": "",
            "E_MAIL": ""
        }
        self.snc = {
            "GUIFLAG": "",
            "PNAME": ""
        }
        self.snc_x = {
            "GUIFLAG": "",
            "PNAME": ""
        }

    def connect(self):
        """Establish the connect to the SAP system"""
        try:
            pass_h = PassHandler(self.config_file, self.__log)
            passwd = pass_h.read_password()
            self.conn = pyrfc.Connection(ashost=self.ashost, sysnr=self.sysnr,
                                        client=self.client, user=self.user, passwd=passwd)
        except Exception as error:
            self.__logger.error("An error occurred while connect: %s", error)
            sys.exit()
        return self.conn

    def ping(self):
        """Perform ping the SAP system"""
        conn = self.connect()
        if conn.alive:
            self.__logger.info("Connection established successfully")
            result = conn.call('STFC_CONNECTION', REQUTEXT='Ping SAP')
            self.__logger.debug("Ping Result: %s", str(result))
        else:
            self.__logger.error("An error occurred while connect alive check")
        conn.close()

    def bapi_user_change(self, parameters_names, parameters_values):
        """Change users using data from csv file"""
        conn = self.connect()
        self.__bapi_user_changes_structx(parameters_names)
        for row in parameters_values:
            for field in self.logondata:
                if field in row.keys():
                    self.logondata[field] = row[field]
            self.__logger.debug("LOGONDATA: %s", str(self.logondata))
            for field in self.defaults:
                if field in row.keys():
                    self.defaults[field] = row[field]
            self.__logger.debug("DEFAULTS: %s", str(self.defaults))
            for field in self.address:
                if field in row.keys():
                    self.address[field] = row[field]
            self.__logger.debug("ADDRESS: %s", str(self.address))
            for field in self.snc:
                if field in row.keys():
                    self.snc[field] = row[field]
            self.__logger.debug("SNC: %s", str(self.snc))
            username = row["USERNAME"]
        # Call the function
            try:
                result = conn.call("BAPI_USER_CHANGE",  USERNAME=username,
                                    LOGONDATA=self.logondata, LOGONDATAX=self.logondata_x,
                                    DEFAULTS=self.defaults, DEFAULTSX=self.defaults_x,
                                    ADDRESS=self.address, ADDRESSX=self.address_x,
                                    SNC=self.snc, SNCX=self.snc_x)
                self.__print_result(username, result)
            except Exception as error:
                self.__print_result(username, error)
                sys.exit()
        # Close the connection
        conn.close()

    def __print_result(self, username, data):
        """Print SAP response in more human readabale way"""
        self.__logger.debug("Result of call BAPI_USER_CHANGE: %s", str(data))
        if isinstance(data, str):
            self.__logger.error(f"RFC Call Error: {username}: {data}")
        elif isinstance(data, dict):
            for item in data["RETURN"]:
                if item["TYPE"] == 'E':
                    message = item["MESSAGE"]
                    self.__logger.error(f"RFC Call Error: {username}: {message}")
                else:
                    message = item["MESSAGE"]
                    self.__logger.info(f"OK!: {username}: {message}")
        elif data:
            self.__logger.error("Unknown data: %s", str(data))
            sys.exit()

    def __bapi_user_changes_structx(self, parameters_names):
        """Initialise *X structures"""
        for key in self.logondata_x:
            if key in parameters_names:
                self.logondata_x[key] = "X"
        self.__logger.debug("LOGONDATAX: %s", str(self.logondata_x))
        for key in self.defaults_x:
            if key in parameters_names:
                self.defaults_x[key] = "X"
        self.__logger.debug("DEFAULTSX: %s", str(self.defaults_x))
        for key in self.address_x:
            if key in parameters_names:
                self.address_x[key] = "X"
        self.__logger.debug("ADDRESSX: %s", str(self.address_x))
        for key in self.snc_x:
            if key in parameters_names:
                self.snc_x[key] = "X"
        self.__logger.debug("SNCX: %s", str(self.snc_x))
