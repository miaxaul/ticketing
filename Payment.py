import boto3
import json
import random

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('MiaOrders')  # Ganti sesuai nama tabel Anda

def generate_random_id(length=3):
    """Generate a random numeric ID."""
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])

def lambda_handler(event, context):
    try:
        # Parse body dari string JSON ke dictionary
        body = json.loads(event['body'])
        token = body['token']
        price = body['price']

        # Validasi apakah token ada di DynamoDB
        response = table.get_item(Key={'order_id': token})
        if 'Item' not in response:
            return {
                'statusCode': 404,
                'body': json.dumps({
                    'message': 'Order not found'
                })
            }

        # Generate random ID untuk payment
        payment_id = generate_random_id()

        return {
            'statusCode': 200,
            'body': json.dumps({
                'payment_id': payment_id,
                'message': 'Enjoy the movie!'
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
