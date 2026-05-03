# FIXED VERSION - After Fix (Lesson #5)
# Fix: Added invoker validation to ensure only DVSA-ORDER-BILLING
# can invoke this function, preventing direct unauthorized access

import json
import boto3
import os
import uuid
import time
import base64
import decimal
import jsonpickle

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ["ORDERS_TABLE"])

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


def addItem(user, obj, ts):
    id = str(uuid.uuid4())
    response = table.put_item(
        Item={
            'orderId': id,
            'userId': obj['userId'],
            'orderStatus': obj['status'],
            'itemList': obj['itemList'],
            'address': obj['address'],
            'confirmationToken': obj['token'],
            'paymentTS': ts,
            'totalAmount': obj['total']
        }
    )
    return {"status": "ok", "msg": id}


def deleteItem(orderId, user):
    key = {"orderId": orderId}
    response = table.delete_item(Key=key)
    return {"status": "ok", "msg": "order deleted"}


def updateItem(orderId, user, obj, ts):
    update_expr = 'SET itemList = :itemList, orderStatus = :orderStatus, address = :address, confirmationToken = :token, paymentTS = :ts, totalAmount = :total'
    response = table.update_item(
        Key={"orderId": orderId, "userId": user},
        UpdateExpression=update_expr,
        ExpressionAttributeValues={
            ':itemList': obj['itemList'],
            ':orderStatus': obj['status'],
            ':address': obj['address'],
            ':token': obj['token'],
            ':ts': obj['ts'],
            ':total': obj['total']
        }
    )
    return {"status": "ok", "msg": "order updated"}


def lambda_handler(event, context):
    # FIXED: Only allow invocation from the billing workflow
    # Direct invocations from any other source are rejected
    invoker = event.get("invoker", "")
    if invoker != "DVSA-ORDER-BILLING":
        return {"status": "err", "msg": "Unauthorized - must be invoked through billing workflow"}

    if "authorization" in event["headers"]:
        auth_header = event["headers"]["authorization"]
    elif "Authorization" in event["headers"]:
        auth_header = event["headers"]["Authorization"]
    else:
        return {"status": "err", "msg": "Missing authorization header"}

    token_sections = auth_header.split('.')
    try:
        padding = 4 - len(token_sections[1]) % 4
        auth_data = base64.b64decode(token_sections[1] + "=" * padding)
    except Exception:
        return {"status": "err", "msg": "Invalid authorization header"}

    token = json.loads(auth_data)
    user = token["username"]

    action = event['body']['action']
    orderId = event['body']['order-id']
    item = event['body']['item']
    ts = int(time.time())

    if action == "add":
        res = addItem(user, item, ts)
    elif action == "delete":
        res = deleteItem(orderId, user)
    elif action == "update":
        res = updateItem(orderId, user, item, ts)
    else:
        res = {"status": "err", "msg": "unknown command"}

    return res
