"""IBM Cloud Function that gets all reviews for a dealership
Returns:
    List: List of reviews for the given dealership
"""
import sys 
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def get_review(dict): 
    authenticator = IAMAuthenticator("vwihyHQ5ekJRB02JUarrC1c8H8CSYDHax-5s9Ymta-mE")
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url("https://apikey-v2-k1xhitwcmkebvzelp7z21l1x7zsnewn5cykl50ilk8t:56bf52d0826be71246039afa3a46eb19@542d5355-caae-474a-9aba-7ee4a461f0b5-bluemix.cloudantnosqldb.appdomain.cloud")
    response = service.post_find(
                db='reviews',
                selector={'dealership': {'$eq': int(dict['id'])}},
            ).get_result()
    try: 
        # result_by_filter=my_database.get_query_result(selector,raw_result=True) 
        result= {
            'headers': {'Content-Type':'application/json'}, 
            'body': {'data':response} 
            }        
        return result
    except:  
        return { 
            'statusCode': 404, 
            'message': 'Something went wrong'
            }
"""Posts a new review into an existing database"""
def post_review(dict):
    authenticator = IAMAuthenticator("vwihyHQ5ekJRB02JUarrC1c8H8CSYDHax-5s9Ymta-mE")
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url("https://apikey-v2-k1xhitwcmkebvzelp7z21l1x7zsnewn5cykl50ilk8t:56bf52d0826be71246039afa3a46eb19@542d5355-caae-474a-9aba-7ee4a461f0b5-bluemix.cloudantnosqldb.appdomain.cloud")
    response = service.post_document(db='reviews', document=dict["review"]).get_result()
    try:
    # result_by_filter=my_database.get_query_result(selector,raw_result=True)
        result= {
        'headers': {'Content-Type':'application/json'},
        'body': {'data':response}
        }
        return result
    except:
        return {
        'statusCode': 404,
        'message': 'Something went wrong'
        }