import boto3
import json
import random
import string

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('MiaOrders')  # Ganti sesuai nama tabel Anda

def generate_random_token(length=8):
    """Generate a random alphanumeric token."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))

def lambda_handler(event, context):
    try:
        # Parse body dari string JSON ke dictionary
        body = json.loads(event['body'])
        movie_name = body['movie_name']
        user_id = body['user_id']  # Ambil user_id dari body request
        ticket_quantity = body.get('ticket_quantity', 1)  # Default ke 1 jika tidak disediakan

        # Validasi jumlah tiket
        if not isinstance(ticket_quantity, int) or ticket_quantity <= 0:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': "Invalid 'ticket_quantity'. It must be a positive integer."
                })
            }

        # Generate token
        token = generate_random_token()

        # Masukkan data ke DynamoDB
        table.put_item(
            Item={
                'order_id': token,
                'user_id': user_id,
                'movie_name': movie_name,
                'ticket_quantity': ticket_quantity  # Tambahkan jumlah tiket
            }
        )

        return {
            'statusCode': 201,
            'body': json.dumps({
                'message': 'Order created successfully',
                'user_id': user_id,
                'movie_name': movie_name,
                'ticket_quantity': ticket_quantity,
                'token': token
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
