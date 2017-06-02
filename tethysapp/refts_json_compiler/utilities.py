import xml.etree.ElementTree as eTree
import tempfile
import json


def convert_files_to_refts(file_list):
    refts_data_list = []
    for f in file_list:
        uploaded_file = tempfile.TemporaryFile()
        uploaded_file.write(f.read())
        uploaded_file.seek(0)
        refts_json_data = compile_refts_data(uploaded_file)
        refts_data_list.append(refts_json_data)
        uploaded_file.close()
        # Add code to create refts files.


def compile_refts_data(file_upload):

    refts_data = {
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
        refts_data = parse_wml_1(file_upload, refts_data)
        refts_json_data = compile_refts_json_files(refts_data)
        return refts_json_data

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

    elif file_type(file_upload) is 'unknown_error':
        print("Encountered an unknown error.")

    else:
        print("Encountered unknown error.")


def file_type(doc):
    doc.seek(0)
    try:
        tree = eTree.parse(doc)
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


def parse_tsml(tsml_file, json_data):
    tsml_file.seek(0)
    return json_data


def parse_wml_2(wml_2_file, json_data):
    wml_2_file.seek(0)
    return json_data


def parse_wml_1(wml_1_file, refts_data):
    wml_1_file.seek(0)

    tree = eTree.parse(wml_1_file)

    previous_node = None
    wml = "{http://www.cuahsi.org/waterML/1.1/}"

    for node in tree.iter():
        if previous_node is None:
            previous_node = node

        if str(node.tag) == wml + "timeSeries":
            refts_data['returnType'].append('WaterML 1.1')
            refts_data['refType'].append('WOF')
            refts_data['serviceType'].append('SOAP')

        if str(node.tag) == wml + "value" and str(previous_node.tag) != \
                wml + "value":
            refts_data['beginDate'].append(node.attrib['dateTime'])

        if str(node.tag) != wml + "value" and str(previous_node.tag) == \
                wml + "value":
            refts_data['endDate'].append(previous_node.attrib['dateTime'])

        if str(node.tag) == wml + "siteName":
            refts_data['site'].append(node.text)

        if str(node.tag) == wml + "latitude":
            refts_data['latitude'].append(node.text)

        if str(node.tag) == wml + "longitude":
            refts_data['longitude'].append(node.text)

        if str(node.tag) == wml + "variableName":
            refts_data['variable'].append(node.text)

        if str(node.tag) == wml + "variableCode":
            refts_data['variableCode'].append(node.text)

        if str(node.tag) == wml + "sourceLink":
            refts_data['url'].append(node.text)

        if str(node.tag) == wml + "siteCode":
            refts_data['siteCode'].append(node.text)
            refts_data['networkName'].append(node.attrib['network'])

        if str(node.tag) == wml + "creationTime":
            refts_data['creationTime'].append(node.text)

        if str(node.tag) == wml + "parameter":
            if str(node.attrib['name']) == "startDate":
                refts_data['beginTime'].append(node.attrib['value'])

        if str(node.tag) == wml + "parameter":
            if str(node.attrib['name']) == "endDate":
                refts_data['endTime'].append(node.attrib['value'])

        previous_node = node

    return refts_data


def compile_refts_json_files(refts_data):
    n = 0
    refts_list = []

    for _ in refts_data['returnType']:
        refts = {
            "refType": refts_data['refType'][n],
            "serviceType": refts_data['serviceType'][n],
            "endDate": refts_data['endDate'][n],
            "url": refts_data['url'][n],
            "beginDate": refts_data['beginDate'][n],
            "site": refts_data['site'][n],
            "returnType": refts_data['returnType'][n],
            "location": {
                "latitude": refts_data['latitude'][n],
                "longitude": refts_data['longitude'][n]
            },
            "variable": refts_data['variable'][n],
            "variableCode": refts_data['variableCode'][n],
            "networkName": refts_data['networkName'][n],
            "SiteCode": refts_data['siteCode'][n]
        }
        refts_list.append(refts)
        n += 1

    compiled_json_data = {
        "timeSeriesLayerResource": {
            "fileVersion": 1,
            "title": ", ".join(sorted(set(refts_data['site'])) + sorted(set(refts_data['variable']))),
            "symbol": "http://data.cuahsi.org/content/images/cuahsi_logo_small.png",
            "REFTS": refts_list,
            "keyWords": "Timeseries, CUAHSI",
            "abstract": ", ".join(sorted(set(refts_data['variable']))) +
                        ' data collected from ' +
                        ", ".join(refts_data['beginTime']) +
                        ' to ' +
                        ", ".join(refts_data['endTime']) +
                        ' created on ' +
                        ", ".join(refts_data['creationTime']) +
                        ' from the following site(s): ' +
                        ", ".join(sorted(set(refts_data['site']))) +
                        '. Data created by CUAHSI HydroClient: http://data.cuahsi.org/#.'
        }
    }
    refts_file = tempfile.TemporaryFile()
    refts_file.write(json.dumps(compiled_json_data))
    refts_file.seek(0)
    print(":::REFTS CONTENT:::")
    print(refts_file.read())
    print(":::END CONTENT:::")
    return refts_file
