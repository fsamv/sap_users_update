"""Main programm"""
import argparse
import getpass
import csv
import sys
from sapsyslib import SAPSystem
from passhandlerlib import PassHandler
from logginglib1 import Log

def run_rfc_function():
    """Run rfc function"""
    if args.rfc_func_name == "ping":
        sap_system = SAPSystem(args.config_file.name, loggerget)
        sap_system.ping()
    elif args.rfc_func_name == "bapi_user_change":
        if args.csv_file_name:
            sap_system = SAPSystem(args.config_file.name, loggerget)
            parameters_names, parameters_values = get_csv_data(args.csv_file_name.name)
            sap_system.bapi_user_change(parameters_names, parameters_values)
        else:
            logger_main.error("ERROR: Specify CSV file with RFC Function parameters")
            parser.print_help()
    else:
        logger_main.error("ERROR: Wrong function name!")

def set_password(config_file):
    """Set password in ini file"""
    logger_main.info("Saving password to ini file.")
    password = getpass.getpass(prompt="Enter your password: ")
    pass_h = PassHandler(config_file, loggerget)
    pass_h.store_password(password)

def check_password(config_file):
    """Check password in ini file"""
    logger_main.info("Checking password from ini file.")
    password = getpass.getpass(prompt="Enter your password: ")
    pass_h = PassHandler(config_file, loggerget)
    pass_h.check_password(password)

#Get input parameters
def create_parser ():
    """Create argument parser"""
    my_parcer = argparse.ArgumentParser(
        description = '''Update SAP users with BAPI bapi_user_change''',
        epilog = '''version 1.0.0 (c) 2023 Semen Fedkin, fc13adm@gmail.com''',
        add_help=False)

    parent_group = my_parcer.add_argument_group (title='Parameters')
    parent_group.add_argument("-f", "--config-file", type=argparse.FileType(),
                                default="connection.ini", help="Configuration file name")
    parent_group.add_argument ('--debug', action='store_true', default=False, help='Debug mode')
    parent_group.add_argument ('--help', '-h', action='help', help='Help')

    sub_parsers = my_parcer.add_subparsers (dest='command', title = 'Commands',
                                        description = 'First parameters of %(prog)s')

    run_parser = sub_parsers.add_parser("run", help="Run RFC function")
    run_group = run_parser.add_argument_group (title='Parameters')
    run_group.add_argument("-n", "--rfc-func-name", type=str,
                            required=True, choices=["ping", "bapi_user_change"],
                            help="RFC function name (allowed values: ping, bapi_user_change)")
    run_group.add_argument("-c", "--csv-file-name",type=argparse.FileType(),
                            required=False, help="CSV with RFC Function parameters")

    set_p_parser = sub_parsers.add_parser("set_pass", help="Set password for connection user")

    check_p_parser = sub_parsers.add_parser("check_pass",
                                            help="Check if password provided is saved in ini file")

    return my_parcer

def get_csv_data(file_name):
    """Read CSV data"""
    try:
        with open(file_name, 'r', encoding='utf-8-sig') as file:
            reader = csv.reader(file, delimiter=';')
            logger_main.debug("Readed CSV: %s", str(reader))
            parameters_names = next(reader)
            logger_main.debug("Parameters Names: %s", str(parameters_names))
            parameters_values = [{parameters_names[i]:row[i] for i in range(len(parameters_names))} for row in reader]
            logger_main.debug("Parameters Valies: %s", str(parameters_values))
        if parameters_names[0] != "USERNAME":
            logger_main.error("An ERROR in file format! %s First coloumn: %s", file_name, parameters_names[0])
            sys.exit()
        else:
            return parameters_names, parameters_values
    except Exception as error:
        logger_main.error("An ERROR occurred when open %s: %s", file_name, error)
        sys.exit()

if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()
    if args.debug:
        LOG_LVL = "DEBUG"
    else:
        LOG_LVL = "INFO"
    loggerget = Log(args.config_file.name, LOG_LVL)
    logger_main = loggerget.get_logger("sap-users-upd")
    logger_main.debug("Arguments: %s", str(args))
    if args.command == "run":
        run_rfc_function()
    elif args.command == "set_pass":
        set_password(args.config_file.name)
    elif args.command == "check_pass":
        check_password(args.config_file.name)
    else:
        parser.print_help()
