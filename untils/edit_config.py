import json




profilefile = 'config.json'


def edit_config(config_id:str,term:str,price:str):
    with open(profilefile, "r", encoding="utf-8") as edit_file:
        json_data = edit_file.read()
        edit_status = json.loads(json_data)
        edit_file.close()
        # print(edit_status)
        for name, values in edit_status.items():
            # print(values['ID'])
            if values['ID'] == config_id:
                values[term] = price
                with open(profilefile, "w", encoding="utf-8") as save_file:
                    save_file.write(json.dumps(edit_status, indent=4, ensure_ascii=False))
                    save_file.close()