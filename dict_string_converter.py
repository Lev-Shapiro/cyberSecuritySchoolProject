import json

class DictStringConverter:
    @staticmethod
    def convertToStr(data: dict) -> str:
        # Use JSON to serialize the dictionary to a string
        return json.dumps(data)
    
    @staticmethod
    def convertToDict(data_str: str) -> dict:
        # Use JSON to deserialize the string back to a dictionary
        return json.loads(data_str)