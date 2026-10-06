'''
This program is a simple user settings/configuration manager 
that allows users to add new settings to a pre-existing dictionary of settings.
'''

test_settings = {
    "theme": "dark",
    "language": "en",
    "notifications": True,
}

# Add-setting function that lowers the case of the key and value that is given to it, checks if the key already exits in the dictionary, and if it does not, adds the key-value pair to the dictionary.

def add_setting(key, value):
    lower_key = key.lower()
    lower_value = value.lower()

    if lower_key in test_settings:
        return f"Setting '{lower_key}' already exists! Cannot add a new setting with this name."

    test_settings[lower_key] = lower_value
    return f"Setting '{lower_key}' added with value '{lower_value}' successfully!"

# Update-setting function that lowers the case of the key and value that is given to it, checks if the key already exists in the dictionary, and if it does, updates the value of the key in the dictionary.

def update_setting(key, value):
    lower_key = key.lower()
    lower_value = value.lower()

    if lower_key in test_settings:
        test_settings[lower_key] = lower_value
        return f"Setting '{lower_key}' updated to '{lower_value}' successfully!"
    elif lower_key not in test_settings:
        return f"Setting '{lower_key}' does not exist! Cannot update a non-existing setting."

# Delete-setting function that lowers the case of the key that is given to it, checks if the key already exists in the dictionary, and if it does, deletes the key-value pair from the dictionary.

def delete_setting(key, test_settings):
    lower_key = key.lower()

    if lower_key in test_settings:
        del test_settings[lower_key]
        return f"Setting '{lower_key}' deleted successfully!"
    elif lower_key not in test_settings:
        return f"Setting '{lower_key}' not found!"
    
# View-settings function that checks if the dictionary is empty, and if it is not, returns the current settings in the dictionary.

def view_settings(test_settings):
    if not test_settings:
        return "No settings available."
    elif test_settings:
        test_settings_str = "Current User Settings:\n"
        for key, value in test_settings.items():
            test_settings_str += f"{key}: {value}\n"
        return test_settings_str.strip()


print(add_setting("THEME", "LIGHT")) # Should return an error message since the key already exists
print(add_setting("newkey", "newvalue")) # Should add the new key-value pair to the dictionary
print(delete_setting("newkey", test_settings)) # Should delete the key-value pair from the dictionary

print(view_settings(test_settings)) # Should return the current settings in the dictionary

print(update_setting("language", "fr")) # Should update the existing key
print(update_setting("xyz", "value"))   # Should return an error message

print(view_settings(test_settings)) # Should return the current settings in the dictionary after the update



