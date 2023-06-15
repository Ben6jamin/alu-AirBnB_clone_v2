#!/usr/bin/python3
""" Console Module """
import cmd
import sys
from models.base_model import BaseModel
from models.__init__ import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """ Contains the functionality for the HBNB console"""

    # determines prompt for interactive/non-interactive modes
    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ''

    classes = {
        'BaseModel': BaseModel, 'User': User, 'Place': Place,
        'State': State, 'City': City, 'Amenity': Amenity,
        'Review': Review
    }
    dot_cmds = ['all', 'count', 'show', 'destroy', 'update']
    types = {
        'number_rooms': int, 'number_bathrooms': int,
        'max_guest': int, 'price_by_night': int,
        'latitude': float, 'longitude': float
    }

    def preloop(self):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb)')

    def precmd(self, line):
        """Reformat command line for advanced command syntax.

        Usage: <class name>.<command>([<id> [<*args> or <**kwargs>]])
        (Brackets denote optional fields in usage example.)
        """
        _cmd = _cls = _id = _args = ''  # initialize line elements

        # scan for general formatting - i.e '.', '(', ')'
        if not ('.' in line and '(' in line and ')' in line):
            return line

        try:  # parse line left to right
            pline = line[:]  # parsed line

            # isolate <class name>
            _cls = pline[:pline.find('.')]

            # isolate and validate <command>
            _cmd = pline[pline.find('.') + 1:pline.find('(')]
            if _cmd not in HBNBCommand.dot_cmds:
                raise Exception

            # if parentheses contain arguments, parse them
            pline = pline[pline.find('(') + 1:pline.find(')')]
            if pline:
                # partition args: (<id>, [<delim>], [<*args>])
                pline = pline.partition(', ')  # pline converted to tuple

                # isolate _id, stripping quotes
                _id = pline[0].replace('\"', '')
                # check if _id is an empty string
                if not _id:
                    _id = None

                # if arguments exist beyond _id
                pline = pline[2].strip()  # pline is now str
                if pline:
                    # check for *args or **kwargs
                    if pline[0] == '{' and pline[-1] == '}' \
                            and type(eval(pline)) is dict:
                        _args = pline
                    else:
                        _args = pline.replace(',', '')
                        # _args = _args.replace('\"', '')
            line = ' '.join([_cmd, _cls, str(_id), _args])

        except Exception as mess:
            pass
        finally:
            return line

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def emptyline(self):
        """Called when an empty line is entered in response to the prompt."""
        pass

    def do_EOF(self, arg):
        """EOF command to exit the program"""
        print()  # newline
        return True

    def help_EOF(self):
        """Help message for EOF command"""
        print("Quit the console by pressing Ctrl+D or using the EOF command.")

    def do_create(self, arg):
        """Creates a new instance of BaseModel, saves it to JSON file, and prints the id"""
        if not arg:
            print("** class name missing **")
        elif arg not in HBNBCommand.classes:
            print("** class doesn't exist **")
        else:
            new_instance = HBNBCommand.classes[arg]()
            new_instance.save()
            print(new_instance.id)

    def do_show(self, arg):
        """Prints the string representation of an instance based on the class name and id"""
        if not arg:
            print("** class name missing **")
        else:
            arg_list = arg.split()
            if arg_list[0] not in HBNBCommand.classes:
                print("** class doesn't exist **")
            elif len(arg_list) < 2:
                print("** instance id missing **")
            else:
                key = "{}.{}".format(arg_list[0], arg_list[1])
                all_objs = storage.all()
                if key not in all_objs:
                    print("** no instance found **")
                else:
                    print(all_objs[key])

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id, then saves the change to the JSON file"""
        if not arg:
            print("** class name missing **")
        else:
            arg_list = arg.split()
            if arg_list[0] not in HBNBCommand.classes:
                print("** class doesn't exist **")
            elif len(arg_list) < 2:
                print("** instance id missing **")
            else:
                key = "{}.{}".format(arg_list[0], arg_list[1])
                all_objs = storage.all()
                if key not in all_objs:
                    print("** no instance found **")
                else:
                    del all_objs[key]
                    storage.save()

    def do_all(self, arg):
        """Prints all string representation of all instances based or not on the class name"""
        arg_list = arg.split()
        all_objs = storage.all()
        obj_list = []
        if not arg:
            for obj_key in all_objs:
                obj_list.append(str(all_objs[obj_key]))
        elif arg_list[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        else:
            for obj_key in all_objs:
                if obj_key.split('.')[0] == arg_list[0]:
                    obj_list.append(str(all_objs[obj_key]))
        print(obj_list)

    def do_update(self, arg):
        """Updates an instance based on the class name and id by adding or updating an attribute"""
        arg_list = arg.split()
        all_objs = storage.all()
        if not arg:
            print("** class name missing **")
        elif arg_list[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
        elif len(arg_list) < 2:
            print("** instance id missing **")
        elif "{}.{}".format(arg_list[0], arg_list[1]) not in all_objs:
            print("** no instance found **")
        elif len(arg_list) < 3:
            print("** attribute name missing **")
        elif len(arg_list) < 4:
            print("** value missing **")
        else:
            key = "{}.{}".format(arg_list[0], arg_list[1])
            obj = all_objs[key]
            attr = arg_list[2]
            value = arg_list[3].strip('"')
            if attr in HBNBCommand.types:
                value = HBNBCommand.types[attr](value)
            setattr(obj, attr, value)
            obj.save()

    def help_quit(self):
        """Help message for quit command"""
        print("Quit the console.")

    def help_EOF(self):
        """Help message for EOF command"""
        print("Quit the console by pressing Ctrl+D or using the EOF command.")

    def help_create(self):
        """Help message for create command"""
        print("Create a new instance of a class, save it, and display its id.")

    def help_show(self):
        """Help message for show command"""
        print("Display the string representation of an instance.")

    def help_destroy(self):
        """Help message for destroy command"""
        print("Delete an instance based on the class name and id.")

    def help_all(self):
        """Help message for all command"""
        print("Display string representations of all instances, or of a specific class if specified.")

    def help_update(self):
        """Help message for update command"""
        print("Update an instance based on the class name and id by adding or updating an attribute.")


if __name__ == '__main__':
    HBNBCommand().cmdloop()
