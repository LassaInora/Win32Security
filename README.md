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
- `2.0.1`

--------
## Summary

- **[Links](#links)**
- **[Methods](#methods)**
--------

## Links

- [Personal GitHub](https://github.com/LassaInora)
- [GitHub project](https://github.com/LassaInora/Win32Security)
- [Website project](https://lassainora.fr/projets/librairies/Win32Security)
- [Pypi project](https://pypi.org/project/Win32Security/)

--------
## Methods

 Execution: python -m Win32Security {path}
    
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


    def _get_data(data):
        if data[0] == SecurityObject:
          return data[0](data[1]).data
        else:
          return data[0](data[1])
    
        
    class YourClassName__:
        """Settings of YourClassName"""
        
        _YOURVARIABLENAME = (type_of_variable, "Your variable")
        
        @property
        def YOURVARIABLENAME(self):
            return _get_data(self._YOURVARIABLENAME)
    
    
    class ClassExample__:
        """Settings of ClassExample"""
        
        _DATA1 = (SecurityObject, "0a1b2c3d4e5f6g7h8i9j")  # Fake encrypted 'Banana'
        _DATA2 = (int, "42")
        _DATA3 = (str, "foo")
        
        @property
        def DATA3(self):
            return _get_data(self._DATA3)
        
        @property
        def DATA2(self):
            return _get_data(self._DATA2)
        
        @property
        def DATA1(self):
            return _get_data(self._DATA1)
    
    ...
  ```
  
  You can call its classes from your code normally, the value of their self will be the value of your variable transformed by the indicated class.
If you use the SecurityObject class then the encrypted value in your file will be decrypted when used without modifying the current file.
  
  ```python
    obj = ClassExample__().DATA1
    # obj -> 'Banana'
    obj = ClassExample__().DATA2
    # obj -> 42
    obj = ClassExample__().DATA3
    # obj -> 'foo'
  ```

  In order to create, modify or see your data it is advisable to refer to `python -m Win32Security`

        
