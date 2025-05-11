import json
import os

# Save data, which must persist over sessions

class SaveManager:
    __path = "src/assets/current_save.json"
    __allowed_keys = ["highscore", "fall_count", "squish_count"]

    @classmethod
    def decode(cls) -> dict:
        if (not os.path.exists(cls.__path)):
            return None
        data = None
        with open(cls.__path, 'r') as target:
            data = json.loads(target.read())
        if (not cls.is_valid(data)):
            raise ValueError("data fields were incorrect")
        return data

    @classmethod
    def encode(cls, data: dict):
        if (not cls.is_valid(data)):
            raise ValueError("data fields were incorrect")

        updated = None
        if (os.path.exists(cls.__path)):
            with open(cls.__path, 'r') as target:
                old = json.loads(target.read())
            updated = cls.copy_data(data, old)
        else:
            updated = data

        with open(cls.__path, 'w') as target:
            target.write(json.dumps(updated))
    
    @classmethod
    def copy_data(cls, new_data: dict, old_data: dict) -> dict:
        for k in cls.__allowed_keys:
            if (old_data[k] < new_data[k]):
                old_data[k] = new_data[k]
        return old_data

    @classmethod
    def is_valid(cls, data: dict) -> bool:
        count = 0
        for key, value in data.items():
            if (key not in cls.__allowed_keys):
                return False
            else:
                count += 1
            if (not str.isdigit(str(value))):
                return False
        if (count != len(cls.__allowed_keys)):
            return False
        return True
