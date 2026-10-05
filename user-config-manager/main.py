'''
This program is a simple user settings/configuration manager 
that allows users to add new settings to a pre-existing dictionary of settings.
'''

test_settings = {
    "theme": "dark",
    "language": "en",
    "notifications": True,
}

# Function that lowers the case of the key and value that is given to it, checks if the key already exits in the dictionary, and if it does not, adds the key-value pair to the dictionary.

def add_setting(key, value):
    lower_key = key.lower()
    lower_value = value.lower()

    if lower_key in test_settings:
        return f"Setting '{lower_key}' already exists! Cannot add a new setting with this name."

    test_settings[lower_key] = lower_value
    return f"Setting '{lower_key}' added with value '{lower_value}' successfully!"

def update_setting(key, value):
    pass



print(add_setting("THEME", "LIGHT"))
print(add_setting("newkey", "newvalue"))



