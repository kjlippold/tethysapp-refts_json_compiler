from utilities import file_type, parse_wml_1, compile_refts_json
import os


def compile_json(file_upload):
    json_dict = {
        'refType': [],
        'serviceType': [],
        'endDate': [],
        'url': [],
        'beginDate': [],
        'site': [],
        'returnType': [],
        'latitude': [],
        'longitude': [],
        'variable': [],
        'variableCode': [],
        'networkName': [],
        'siteCode': [],
        'keyWords': [],
        'creationTime': [],
        'beginTime': [],
        'endTime': []
    }
    if file_type(file_upload) is 'wml_1':
        compile_refts_json(parse_wml_1(file_upload, json_dict))
        print("refts.json was compiled successfully.")
    elif file_type(file_upload) is 'wml_2':
        print("WaterML 2 not currently supported.")
    elif file_type(file_upload) is 'tsml_1':
        print("TimeseriesML not currently supported.")
    elif file_type(file_upload) is 'unknown_xml':
        print("File type not supported.")
    elif file_type(file_upload) is 'parse_error':
        print("Parse Error")
    elif file_type(file_upload) is 'upload_error':
        print("File does not exist.")
    else:
        print("Encountered unknown error.")

"""
myFile = 'test_upload_files/' + 'wml_1_example_1.xml'
compile_json(myFile)
"""