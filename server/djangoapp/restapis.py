import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    
    # If argument contain API KEY
    api_key = kwargs.get("api_key")
    print("GET from {} ".format(url))
    try:
        if api_key:
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', api_key))
        else:
            # Call get method of requests library with URL and parameters
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")

    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data
    
# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, dealer_id, **kwargs):
    try:
        params = {}
        if dealer_id is not None:
            params['dealer_id'] = dealer_id

        response = requests.post(url, json=json_payload, params=params, **kwargs)
        return response
    except requests.exceptions.RequestException as e:
        raise Exception(f'Error making POST request: {e}')

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    state = kwargs.get("state")
    if state:
        json_result = get_request(url, state=state)
    else:
        json_result = get_request(url)
    print('json_result RESTAPIS', json_result) 

    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   dealer_id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    id = kwargs.get("dealer_id")
    if id:
        json_result = get_request(url, id=id)
    else:
        json_result = get_request(url)
    print(json_result)
    if json_result:
        for review_data in json_result:
            # Check if all required fields exist in review_data
            if "id" in review_data and "dealership" in review_data and "review" in review_data \
                    and "purchase" in review_data and "purchase_date" in review_data \
                    and "car_make" in review_data and "car_model" in review_data and "car_year" in review_data:
                # If all fields are available, create the DealerReview object
                dealer_review = DealerReview(
                    review_id=review_data["id"],
                    dealer_id=review_data["dealership"],
                    review=review_data["review"],
                    purchase=review_data["purchase"],
                    purchase_date=review_data["purchase_date"],
                    car_make=review_data["car_make"],
                    car_model=review_data["car_model"],
                    car_year=review_data["car_year"],
                    sentiment=None
                )
                results.append(dealer_review)

    return results

def get_dealer_by_id(url, dealer_id):
    json_result = get_request(url, dealer_id=dealer_id)
    print('json_result RESTAPIS',json_result)

    if json_result:
        dealers = json_result
        
    
        dealer_doc = dealers[0]
        dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"],
                                dealer_id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"], full_name=dealer_doc["full_name"],
                                
                                st=dealer_doc["st"], zip=dealer_doc["zip"], short_name=dealer_doc["short_name"])
    return dealer_obj
    
def get_dealers_by_state(state):
    # Call get_request with the base URL for dealerships and state parameter
    url = "https://michischaetz-3000.theiadocker-3-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
    json_result = get_request(url, state=state)

    results = []
    if json_result and "docs" in json_result:
        dealers = json_result["docs"]
        for dealer in dealers:
            # Create a CarDealer object with values in `dealer` dictionary
            dealer_obj = CarDealer(
                address=dealer.get("address", ""),
                city=dealer.get("city", ""),
                full_name=dealer.get("full_name", ""),
                dealer_id=dealer.get("id", ""),
                lat=dealer.get("lat", ""),
                long=dealer.get("long", ""),
                short_name=dealer.get("short_name", ""),
                st=dealer.get("st", ""),
                zip=dealer.get("zip", "")
            )
            results.append(dealer_obj)

    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(dealerreview):
    # Define the URL for sentiment analysis
    url = 'https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/e5b1b5b2-71df-425f-9427-f2e466ac8a35'

    # Debugging: Print the review text
    print("Review Text:", dealerreview.review)
    # Construct the parameters from the dealerreview object
    params = {
        "text": dealerreview.review,
        "version": "2022-04-07",
        "features": "sentiment",
        "return_analyzed_text": True
    }

    # Your API key for Watson NLU
    api_key = 'AzkX9wDCuhaRi19BXNyLhhAolICTQU7nAcl666D1isJG'

    try:
        # Make the GET request to Watson NLU
        response = get_request(url, api_key=api_key, **params)
        
        print("API Response:", response)  # Print the response for debugging

        # Check if the response is successful
        if "sentiment" in response:
            sentiment = response["sentiment"]["document"]["label"]
            print("Sentiment:", sentiment)  # Print the extracted sentiment for debugging
            return sentiment
        else:
            return None
    except Exception as e:
        # Handle any exceptions here
        print("Error analyzing sentiment:", str(e))
        return None



