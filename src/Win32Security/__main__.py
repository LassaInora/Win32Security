import os
import sys

import LassaLib

from Win32Security import SecurityObject


class FILE:
    class CLASS:
        class ATTR:
            def __init__(self, data: str):
                self.data = data.splitlines()[0]
                self.name = (self.data.split(' = ')[0])
                self.type = self.data.split(' = ')[1][1:-1].split(', ')[0]
                self.value = self.data.split(' = ')[1][1:-1].split(', ')[1][1:-1]

            def get_set(self):
                return f'    _{self.name.upper()} = ({self.type}, "{self.value}")'

            def get_property(self):
                return (
                    f"\n"
                    f"    @property\n"
                    f"    def {self.name.upper()}(self):\n"
                    f"        return _get_data(self._{self.name.upper()})\n"
                )

        def __init__(self, data: str):
            self.data = '\n'.join(data.splitlines()[3:])
            self.name = data.splitlines()[0][6:-3]
            self.attributes = self.get_attributes()

        def get_attributes(self):
            return [self.ATTR(attribute) for attribute in self.data.split('    _')[1:]]

        def __str__(self):
            attrs = ""
            for attr in self.attributes:
                attrs = attr.get_set() + "\n" + attrs
                attrs += attr.get_property()

            return (
                       f'class {self.name}__:\n'
                       f'    """Settings of {self.name}"""\n'
                       f'\n'
                   ) + attrs

    def __init__(self, name: str):
        name = name.replace('\\', '/')
        if '/' in name:
            self.path = '/'.join(name.split('/')[:-1]) + '/'
            self.name = '.'.join(name.split('/')[-1].split('.')[:-1]) if '.' in name.split('/')[-1] else name.split('/')[-1]
        else:
            self.path = ''
            self.name = '.'.join(name.split('.')[:-1]) if '.' in name else name
        try:
            self.data = open(self.path + self.name + '.py', 'r').read()
        except FileNotFoundError:
            self.data = ''
        self.classes = self.get_classes()
        self.locked = self.data.split('# <lock:')[1].split('>')[0] == 'True'

    def get_classes(self):
        return [self.CLASS('class ' + class_) for class_ in self.data.split('class ')[1:]]

    def __str__(self):
        return (
                "from Win32Security import SecurityObject\n"
                "\n"
                f"# <lock:{self.locked}>\n"
                "\n"
                "\n"
                "def _get_data(data):\n"
                "    if data[0] == SecurityObject:\n"
                "        return data[0](data[1]).data\n"
                "    else:\n"
                "        return data[0](data[1])\n"
                "\n"
                "\n"
               ) + '\n\n'.join(str(class_) for class_ in self.classes)

    def save(self):
        open(self.path + self.name + '.py', 'w').write(str(self))
        print(self.name + '.py has been saved.')


