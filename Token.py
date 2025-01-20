import boto3
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('MiaOrders')

def lambda_handler(event, context):
    try:
        # Parse body dari string JSON ke dictionary
        body = json.loads(event['body'])
        token = body['token']

        # Cek keberadaan token di DynamoDB
        response = table.get_item(Key={'order_id': token})
        if 'Item' in response:
            price = 100  # Harga tetap untuk sekarang
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': f"The price for {response['Item']['movie_name']} is ${price}"
                })
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({
                    'message': "Order not found"
                })
            }
    except KeyError as e:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'error': f"Missing key in request: {str(e)}"
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': f"Internal server error: {str(e)}"
            })
        }
