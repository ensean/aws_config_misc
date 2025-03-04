import boto3
import json
from urllib.parse import unquote


BIAS_POS_DICT = {
    'JPN': [139.7774201, 35.736716],
    'USA': [-77.0368707, 38.9071923],
    'GBR': [-0.1276474, 51.5073219],
    'AUS': [151.2164539, -33.8548157],
    'THA': [100.523186, 13.736717],
    'FRA': [2.3522219, 48.856614],
    'TWN': [121.5654177, 25.0329694],
    'HKG': [114.1628131, 22.2793278],
    'SGP': [103.819836, 1.352083],
    'IDN': [106.8650395, -6.1753942],
    "MYS": [101.686855, 3.139003],
    "VNM": [105.854444, 21.028511],
    "PHL": [121.774017, 12.879721],
    "CHN": [116.4073963, 39.9041999],
    "SVK": [17.107747, 48.148598],
}

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
    text = unquote(text)

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
            BiasPosition=BIAS_POS_DICT.get(filter_countries[0]),
            AdditionalFeatures=['Core']
        )
        if len(filter_countries) > 0:
            kwargs['Filter'] = {'IncludeCountries': filter_countries}
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


def get_place_v2(event, context):
    """
    latest api for amazon location service
    """
    geo_client = boto3.client('geo-places')
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
    if place_id:
        kwargs = dict(
            PlaceId=place_id
        )
        if language:
            kwargs['Language'] = language
        result = geo_client.get_place(
            **kwargs
        )
        body = {
            'Place': result
        }
        response['body'] = json.dumps(body)
    else:
        response['body'] = json.dumps({"msg": "invalid or missing parameters"})
    return response

def geocode(event, context):
    """
    latest api for amazon location service
    """
    geo_client = boto3.client('geo-places')
    text = event['queryStringParameters'].get('text', '')
    text = unquote(text)    # url decode
    country = event['queryStringParameters'].get('country', '')
    response = {
        "statusCode": 200,
        "statusDescription": "200 OK",
        "isBase64Encoded": False,
        "headers": {
            "Content-Type": "application/json"
        },
    }
    kwargs = dict(
        QueryText=text,
        Filter = {'IncludeCountries': [country]}
    )
    result = geo_client.geocode(
        **kwargs
    )
    response['body'] = json.dumps(result)
    
    return response

def lambda_handler(event, context):
    if event['httpMethod'] == 'GET' and event['path'] == '/suggestions':
        return search_place_index_for_suggestions(event, context)
    elif event['httpMethod'] == 'GET' and event['path'] == '/place':
        return get_place(event, context)
    elif event['httpMethod'] == 'GET' and event['path'] == '/suggest_v2':
        return suggest_v2(event, context)
    elif event['httpMethod'] == 'GET' and event['path'] == '/get_place_v2':
        return get_place_v2(event, context)
    elif event['httpMethod'] == 'GET' and event['path'] == '/geocode':
        return geocode(event, context)
    else:
        raise ValueError('Invalid operation specified')
