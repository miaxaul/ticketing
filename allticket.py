import boto3
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('MiaOrders')  # Ganti sesuai dengan nama tabel Anda

def lambda_handler(event, context):
    try:
        # Periksa apakah 'queryStringParameters' ada
        if 'queryStringParameters' not in event or event['queryStringParameters'] is None:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': "Missing query parameters"
                })
            }

        # Ambil user_id dari query string
        user_id = event['queryStringParameters'].get('user_id')
        if not user_id:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': "Missing 'user_id' in query parameters"
                })
            }

        # Query DynamoDB untuk pesanan berdasarkan user_id
        response = table.scan(
            FilterExpression="user_id = :uid",
            ExpressionAttributeValues={":uid": user_id}
        )

        # Ambil data pesanan
        items = response.get('Items', [])

        # Jika tidak ada pesanan, kirimkan respons kosong
        if not items:
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'user_id': user_id,
                    'orders': []
                })
            }

        # Jika ada pesanan, kirimkan informasi pesanan
        orders = []
        for item in items:
            orders.append({
                'user_id': item['user_id'],
                'movie_name': item['movie_name'],
                'order_quantity': item.get('order_quantity', 1)  # Default ke 1 jika tidak ada
            })

        return {
            'statusCode': 200,
            'body': json.dumps({
                'user_id': user_id,
                'orders': orders
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': f"Internal server error: {str(e)}"
            })
        }
