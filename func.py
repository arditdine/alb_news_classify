import io
import json
import logging
from news_classify import NewsClassify

from fdk import response

model = NewsClassify(train=False)

def handler(ctx, data: io.BytesIO=None):    
    try:
        body = json.loads(data.getvalue())
        articleTxt = body.get("article")
    except (Exception, ValueError) as ex:
        logging.getLogger().info('error parsing json payload: ' + str(ex))

    prediction = model.classify(articleTxt)
    return response.Response(
        ctx, response_data=json.dumps(
            {"result": str(prediction)}),
        headers={"Content-Type": "application/json"}
    )
