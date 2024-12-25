import boto3
import json


def search_place_index_for_suggestions(event, context):
    """
    Handles the SearchPlaceIndexForSuggestions API from AWS Location Service.
    """
    location = boto3.client('location')
    index_name = event['queryStringParameters'].get('index_name', '')
    max_results = event['queryStringParameters'].get('max_results', 5)
    text = event['queryStringParameters'].get('text', '')
    language = event['queryStringParameters'].get('language', '')
    filter_countries = event['queryStringParameters'].get('filter_countries', '').split(',') if event['queryStringParameters'].get('filter_countries', '') else []
    response = {
        "statusCode": 200,
        "statusDescription": "200 OK",
        "isBase64Encoded": False,
        "headers": {
            "Content-Type": "application/json"
        },
    }
    if index_name and text:
        kwargs = dict(
            IndexName=index_name,
            MaxResults=int(max_results),
            Text=text,
        )
        if len(filter_countries) > 0:
            kwargs['FilterCountries'] = filter_countries
        if language:
            kwargs['Language'] = language
        result = location.search_place_index_for_suggestions(
            **kwargs
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

def suggest_v2(event, context):
    """
    latest api for amazon location service
    """
    geo_client = boto3.client('geo-places')
    text = event['queryStringParameters'].get('text', '')
    language = event['queryStringParameters'].get('language', '')
    max_results = event['queryStringParameters'].get('max_results', 5)
    filter_countries = event['queryStringParameters'].get('filter_countries', '').split(',') if event['queryStringParameters'].get('filter_countries', '') else []
    response = {
        "statusCode": 200,
        "statusDescription": "200 OK",
        "isBase64Encoded": False,
        "headers": {
            "Content-Type": "application/json"
        },
    }
    if text:
        kwargs = dict(
            MaxResults=int(max_results),
            QueryText=text,
        )
        if len(filter_countries) > 0:
            kwargs['Filter']['IncludeCountries'] = [filter_countries]
        if language:
            kwargs['Language'] = language
        result = geo_client.suggest(
            **kwargs
        )
        # extract result from boto3 api call
        body = {
            'Results': result['ResultItems']
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
    language = event['queryStringParameters'].get('language', '')
    response = {
        "statusCode": 200,
        "statusDescription": "200 OK",
        "isBase64Encoded": False,
        "headers": {
            "Content-Type": "application/json"
        },
    }
    if index_name and place_id:
        kwargs = dict(
            IndexName=index_name,
            PlaceId=place_id
        )
        if language:
            kwargs['Language'] = language
        result = location.get_place(
            **kwargs
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
    elif event['httpMethod'] == 'GET' and event['path'] == '/suggest_v2':
        return suggest_v2(event, context)
    else:
        raise ValueError('Invalid operation specified')
