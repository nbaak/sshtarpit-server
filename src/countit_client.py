import os
import requests
from typing import Union


def read_token(token_file):
    if os.path.exists(token_file):
        with open(token_file, 'r') as f:
            return f.read()
    return None


def dict_builder(in_dict=None, *args, **kwargs):
    parse_dict:dict = in_dict or kwargs
    new_dict = {}
    for label, value in parse_dict.items():
        if value != None: new_dict[label] = value 
        
    return new_dict


def build_headers(token:str):
    headers = {
        "Authorization": f"{token}",
        "Content-Type": "application/json"
    }
    return headers


class CountItClient():
    
    def __init__(self, server:str, port:int, *args, token:str=None, token_file:str=None):
        self.server = server
        self.port = port
        if token: 
            self.token = token
        elif token == None and token_file:
            self.token = read_token(token_file)
        else:
            self.token = ""
        
    def __get(self, endpoint):
        try:
            headers = build_headers(self.token)
            response = requests.get(f"{self.server}:{self.port}/{endpoint}", headers=headers)
            return response
        except Exception as e:
            print("Server not available")
            return None
    
    def __post(self, endpoint, data:dict=None):
        try:
            headers = build_headers(self.token)
            if data:
                response = requests.post(f"{self.server}:{self.port}/{endpoint}", json=data, headers=headers)
            else:
                response = requests.post(f"{self.server}:{self.port}/{endpoint}", json={}, headers=headers)
            return response        
        except Exception as e:
            print("Server not available")
            return None
        
    def test_connection(self) -> bool:
        response = self.__get(f"/test")
        if response and response.status_code == 200:
            return True        
        return False
        
    def add_metric(self, metric_name) -> str:
        data = dict_builder()
        response = self.__post(f"/new/{metric_name}", data)
        
        if response and response.status_code == 201:
            return response.json()["success"]
        
        return ""
    
    def inc(self, metric_name:str, *args, label=None, value=None) -> Union[None, int]:
        """
        increases the metric label by value
        """
        data = dict_builder(label=label, value=value)
             
        response = self.__post(f"/inc/{metric_name}", data)
        
        if response and response.status_code == 202:
            value = response.json()["success"]
            if isinstance(value, (int, float)):
                return value
        
        return None
    
    def update(self, metric_name:str, *args, label=None, value=None) -> bool:
        """
        updates the metric label by value
        same as inc
        """
        return self.inc(metric_name, label=label, value=value)
    
    def labels(self, metric_name:str) -> list:
        """
        get labels of metric
        """
        response = self.__get(f"/labels/{metric_name}")
        
        if response and response.status_code == 201:
            return response.json()["success"]
        
        return []
    
    def get(self, metric_name:str, *args, label=None) -> Union[int, float, None]:
        """
        get labels of metric
        """
        data = dict_builder(label=label)
            
        response = self.__post(f"/get/{metric_name}", data)
        
        if response and response.status_code == 201:
            return response.json()["success"]
        
        return None
    
    def metrics(self) -> list:
        """
        get metrics from service
        """
        response = self.__get(f"/metrics")
        
        if response and response.status_code == 200:
            return response.json()["success"]
        
        return []
    
    def delete(self, metric_name) -> str:
        data = dict_builder()
        response = self.__post(f"/delete/{metric_name}", data)
        
        if response and response.status_code == 201:
            return response.json()["success"]
        
        return ""
    
    def __str__(self):
        return f"CountIt: {self.server}:{self.port}"
    
    def __repr__(self):
        return self.__str__()
    
    
def test():
    # test dict builder
    d1 = dict_builder(a="a", B=1, c=None, d="123")
    print(d1)
    d2 = dict_builder(d1)
    print(d2)
    d3 = dict_builder({"a": None, "b": "C", (12, 32): (12, 34, 56)})
    print(d3)


if __name__ == "__main__":
    test()
        
