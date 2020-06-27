import boto3
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('tweets')

table.put_item(
   Item={
        'id': 'janedoe',
        'first_name': 'Jane',
        'last_name': 'Doe',
        'age': 25,
        'account_type': 'standard_user',
    }
)
