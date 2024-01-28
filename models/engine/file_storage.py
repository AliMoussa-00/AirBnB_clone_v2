#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    from models.base_model import BaseModel
    from models.user import User
    from models.place import Place
    from models.state import State
    from models.city import City
    from models.amenity import Amenity
    from models.review import Review

    classes = {
            'BaseModel': BaseModel, 'User': User, 'Place': Place,
            'State': State, 'City': City, 'Amenity': Amenity,
            'Review': Review
            }

    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""

        all_list = {}

        if cls and cls in FileStorage.classes.values():

            for k, v in FileStorage.__objects.items():
                # get the class from the 'key.id'
                key_class = k.split(".")[0]

                if key_class == cls.__name__:
                    all_list[k] = v

        else:
            all_list = FileStorage.__objects

        return all_list

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def reload(self):
        """Loads storage dictionary from file"""
        try:
            temp = {}
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    self.all()[key] = \
                            FileStorage.classes[val['__class__']](**val)

        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """delete obj from __objects if it exists"""

        if obj:
            # passing '__objects' in case we change it
            objs = FileStorage.__objects.copy()

            for k in objs.keys():

                obj_id = f"{obj.__class__.__name__}.{obj.id}"

                if obj_id == k:

                    FileStorage.__objects.pop(k)

    def close(self):
        """close the deserialization of data"""
        self.reload()
