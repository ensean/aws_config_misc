import boto3
import json
from urllib.parse import unquote


tools = [
    {
        "toolSpec": {
            "name": "extract_iso_3166_2_code",
            "description": "Extracts the ISO 3166-2 code from a given text.",
            "inputSchema": {
                "json": {
                "type": "object",
                    "properties": {
                        "iso_code": {"type": "string", "description": "The ISO 3166-2 code of the country's region, with the country code as a prefix, e.g. US-CA for California, USA."},
                    },
                    "required": ["iso_code"]
                }
            }
        }
    }
]



def get_iso_code(event, context):
    text = event['queryStringParameters'].get('text', '')
    text = unquote(text)
    country_code = event['queryStringParameters'].get('country', '')
    prompt = f"""
        Analyze the following address and extract the ISO 3166-2 code for the country's region.
        1. ISO 3166-2 code
    

        Use the extract_iso_3166_2_code tool to provide the extracted information.

        Here's the address: {text}
        """
    br = boto3.client('bedrock-runtime', region_name='us-west-2')
    response = br.converse(
        modelId='anthropic.claude-3-sonnet-20240229-v1:0',
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "text": prompt,
                    }
                ]
            }
        ],
        inferenceConfig={
            "maxTokens": 4096,
        },
        toolConfig={
            "tools": tools,
            # forece use of the tool
            "toolChoice": {
                "tool": {
                    "name": "extract_iso_3166_2_code"
                }
            }
        }
    )

    for content in response['output']['message']['content']:
        if 'toolUse' in content.keys():
            return content['toolUse']['input']
    # no msg extracted
    return None


def lambda_handler(event, context):
    if event['httpMethod'] == 'GET' and event['path'] == '/iso_code':
        return get_iso_code(event, context)
    else:
        raise ValueError('Invalid operation specified')


def main():
    event = {
        'httpMethod': 'GET',
        'path': '/iso_code',
        'queryStringParameters': {
            'text': '223/31 ถนน ร่วมจิตต์, ชะอำ, เพชรบุรี, 76120 ประเทศไทย',
            'country': 'TH'
        }
    }
    context = {}
    print(lambda_handler(event, context))

if __name__ == '__main__':
    main()