# Win32Security

#### _Data secured by the Windows API_

Author:
-------
- [Axelle (LassaInora) VIANDIER](mailto:axelleviandier@lassainora.fr)

License:
--------
- GNU General Public License v3.0

Version:
--------
- `1.0.0`

--------
## Summary

- **[Links](#links)**
- **[Contacts](#contacts)**
- **[Methods](#methods)**
--------

## Links

- [Personal GitHub](https://github.com/LassaInora)
- [GitHub project](https://github.com/LassaInora/Win32Security)
- [Website project](https://lassainora.fr/projets/librairies/Win32Security)
- [Pypi project](https://pypi.org/project/Win32Security/)

--------
## Methods

- ### python -m Win32Security \<command> \[options]
  - help
    ```
    Usage:
        python.exe -m Win32Security <command> [options]
      
    Commands:
        view            Checks class data of the configuration file set in parameter
        edit            Edit the configuration file set in parameter
        create          Create a configuration file named by default 'settings.py'
      
    General Options:
        -h, --help      Show help.
    
  - view
    ```
    Usage:
        python.exe -m Win32Security view <path of file>
    
    General Options:
        -h, --help      Show help.
    
  - edit
    ```
    Usage:
        python.exe -m Win32Security edit <path of file>
    
    General Options:
        -h, --help      Show help.
    
  - create
    ```
    Usage:
        python.exe -m Win32Security create [options]
    
    General Options:
        -h, --help      Show help.
        -n, --name      Name of the file.
        -f, --folder    Folder of the file.
    
- ### import Win32Security
  - #### class SecurityObject
    - SecurityObject(data_=None, encrypt=False)
      - data_ (str): The encrypted or decrypted data to be saved.
      - encrypt (bool): Should the data be encrypted?
    - data (str)
      - The decrypted data
    - encrypted_data (str)
      - The encrypted data


  To use Win32Security you must create a python file which will be your parameter file.
  This should look like this:

  ```python
from Win32Security import *
  
  
# <class>
class __YourClassName__(Params):
  """Settings of YourClassName"""
  
  def __init__(self):
    self.YOURVARIABLENAME = (type_of_variable, "Your variable")
# </class>
  

# <class>
class __ClassExample__(Params):
  """Settings of YourSecondClassName"""
  
  def __init__(self):
    self.DATA1 = (SecurityObject, "0a1b2c3d4e5f6g7h8i9j")  # Fake encrypted 'Banana'
    self.DATA2 = (int, "42")
    self.DATA3 = (str, "foo")
# </class>
  
...
  ```
  
  You can call its classes from your code normally, the value of their self will be the value of your variable transformed by the indicated class.
If you use the SecurityObject class then the encrypted value in your file will be decrypted when used without modifying the current file.
  
  ```python
obj = __ClassExample__().DATA1
# obj -> 'Banana'
obj = __ClassExample__().DATA2
# obj -> 42
obj = __ClassExample__().DATA3
# obj -> 'foo'
  ```

  In order to create, modify or see your data it is advisable to refer to `python -m Win32Security`

        