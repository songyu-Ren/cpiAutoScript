import json
import re

def clean_keys(obj, parent_key=''):
    """
    Recursively goes through the object and removes the braces and URLs from the keys.
    Also appends a unique number to each 'properties' key.
    """
    if isinstance(obj, dict):
        new_obj = {}
        for k, v in obj.items():
            # Use regular expression to remove the URL part within braces from the key
            new_key = re.sub(r'\{.*?\}', '', k)

            # Check if the new_key is 'properties', and append a unique number if it is
            if new_key == 'properties':
                new_key += str(clean_keys.counter)
                clean_keys.counter += 1

            new_obj[new_key] = clean_keys(v, new_key)  # Recurse for nested dictionaries
        return new_obj
    elif isinstance(obj, list):
        return [clean_keys(item, parent_key) for item in obj]  # Recurse for each item in the list
    else:
        return obj  # Return the item itself if it's not a dict or list

# Initialize a counter as an attribute of the clean_keys function
clean_keys.counter = 1

# Path to the JSON file you want to load and clean
file_path = './IntegrationPackage.json'

# Load the JSON data from the file
with open(file_path, 'r') as file:
    data = json.load(file)

# Clean the keys
cleaned_data = clean_keys(data)

# Path for the output file
output_file_path = 'CleanedIntegrationPackage.json'

# Save the cleaned data back to a new JSON file
with open(output_file_path, 'w') as file:
    json.dump(cleaned_data, file, indent=4)

print(f"Cleaned JSON data has been saved to {output_file_path}.")