class MENU:
    def __init__(self, file):
        """Execute Menu for file

        Parameters:
            file (str or FILE): The file
        """
        if isinstance(file, str):
            file = FILE(file)

        self.file: FILE = file
        self._exit = False

    def home(self):
        self._exit = False
        while not self._exit:
            _clear()
            match LassaLib.menu(
                ['VIEW', 'LOCK / UNLOCK', 'EDIT', 'DELETE'], f'{self.file.name} Home',
                can_back=True,
                desc=f'{self.file.path}{self.file.name}.py\nis\n{"LOCK" if self.file.locked else "UNLOCK"}'
            ):
                case 0: self._exit = True
                case 1: self.view()
                case 2:
                    self.file.locked = not self.file.locked
                    for class_ in self.file.classes:
                        for attr_ in class_.attributes:
                            self.set_var(attr_, type=attr_.type)
                case 3: self.edit()
                case 4:
                    _clear()
                    if LassaLib.menu(['YES', 'NO'], f'Delete {self.file.name}?') == 1 and os.path.exists(
                            f'{self.file.path}{self.file.name}.py'):
                        match os.name:
                            case 'posix':
                                os.system(f'rm {self.file.path}{self.file.name}.py')
                            case 'nt':
                                os.system(f'del {self.file.path}{self.file.name}.py')
                    exit()

    def view(self):
        exit_view = False
        while not exit_view:
            class_ = self.select_class()
            if class_ is not None:
                self.display_class(class_)
            else:
                exit_view = True

    def edit(self):
        exit_edit = False
        while not exit_edit:
            _clear()
            match LassaLib.menu(
                ['Add class', 'Edit class', 'Delete class'], f'Edit {self.file.name}',
                can_back=True,
                desc=f'{self.file.path}{self.file.name}.py'
            ):
                case 0: exit_edit = True
                case 1: self.file.classes.append(FILE.CLASS(f"class {input('Choose a name: ')}__:\n"))
                case 2: self.edit_class()
                case 3:
                    class_ = self.select_class()
                    if class_ is not None:
                        _clear()
                        if LassaLib.menu(['YES', 'NO'], f'Delete {class_.name}?') == 1:
                            self.file.classes.remove(class_)

    def edit_class(self):
        class_ = self.select_class()
        if class_ is not None:
            exit_edit_class = False
            while not exit_edit_class:
                _clear()
                match LassaLib.menu([f'Rename {class_.name}', 'Add attribute', 'Edit attribute'], f'Edit {class_.name}', can_back=True):
                    case 0: exit_edit_class = True
                    case 1: class_.name = input('Choose a name: ')
                    case 2:
                        name = input('Enter the name: ')
                        type_ = input('Enter the type: ')
                        if type_.lower() == 'secure' or type_.lower() == 'securityobject':
                            type_ = 'SecurityObject'
                        value = input('Enter the value: ') if type_ != 'SecurityObject' or self.file.locked else SecurityObject(input('Enter the value'), encrypt=True).encrypted_data
                        class_.attributes.append(FILE.CLASS.ATTR(f"{name} = ({type_}, \"{value}\")"))
                    case 3: self.edit_attribute(class_)

    def edit_attribute(self, class_):
        attr_ = self.select_attributes(class_)
        if attr_ is not None:
            exit_edit_attribute = False
            while not exit_edit_attribute:
                _clear()
                match LassaLib.menu(
                    [f'Rename {attr_.name}', 'Change type', 'Change value', f'Delete {attr_.name}'],
                    f'Edit {class_.name}.{attr_.name}', can_back=True
                ):
                    case 0: exit_edit_attribute = True
                    case 1: self.set_var(attr_, name=input('Choose a name: '))
                    case 2: self.set_var(attr_, type=input('Enter a type: '),)
                    case 3: self.set_var(attr_, value=input('Enter the new value: '))
                    case 4:
                        _clear()
                        if LassaLib.menu(['YES', 'NO'], f'Delete {class_.name}.{attr_.name}?') == 1:
                            class_.attributes.remove(attr_)
                        exit_edit_attribute = True

    def set_var(self, attr, *, name=None, type=None, value=None):
        if name is not None:
            attr.name = name

        if type is not None or value is not None:
            if attr.type == 'SecurityObject':
                attr.value = SecurityObject(attr.value).data

            if type is not None:
                if type.lower() == 'secure' or type.lower() == 'securityobject':
                    attr.type = 'SecurityObject'
                else:
                    attr.type = type

            if attr.type == 'SecurityObject' and self.file.locked:
                attr.value = SecurityObject(value if value is not None else attr.value, encrypt=True).encrypted_data
            else:
                attr.value = value if value is not None else attr.value

    def select_class(self):
        _clear()
        res = LassaLib.menu(
            [class_.name for class_ in self.file.classes], 'Choose a class',
            can_back=True
        )
        if res == 0:
            return None
        else:
            return self.file.classes[res - 1]

    def select_attributes(self, class_=None):
        if class_ is None:
            class_ = self.select_class()
        if class_ is not None:
            _clear()
            res = LassaLib.menu(
                [attr.name for attr in class_.attributes], 'Choose an attribute',
                can_back=True
            )
            if res != 0:
                return class_.attributes[res - 1]
        return None

    def run(self):
        self.home()
        self.file.save()

    def display_class(self, class_=None):
        """ Display class

        Parameters:
            class_ (FILE.CLASS): The class
        """
        """ Model:
             ╔══════════════╗         
    ╔════════╣  class name  ╠════════╗
    ║        ╚══════════════╝        ║
    ║    ┌──────────────────────┐    ║
    ║    │  Settings of class   │    ║
    ║    └──────────────────────┘    ║
    ║                                ║
    ║ ┌──────┐ ┌─────┐ ┌───────────┐ ║
    ║ │ VAR1 ├─┤ int ├─┤  VALUE 1  │ ║
    ║ └──────┘ └─────┘ └───────────┘ ║
    ║ ┌──────┐ ┌─────┐ ┌───────────┐ ║
    ║ │ VAR1 ├─┤ str ├─┤  VALUE 2  │ ║
    ║ └──────┘ └─────┘ └───────────┘ ║
    ╟--------------------------------╢
    ║  ┌──────────────────────────┐  ║
    ║  │   Press enter to exit    │  ║
    ║  └──────────────────────────┘  ║
    ╚════════════════════════════════╝
        """
        if class_ is None:
            class_ = self.select_class()
        if class_ is not None:
            max_name, max_type, max_value = 0, 0, 0
            for attr in class_.attributes:
                if attr.type == 'SecurityObject':
                    value = SecurityObject(attr.value).data
                else:
                    value = attr.value
                if len(value) > 100:
                    value = value[:97] + '...'
                max_name = max(max_name, len(attr.name))
                max_type = max(max_type, len(attr.type))
                max_value = max(max_value, len(value))

            max_length = max(
                len(f"╔══╣  {class_.name}  ╠══╗"),
                len(f"║   │  Settings of {class_.name}   │    ║"),
                len(f"║ │ {'*' * max_name} ├─┤ {'*' * max_type} ├─┤ {'*' * max_value} │ ║")
            )
            val_length = max_value + (max_length - len(f"║ │ {'*' * max_name} ├─┤ {'*' * max_type} ├─┤ {'*' * max_value} │ ║"))

            bloc = ""

            bloc += (f"╔══{'═'*len(class_.name)}══╗".center(max_length, ' ')) + "\n"
            bloc += ("╔══" + f"╣  {class_.name}  ╠".center(max_length - 6, '═') + "══╗") + "\n"
            bloc += ("║  " + f"╚══{'═'*len(class_.name)}══╝".center(max_length - 6, ' ') + "  ║") + "\n"
            var = max_length - len(f"║ │  Settings of {class_.name}  │ ║")
            part = [
                var // 4 + (1 if var % 4 > 0 else 0),
                var // 4 + (1 if var % 4 > 1 else 0),
                var // 4 + (1 if var % 4 > 2 else 0),
                var // 4
            ]
            bloc += ("║ " + " "*part[0] + "┌─" + "─"*part[1] + f"─────────────{'─'*len(class_.name)}─" + "─"*part[2] + "─┐" + " "*part[3] + " ║") + "\n"
            bloc += ("║ " + " "*part[0] + "│ " + " "*part[1] + f" Settings of {class_.name} " + " "*part[2] + " │" + " "*part[3] + " ║") + "\n"
            bloc += ("║ " + " "*part[0] + "└─" + "─"*part[1] + f"─────────────{'─'*len(class_.name)}─" + "─"*part[2] + "─┘" + " "*part[3] + " ║") + "\n"
            bloc += ('║' + ' '*(max_length - 2) + '║') + "\n"
            for attr in class_.attributes:
                if attr.type == 'SecurityObject':
                    value = SecurityObject(attr.value).data
                else:
                    value = attr.value
                if len(value) > 100:
                    value = value[:97] + '...'
                bloc += f"║ ┌─{'─' * max_name}─┐ ┌─{'─' * max_type}─┐ ┌─{'─' * val_length}─┐ ║" + "\n"
                bloc += f"║ │ {attr.name.center(max_name, ' ')} ├─┤ {attr.type.center(max_type, ' ')} ├─┤ {LassaLib.position('LEFT', value, val_length, ' ')} │ ║" + "\n"
                bloc += f"║ └─{'─' * max_name}─┘ └─{'─' * max_type}─┘ └─{'─' * val_length}─┘ ║" + "\n"
            bloc += ('╟' + '-'*(max_length - 2) + '╢') + "\n"
            part = [
                (max_length - 29) // 4 + (1 if (max_length - 29) % 4 > 0 else 0),
                (max_length - 29) // 4 + (1 if (max_length - 29) % 4 > 1 else 0),
                (max_length - 29) // 4 + (1 if (max_length - 29) % 4 > 2 else 0),
                (max_length - 29) // 4
            ]
            bloc += ("║ " + " "*part[0] + "┌─" + "─"*part[1] + f"─────────────────────" + "─"*part[2] + "─┐" + " "*part[3] + " ║") + "\n"
            bloc += ("║ " + " "*part[0] + "│ " + " "*part[1] + f" Press enter to exit " + " "*part[2] + " │" + " "*part[3] + " ║") + "\n"
            bloc += ("║ " + " "*part[0] + "└─" + "─"*part[1] + f"─────────────────────" + "─"*part[2] + "─┘" + " "*part[3] + " ║") + "\n"
            bloc += ('╚' + '═'*(max_length - 2) + '╝')

            _clear()
            input(bloc)


def _clear():
    match os.name:
        case 'posix':
            os.system('clear')
            print()
        case 'nt':
            os.system('cls')
            print()


if __name__ == '__main__':
    MENU('settings' if len(sys.argv) <= 1 else sys.argv[1]).run()
