def map_data_values(data: dict, fields_values: dict[str,dict]) -> dict:
    for field in list(fields_values.keys()):
        if field in list(data.keys()):
            data[field] = fields_values[field].get(data[field])
            
    return data