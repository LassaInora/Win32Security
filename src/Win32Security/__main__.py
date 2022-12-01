import os
import sys

import LassaLib

from Win32Security import SecurityObject

_types = {
    "SecurityObject": SecurityObject,
    "str": str,
    "int": int,
    "float": float,
    "bool": bool,
    "list": list,
    "tuple": tuple,
    "dict": dict,
}

_commands = {
    'view': """Usage:
    python.exe -m Win32Security view <path of file>
    
General Options:
    -h, --help      Show help.
""",
    'edit': """Usage:
    python.exe -m Win32Security edit <path of file>
    
General Options:
    -h, --help      Show help.
""",
    'create': """Usage:
    python.exe -m Win32Security create [options]
    
General Options:
    -h, --help      Show help.
    -n, --name      Name of the file.
    -f, --folder    Folder of the file.
""",
    '_': """Usage:
    python.exe -m Win32Security <command> [options]
    
Commands:
    view            Checks class data of the configuration file set in parameter
    edit            Edit the configuration file set in parameter
    create          Create a configuration file named by default 'settings.py'
    
General Options:
    -h, --help      Show help.
""",
}


class Class:
    def __init__(self, data=..., *, name=...):
        if data is ... and name is ...:
            raise AttributeError("No attribute")

        if data is ...:
            self.name = name
            self.data = {}
        else:
            self.name = data.split('class __')[1].split('__(Params):')[0]
            self.data = {}

            for line in data.split("def __init__(self):")[1].splitlines()[1:]:
                try:
                    line: str
                    name, value = line.split('self.')[1].split(' = ')
                    type_, value = value[1:-1].split(', ')
                    self.data[name] = (type_, value[1:-1])
                except IndexError:
                    pass

    def get_attributes(self):
        return f"\n        ".join([f'self.{key} = ({value[0]}, "{value[1]}")' for key, value in self.data.items()])

    def __str__(self):
        return f'''
# <class>
class __{self.name}__(Params):
"""Settings of {self.name}"""

def __init__(self):
    {self.get_attributes()}
# </class>
'''


def help(command=...):
    if command is ... or command not in _commands:
        command = '_'

    print(_commands[command])


def edit(path):
    """Edit the configuration file set in parameter

    Parameters:
         path (str):  Path of file.
    """

    data = open(path, 'r').read()

    classes = [Class(class_) for class_ in [class_.split("# </class>")[0] for class_ in data.split('# <class>')[1:]]]

    run = True
    while run:
        os.system('CLS')
        print()
        chx = LassaLib.menu(
            ["Create new class"] + [c.name for c in classes], "Choice of class",
            can_back=True,
            desc="Choose your class to work on.\nAuto-save on exit"
        )

        match chx:
            case 0:
                run = False
            case 1:
                classes.append(Class(name=input("Class name: ").capitalize()))
            case _:
                class_ = classes[chx - 2]
                os.system('CLS')
                print()
                chx2 = LassaLib.menu(
                    ["Rename class", "Delete class", "Create new attribute"] + list(class_.data), f"Menu {class_.name}",
                    can_back=True
                )
                match chx2:
                    case 0:
                        pass
                    case 1:
                        new_name = input("New name: ").capitalize()
                        if LassaLib.enter(f"Rename {class_.name} for {new_name}?\n >> ", bool):
                            class_.name = new_name
                    case 2:
                        if LassaLib.enter(f"Are you sure you want to delete {class_.name}?\n >> ", bool):
                            classes.remove(class_)
                    case 3:
                        os.system('CLS')
                        print()
                        chx3 = LassaLib.menu(
                            _types, f"Menu create new attribute",
                            can_back=True,
                            desc="Choose your type"
                        )
                        if chx3 == 0:
                            break
                        else:
                            chx3 -= 1
                        type_ = _types[list(_types)[chx3]].__name__
                        name = input("Choose the name: ").upper()
                        value = input(f"Value of {name}: ")
                        if type_ == 'SecurityObject':
                            value = SecurityObject(value, True).encrypted_data
                        class_.data[name] = (type_, value)
                    case _:
                        attr_ = list(class_.data.keys())[chx2 - 4]
                        os.system('CLS')
                        print()
                        chx3 = LassaLib.menu(
                            [
                                f"Rename {attr_}",
                                f"Change {attr_}",
                                f"Delete {attr_}"
                            ], f"Menu {class_.name}.{attr_}",
                            can_back=True
                        )
                        match chx3:
                            case 0:
                                pass
                            case 1:
                                new_name = input("New name: ").upper()
                                if LassaLib.enter(f"Rename {attr_} for {new_name}?\n >> ", bool):
                                    class_.data[new_name] = class_.data[attr_]
                                    del class_.data[attr_]
                            case 2:
                                os.system('CLS')
                                print()
                                chx4 = LassaLib.menu(
                                    _types, f"Menu change attribute",
                                    can_back=True,
                                    desc="Choose your type"
                                )
                                if chx4 == 0:
                                    break
                                else:
                                    chx4 -= 1
                                type_ = list(_types.values())[chx4].__name__
                                value = input(f"Value of {attr_}: ")
                                if type_ == 'SecurityObject':
                                    value = SecurityObject(value, True).encrypted_data
                                class_.data[attr_] = (type_, value)
                            case 3:
                                if LassaLib.enter(f"Are you sure you want to delete {class_.name}.{attr_}?\n >> ",
                                                  bool):
                                    del class_.data[attr_]

    doc = "from Win32Security import *\n\n"
    print("Save...", end='')
    try:
        for class_ in classes:
            doc += "\n" + str(class_)
        open(path, 'w').write(doc)
        print(f"OK : {path}")
    except Exception as e:
        print(f"KO : {e}")


