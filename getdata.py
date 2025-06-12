#!/usr/bin/env python
# coding: utf-8
import argparse
import requests
import base64
import json
import yaml

if __name__ == "__main__":

    #Argument acquisition
    parser = argparse.ArgumentParser(usage='Get Meta Data', add_help=True)
    parser.add_argument('-n', '--no_verify', help='no SSL verification', action='store_false')
    args = parser.parse_args()
    settings_file_path = './console_access_settings.yaml'

    with open(settings_file_path, "r", encoding="utf-8") as file:
        yaml_data = yaml.safe_load(file)

    console_endpoint = yaml_data["console_access_settings"]["console_endpoint"]
    portal_authorization_endpoint = yaml_data["console_access_settings"]["portal_authorization_endpoint"]
    client_secret = yaml_data["console_access_settings"]["client_secret"]
    client_id = yaml_data["console_access_settings"]["client_id"]

    #Set device_id
    device_id = "Aid-80070001-0000-2000-9002-000000000b42"

    #client_id:client_secret base64 encoded
    authorization = base64.b64encode((client_id + ':' + client_secret).encode()).decode()

    #Obtain token
    headers  = {'accept': 'application/json',
                'authorization': 'Basic {}'.format(str(authorization)),
                'cache-control': 'no-cache',
                'content-type': 'application/x-www-form-urlencoded'
                }
    data = 'grant_type=client_credentials&scope=system'

    response = requests.post(portal_authorization_endpoint, headers=headers, data=data)
    json_data = response.json()
    access_token    = str(json_data['access_token'])

    #Obtaining and saving inference results
    # console_endpoint = get_param(param_file,'console_endpoint')
    headers  = {'Authorization': 'Bearer {}'.format(access_token)}

    get_inference_result = console_endpoint + '/inferenceresults/devices/' + device_id + '?limit=1&scope=full'

    response = requests.get(get_inference_result, headers=headers)
    json_data = response.json()

    output_file = open('ObjectDetection_encoded.json','w')
    json.dump(json_data["data"][0]["inference_result"],output_file,indent=4)