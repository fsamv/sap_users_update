# **SAP User Updater**

This program is designed to update SAP users with the BAPI **`bapi_user_change`**. The program has several arguments that allow for configuration and control of the process.

## **Parameters**

- **`f, --config-file`** - Configuration file name, with default value of **`connection.ini`**.
- **`-debug`** - Debug mode, with default value of **`False`**.
- **`-help, -h`** - Help.

## **Commands**

### **`run`**

This command runs the RFC function with the following parameters:

- **`n, --rfc-func-name`** - Required parameter with allowed values **`ping`** or **`bapi_user_change`**.
- **`c, --csv-file-name`** - Optional parameter for a CSV file with the RFC function parameters.

### **`set_pass`**

This command sets the password for the connection user.

### **`check_pass`**

This command checks if the password provided is saved in the ini file.

## **Prerequisites**

To run this program, you will need to perform the following steps:

1. Unzip the file **`nwrfc750P_10-70002752_linx86_64.zip`** using the command **`unzip nwrfc750P_10-70002752_linx86_64.zip`**.
2. Create a directory in the path **`/usr/sap/`** using the command **`sudo mkdir /usr/sap/`**.
3. Move the unzipped folder to the directory **`/usr/sap/`** using the command **`sudo mv ./nwrfc750P_10-70002752_linx86_64 /usr/sap/nwrfcsdk`**.
4. Switch to the root user using the command **`sudo su -`**.
5. Create a new configuration file in the path **`/etc/ld.so.conf.d/`** using the command **`echo '/usr/sap/nwrfcsdk/lib' > /etc/ld.so.conf.d/nwrfcsdk.conf`**.
6. Run the command **`ldconfig`** to refresh the shared library cache.
7. Check the library cache using the command **`ldconfig -p | grep sap`**.
8. Set the environment variable **`SAPNWRFC_HOME`** to the path **`/usr/sap/nwrfcsdk/`** using the command **`export SAPNWRFC_HOME=/usr/sap/nwrfcsdk/`**.
9. Install pipenv using the command **`pip install pipenv`**.
10. Use pipenv to install the required dependencies using the command **`pipenv install`**.

## **Usage**

To use this program, the following command line format should be used:

```bash

python <program_name.py> [-h] [--debug] [-f CONFIG_FILE]
                         {run,set_pass,check_pass} ...
```

For more information on the arguments and commands, run the program with the **`-h`** or **`--help`** option.

Please use the csv template from the file csv_file.tmpl.
The first row is the names of the fields that are changed in the SAP system. A description of the fields is provided in the "Structures passed as input to BAPI_USER_CHANGE" section.

**Note: You cannot add new fields!**

If fields do not need to be changed - they should be removed from the file. Then we fill in the file with values and specify its name when starting the program.

## Structures passed as input to BAPI_USER_CHANGE

### LOGONDATA

| Field name  | Description |
| ----------- | ----------- |
| GLTGV | User valid from |
| GLTGB | User valid to |
| USTYP | User Type |
| TZONE | Time Zone |

### DEFAULTS

| Field name  | Description |
| ----------- | ----------- |
| STCOD | Start menu (old, replaced by XUSTART) |
| SPLD | Spool: Output device |
| DATFM | Date format |
| DCPFM | Decimal notation |
| LANGU | Language |
| START_MENU | Start menu |
| TIMEFM | Time Format (12-/24-Hour Specification) |

### ADDRESS

| Field name  | Description |
| ----------- | ----------- |
| FIRSTNAME | First Name |
| LASTNAME | Last name |
| DEPARTMENT | Department |
| FUNCTION | Function |
| CITY | City |
| TEL1_NUMBR | First telephone no.: dialling code+number |
| TEL1_EXT | E-Mail Address |

### SNC

| Field name  | Description |
| ----------- | ----------- |
| GUIFLAG | Permit password logon for SAP GUI (user-specific) |
| PNAME | SNC: Printable name |

## **Version and Contact Information**

This program is version 3.0 and was created by Semen Fedkin. You can contact him at **[fc13adm@gmail.com](mailto:fc13adm@gmail.com)**.
