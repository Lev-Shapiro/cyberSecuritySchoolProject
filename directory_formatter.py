class DictionaryFormatter:
    def __init__(self, data):
        self.data = data

    def format_dict(self, data=None, indent=0):
        if data is None:
            data = self.data

        result = ""
        for key, value in data.items():
            result += " " * indent + f"{key}: "
            if isinstance(value, dict):
                result += "\n" + self.format_dict(value, indent + 4)
            else:
                result += f"{value}\n"
        return result

    def print_formatted(self):
        formatted_text = self.format_dict()
        print(formatted_text)