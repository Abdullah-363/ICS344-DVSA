# FIXED VERSION - After Fix (Lesson #10)
# Fix 1: Wrapped all logic in try/except blocks
# Fix 2: Fixed isAdmin type handling (accepts both boolean and string)
# Fix 3: Returns only generic client-safe error messages
# Fix 4: Full exception details logged to CloudWatch internally

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

    try:
        orderId = event["orderId"]
        userId = event["user"]

        # FIXED: handle both boolean and string isAdmin values safely
        is_admin_raw = event.get("isAdmin", False)
        if isinstance(is_admin_raw, bool):
            is_admin = is_admin_raw
        elif isinstance(is_admin_raw, str):
            is_admin = is_admin_raw.lower() == "true"
        else:
            is_admin = False

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

    except KeyError as e:
        # FIXED: log internally, return generic message to client
        print(f"KeyError in get_order: {e}")
        return {"status": "err", "msg": "invalid request parameters"}

    except Exception as e:
        # FIXED: never expose internal error details to the client
        # Full details are logged to CloudWatch for debugging
        print(f"Unexpected error in get_order: {e}")
        return {"status": "err", "msg": "an internal error occurred"}
