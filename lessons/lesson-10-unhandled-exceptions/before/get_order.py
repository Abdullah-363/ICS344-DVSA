# VULNERABLE VERSION - Before Fix (Lesson #10)
# Vulnerability: No exception handling — unhandled exceptions return full
# stack traces, internal file paths, and source code to the client

import json
import boto3
import os
import decimal
from boto3.dynamodb.conditions import Key, Attr


def lambda_handler(event, context):
    print(json.dumps(event))

    class DecimalEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, decimal.Decimal):
                if o % 1 > 0:
                    return float(o)
                else:
                    return int(o)
            return super(DecimalEncoder, self).default(o)

    orderId = event["orderId"]
    userId = event["user"]

    # VULNERABLE: .lower() called on isAdmin which may be boolean, not string
    # Causes AttributeError: 'bool' object has no attribute 'lower'
    # This exception propagates back to the client with full stack trace
    is_admin = json.loads(event.get("isAdmin", "false").lower())

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ["ORDERS_TABLE"])

    if is_admin:
        response = table.query(
            KeyConditionExpression=Key('orderId').eq(orderId)
        ).get("Items", [None])
    else:
        key = {"orderId": orderId, "userId": userId}
        response = [table.get_item(Key=key).get("Item")]

    res = {"status": "ok", "order": response[0]} if response[0] is not None else {"status": "err", "msg": "could not find order"}

    return json.loads(json.dumps(res, cls=DecimalEncoder).replace("\\\"", "\"").replace("\\n", ""))
