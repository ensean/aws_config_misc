import boto3
import json

def search_place_index_for_suggestions(event, context):
    """
    Handles the SearchPlaceIndexForSuggestions API from AWS Location Service.
    """
    location = boto3.client('location')
    index_name = event['queryStringParameters'].get('index_name', '')
    text = event['queryStringParameters'].get('text', '')
    response = {
        "statusCode": 200,
        "statusDescription": "200 OK",
        "isBase64Encoded": False,
        "headers": {
            "Content-Type": "application/json"
        },
    }
    if index_name and text:
        result = location.search_place_index_for_suggestions(
            IndexName=index_name,
            MaxResults=5,
            Text=text
        )
        # extract result from boto3 api call
        body = {
            'Summary': result['Summary'],
            'Results': result['Results']
        }
        response['body'] = json.dumps(body)
    else:
        response['body'] = json.dumps({"msg": "invalid or missing parameters"})
    return response

def get_place(event, context):
    """
    Handles the GetPlace API from AWS Location Service.
    """
    location = boto3.client('location')
    index_name = event['queryStringParameters'].get('index_name', '')
    place_id = event['queryStringParameters'].get('place_id', '')
    response = {
        "statusCode": 200,
        "statusDescription": "200 OK",
        "isBase64Encoded": False,
        "headers": {
            "Content-Type": "application/json"
        },
    }
    if index_name and place_id:
        result = location.get_place(
            IndexName=index_name,
            PlaceId=place_id
        )
        body = {
            'Place': result['Place']
        }
        response['body'] = json.dumps(body)
    else:
        response['body'] = json.dumps({"msg": "invalid or missing parameters"})
    return response

def lambda_handler(event, context):
    if event['httpMethod'] == 'GET' and event['path'] == '/suggestions':
        return search_place_index_for_suggestions(event, context)
    elif event['httpMethod'] == 'GET' and event['path'] == '/place':
        return get_place(event, context)
    else:
        raise ValueError('Invalid operation specified')
