import json
from json2xml import json2xml

input_file = "messa.xml"

output_file = "izlaz.xml"

with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

xml_output = json2xml.Json2xml(data, wrapper="root", pretty=True).to_xml()

with open(output_file, "w", encoding="utf-8") as f:
    f.write(xml_output)