def create(name, folder):
    """Create a configuration file named by default 'settings.py'

    Parameters:
        name (str): Name of the file.
        folder (str): Folder of the file.
    """
    if not name.endswith('.py'):
        name += '.py'
    open(f"{folder}/{name}", 'w').write('')
    edit(f"{folder}/{name}")


def view(path):
    """Checks class data of the configuration file set in parameter

    Parameters:
         path (str):  Path of file.
    """

    class Viewer:
        def __init__(self, class_):
            self._class: Class = class_

        def __str__(self):
            return (
                    "  " + ("╔═" + "═" * len(self._class.name) + "═╗").center(self.max_length - 4) + "  " + "\n" +
                    "╔═" + f"╣ {self._class.name} ╠".center(self.max_length - 4, '═') + "═╗" + "\n" +
                    "║ " + ("╚═" + "═" * len(self._class.name) + "═╝").center(self.max_length - 4) + " ║" + "\n"
            ) + ''.join(self.make(key, value) for key, value in self._class.data.items()) + (
                    "╚" + "═" * (self.max_length - 2) + "╝" + "\n\n" +
                    "(Press enter for continue.)"
            )

        def make(self, key, value):
            value = str(_types[value[0]](value[1]))
            return (
                    "║ " + "┌─" + "─" * self.length_var + "─┐ ┌─" + "─" * self.length_value + "─┐" + " ║" + "\n" +
                    "║ " + f"│ {key.center(self.length_var)} ├─┤ {value.center(self.length_value)} │" + " ║" + "\n" +
                    "║ " + "└─" + "─" * self.length_var + "─┘ └─" + "─" * self.length_value + "─┘" + " ║" + "\n"
            )

        @property
        def length_title(self):
            return len(f"╔══╣ {self._class.name} ╠══╗")

        @property
        def length_var(self):
            return max(len(key) for key in self._class.data)

        @property
        def length_value(self):
            return max(len(str(_types[val[0]](val[1]))) for val in self._class.data.values())

        @property
        def length_data(self):
            return len("║ │ " + "*"*self.length_var + " ├─┤ " + "*"*self.length_value + " │ ║")

        @property
        def max_length(self):
            return max(self.length_title, self.length_data)


    data = open(path, 'r').read()

    classes = [Class(class_) for class_ in [class_.split("# </class>")[0] for class_ in data.split('# <class>')[1:]]]

    run = True
    while run:
        os.system('CLS')
        print()
        chx = LassaLib.menu(
            [c.name for c in classes], "View a class",
            can_back=True
        )

        match chx:
            case 0:
                run = False
            case _:
                os.system('CLS')
                print()
                input(str(Viewer(classes[chx - 1])))


if __name__ == '__main__':
    keys = {
        'help': "Show help.",
        'edit <path>': "Edit config file",
        'create <path>': "Create config file"
    }
    sys.argv = sys.argv[1:]
    try:
        cmd, sys.argv = sys.argv[0], sys.argv[1:]
    except IndexError:
        cmd = '_'

    PATH = os.getcwd().replace('\\', '/')

    if '-h' in sys.argv or '--help' in sys.argv:
        help(cmd)
    else:
        match cmd:
            case 'edit':
                edit(sys.argv[0])
            case 'view':
                view(sys.argv[0])
            case 'create':
                if '-n' in sys.argv:
                    name = sys.argv.pop(sys.argv.index('-n') + 1)
                    sys.argv.pop(sys.argv.index('-n'))
                elif '--name' in sys.argv:
                    name = sys.argv.pop(sys.argv.index('--name') + 1)
                    sys.argv.pop(sys.argv.index('--name'))
                else:
                    name = 'settings.py'

                if '-f' in sys.argv:
                    folder = sys.argv.pop(sys.argv.index('-f') + 1)
                    sys.argv.pop(sys.argv.index('-f'))
                elif '--folder' in sys.argv:
                    folder = sys.argv.pop(sys.argv.index('--folder') + 1)
                    sys.argv.pop(sys.argv.index('--folder'))
                else:
                    folder = os.getcwd().replace('\\', '/')

                create(name, folder)

            case _:
                help()
