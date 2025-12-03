import xmltodict,json,re

def rmv_whitespace(obj):
    if isinstance(obj,dict):
        return {k:rmv_whitespace(v) for k,v in obj.items()
                }
    elif isinstance(obj,list):
        return [rmv_whitespace(i) for i in obj]
    elif isinstance(obj,str):
        cisto=obj.replace("\n"," ")
        cisto= re.sub(r"\s{2,}", " ", cisto)
        return cisto.strip()
    return obj

def coerce_number(obj):
    if isinstance(obj, dict):
        new_obj = {}
        for k, v in obj.items():
            if k == "OrderQuantity" and isinstance(v, str):
                if re.fullmatch(r"[+-]?\d+", v):
                    try:
                        new_obj[k] = int(v)
                        continue
                    except ValueError:
                        pass
                if re.fullmatch(r"[+-]?\d+[.,]\d+", v):
                    try:
                        new_obj[k] = float(v.replace(",", "."))
                        continue
                    except ValueError:
                        pass
            new_obj[k] = coerce_number(v)
        return new_obj
    elif isinstance(obj, list):
        return [coerce_number(i) for i in obj]
    else:
        return obj

def xml_to_json(input_path, output_path=None):
    with open(input_path, "r", encoding="utf-8") as f:
        xml_content = f.read()

    data_dict = xmltodict.parse(xml_content)

    data_dict = coerce_number(data_dict)

    data_dict = rmv_whitespace(data_dict)

    json_data = json.dumps(data_dict, indent=2)

    if output_path:
        with open(output_path, "w", encoding="utf-8") as out:
            out.write(json_data)

    return json_data

if __name__ == "__main__":
    input_file = "Oktal-farma.xml"
    output_file = "Oktal-farma.json"

    json_result = xml_to_json(input_file, output_file)

    print("Converted JSON : ")
    print(json_result)
   # orders = load_orders_from_json(output_file)