import json
import xml.etree.ElementTree as eTree


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


def file_type(doc):
    """
    Identifies and validates uploaded files before parsing them and compiling refts.json.

    This function will accept an uploaded file from the controller, identify what type of 
    file it is, and pass that file type back to the controller so the file can be parsed 
    correctly. It will also identify and raise errors if the file type is not supported, 
    was not uploaded correctly, or cannot be parsed. It will not prevent errors due to 
    missing or incomplete data within a valid, supported file type. This can lead to the 
    json_dict not being fully filled out, and will be caught by the compile_refts_json 
    function.
    """
    try:
        with open(doc, 'rt') as f:
            tree = eTree.parse(f)
            root = tree.getroot()
            if '{http://www.cuahsi.org/waterML/1.1/}timeSeriesResponse' in root.tag:
                return 'wml_1'
            elif '{http://www.opengis.net/waterml/2.0}Collection' in root.tag:
                return 'wml_2'
            elif '{http://www.opengis.net/timeseriesml/1.0}Collection' in root.tag:
                return 'tsml_1'
            else:
                return 'unknown_xml'
    except eTree.ParseError:
        return "parse_error"
    except IOError:
        return "upload_error"


def parse_wml_1(wml1doc, j):
    """
    Parses a WaterML 1 file and pushes the relevent values into json_dict.

    This function iterates through each node in the wml tree and checks each one against
    the conditions defined below. If a node meets any of these conditions, the appropriate
    data will be appended to the json dictionary, json_dict. The variable pnode defines the 
    previous node in the tree, and is necessary to identify the first and last values for 
    each timeseries with their metadata. The variable wml is a namespace value. Currently, 
    some of these values are not explicitly defined in WaterML 1, so default values have been 
    assigned for now. It is necessary for json_dict to have the same number of elements in 
    each list, but this function does not check this yet.
    """
    with open(wml1doc, 'rt') as f:
        tree = eTree.parse(f)

    pnode = None
    wml = "{http://www.cuahsi.org/waterML/1.1/}"

    for node in tree.iter():
        if pnode is None:
            pnode = node
        if str(node.tag) == wml + "timeSeries":
            j['returnType'].append('WaterML 1.1')
            j['refType'].append('WOF')
            j['serviceType'].append('SOAP')
        if str(node.tag) == wml + "value" and str(pnode.tag) != \
                wml + "value":
            j['beginDate'].append(node.attrib['dateTime'])
        if str(node.tag) != wml + "value" and str(pnode.tag) == \
                wml + "value":
            j['endDate'].append(pnode.attrib['dateTime'])
        if str(node.tag) == wml + "siteName":
            j['site'].append(node.text)
        if str(node.tag) == wml + "latitude":
            j['latitude'].append(node.text)
        if str(node.tag) == wml + "longitude":
            j['longitude'].append(node.text)
        if str(node.tag) == wml + "variableName":
            j['variable'].append(node.text)
        if str(node.tag) == wml + "variableCode":
            j['variableCode'].append(node.text)
        if str(node.tag) == wml + "sourceLink":
            j['url'].append(node.text)
        if str(node.tag) == wml + "siteCode":
            j['siteCode'].append(node.text)
            j['networkName'].append(node.attrib['network'])
        if str(node.tag) == wml + "creationTime":
            j['creationTime'].append(node.text)
        if str(node.tag) == wml + "parameter":
            if str(node.attrib['name']) == "startDate":
                j['beginTime'].append(node.attrib['value'])
        if str(node.tag) == wml + "parameter":
            if str(node.attrib['name']) == "endDate":
                j['endTime'].append(node.attrib['value'])
        pnode = node

    return j


def compile_refts_json(json_dict):
    """
    Accepts json dictionary, returns refts.json file

    This function accepts the json dictionary, j, as an input, and will return a refts.json file
    as outputFile. Currently, the function will encounter an error if the lists in j are not of
    equal length.
    """
    n = 0
    refts_list = []

    for _ in json_dict['returnType']:
        refts = {
            "refType": json_dict['refType'][n],
            "serviceType": json_dict['serviceType'][n],
            "endDate": json_dict['endDate'][n],
            "url": json_dict['url'][n],
            "beginDate": json_dict['beginDate'][n],
            "site": json_dict['site'][n],
            "returnType": json_dict['returnType'][n],
            "location": {
                "latitude": json_dict['latitude'][n],
                "longitude": json_dict['longitude'][n]
            },
            "variable": json_dict['variable'][n],
            "variableCode": json_dict['variableCode'][n],
            "networkName": json_dict['networkName'][n],
            "SiteCode": json_dict['siteCode'][n]
        }
        refts_list.append(refts)
        n += 1

    refts_json = {
        "timeSeriesLayerResource": {
            "fileVersion": 1,
            "title": ", ".join(sorted(set(json_dict['site'])) + sorted(set(json_dict['variable']))),
            "symbol": "http://data.cuahsi.org/content/images/cuahsi_logo_small.png",
            "REFTS": refts_list,
            "keyWords": "Timeseries, CUAHSI",
            "abstract": ", ".join(sorted(set(json_dict['variable']))) +
                        ' data collected from ' +
                        ", ".join(json_dict['beginTime']) +
                        ' to ' +
                        ", ".join(json_dict['endTime']) +
                        ' created on ' +
                        ", ".join(json_dict['creationTime']) +
                        ' from the following site(s): ' +
                        ", ".join(sorted(set(json_dict['site']))) +
                        '. Data created by CUAHSI HydroClient: http://data.cuahsi.org/#.'
        }
    }

    # Save New Data to JSON Template:
    with open('refts.json', 'w') as f:
        outputfile = json.dump(refts_json, f, indent=4)
        return outputfile

myFile = 'test_upload_files/' + 'wml_1_example_2.xml'
compile_json(myFile)
