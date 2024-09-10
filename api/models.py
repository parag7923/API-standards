import datetime
from utils.version import API_VERSION, SERVICE_NAME

def response_template(request_id: str, 
                                  trace_id: str, 
                                  process_duration: int,
                                  isResponseImmediate: bool,
                                  response: dict,
                                  error_code: dict):
    now = datetime.datetime.now()
    now = now.isoformat()
    response_data = {
        "requestId": request_id,
        "traceId": trace_id,
        "apiVersion": API_VERSION,
        "service": SERVICE_NAME,
        "datetime": now,
        "isResponseImmediate": isResponseImmediate,
        "processDuration": process_duration,
        "response" : response,
        "errorCode" : error_code,
    }
    return response_data