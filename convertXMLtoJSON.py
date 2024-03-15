import xml.etree.ElementTree as ET
import json

def xml_to_json(xml_file, json_file):
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    # Convert the XML tree to a dictionary
    def elem_to_dict(elem):
        d = {elem.tag: {} if elem.attrib else None}
        children = list(elem)
        if children:
            dd = {}
            for dc in map(elem_to_dict, children):
                for k, v in dc.items():
                    if k in dd:
                        if not isinstance(dd[k], list):
                            dd[k] = [dd[k]]
                        dd[k].append(v)
                    else:
                        dd[k] = v
            d = {elem.tag: dd}
        if elem.attrib:
            d[elem.tag].update(("@" + k, v) for k, v in elem.attrib.items())
        if elem.text:
            text = elem.text.strip()
            if children or elem.attrib:
                if text:
                  d[elem.tag]['#text'] = text
            else:
                d[elem.tag] = text
        return d

    xml_dict = elem_to_dict(root)
    
    # Convert the dictionary to a JSON string
    json_str = json.dumps(xml_dict, indent=4)
    
    # Write the JSON string to a file
    with open(json_file, "w") as json_f:
        json_f.write(json_str)

# Example usage
xml_file = 'IntegrationRuntimeArtifacts.xml'
json_file = 'IntegrationRuntimeArtifacts.json'
xml_to_json(xml_file, json_file)

print(f"XML file '{xml_file}' has been converted to JSON file '{json_file}'.")
