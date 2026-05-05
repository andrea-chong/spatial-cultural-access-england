from typing import Tuple, List
from shapely import Polygon
import requests
import os
from time import sleep
from datetime import datetime
# from google.maps.places_v1.services.places.async_client import PlacesAsyncClient
# from google.maps.places_v1.types import SearchTextRequest
# from google.geo.type.types import Viewport

class PlaceTextSearchClient():

    def __init__(self):
        API_KEY = os.environ['GMAPS_API_KEY']
        self.headers = {
            'Content-Type': 'application/json',
            'X-Goog-Api-Key': API_KEY,
            'X-Goog-FieldMask': 'places.id,nextPageToken',
        }
        self.endpoint = "https://places.googleapis.com/v1/places:searchText"


    def _get_coords_from_polygon(self, polygon:Polygon):
        minx,miny,maxx,maxy = polygon.bounds
        assert(maxx>=minx and maxy>=miny)
        return (miny, minx, maxy, maxx)

    def _process_input_params(self, text_query:str, polygon:Polygon, page_token:str|None=None, included_type:str|None=None):

        # Get Polygon bounds
        coords = self._get_coords_from_polygon(polygon)

        # Add filters
        json_data = {
            'textQuery': text_query,
            "locationRestriction": {
                "rectangle": {
                    "low": {
                        "latitude": coords[0],
                        "longitude": coords[1]
                    },
                    "high": {
                        "latitude": coords[2],
                        "longitude": coords[3]
                    }
                }
            }
        }
        if included_type:
            json_data['includedType'] = included_type
            json_data['strictTypeFiltering'] = True

        # Add pagination
        if page_token:
            json_data['pageToken'] = page_token
        
        return json_data
    
    def request_placeid_only(self, text_query:str, polygon:Polygon, page_token:str|None=None, included_type:str|None=None):

        json_data = self._process_input_params(text_query, polygon, page_token, included_type)
        response = requests.post(self.endpoint, headers=self.headers, json=json_data)

        try:
            response.raise_for_status()
            return response
        
        except Exception as e:
            print(e)
            return json_data
        
    def paginate_requests_placeid_only(self, text_query:str, polygon:Polygon, page_token:str|None=None, included_type:str|None=None):

        self.request_cnt = 0
        self.pids = []

        has_next = True
        
        while has_next:

            if self.request_cnt>=600:
                sleep(60)
                self.request_cnt = 0
            
            response = self.request_placeid_only(text_query, polygon, page_token, included_type)
            self.request_cnt +=1

            page_token = response.json().get("nextPageToken", None)
            self.pids.extend(response.json().get("places", []))
            has_next = isinstance(page_token, str)
            
        return set([p.get("id") for p in self.pids])

class PlaceDetailsClient():

    def __init__(self):
        API_KEY = os.environ['GMAPS_API_KEY']
        self.headers = {
            'Content-Type': 'application/json',
            'X-Goog-Api-Key': API_KEY,
            # 'X-Goog-FieldMask': 'places.id,nextPageToken',
        }
        self.endpoint = "https://places.googleapis.com/v1/places"
        self.results = {}
    
    def new_request_pid(self, pid:str, fieldmask:set=set()):

        req_headers = self.headers.copy()
        req_headers['X-Goog-FieldMask'] = ",".join(fieldmask)
        response = requests.get(f"{self.endpoint}/{pid}", headers=req_headers)

        try:
            response.raise_for_status()
            self.results[pid] = (response, datetime.now())
            return response
        
        except Exception as e:
            print(e)
            return pid
    
    def request_pid(self, pid, fieldmask:set=set(), force_new:bool=False):
        if pid in self.results and not force_new:
            return self.results.get(pid)[0]
        else:
            return self.new_request_pid(pid, fieldmask)
        
class GeocodingClient():

    def __init__(self):
        API_KEY = os.environ['GMAPS_API_KEY']
        self.headers = {
            'Content-Type': 'application/json',
            'X-Goog-Api-Key': API_KEY,
            # 'X-Goog-FieldMask': 'places.id,nextPageToken',
        }
        self.endpoint = "https://geocode.googleapis.com/v4/geocode/places"
        self.results = {}
    
    def new_request_pid(self, pid:str):

        req_headers = self.headers.copy()
        req_headers['place_id'] = pid
        response = requests.get(f"{self.endpoint}/{pid}", headers=req_headers)

        try:
            response.raise_for_status()
            self.results[pid] = (response, datetime.now())
            return response
        
        except Exception as e:
            print(e)
            return pid
    
    def request_pid(self, pid, force_new:bool=False):
        if pid in self.results and not force_new:
            return self.results.get(pid)[0]
        else:
            return self.new_request_pid(pid)