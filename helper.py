import json, requests, os


api_key = 'PASTE NEBULA PROXYCURL API KEY HERE'


class JSONProcessor:
    def __init__(self, data):
        self.data = data
    
    def remove_empty_fields(self):
        # Load JSON string as dictionary
        if isinstance(self.data, dict):
            json_dict = self.data
        else:
            json_dict = json.loads(self.data)
        # Remove empty fields
        json_dict = {key: value for key, value in json_dict.items() if value}
        # Convert dictionary back to JSON string
        json_str = json.dumps(json_dict)
        # Load JSON string as dictionary
        json_dict = json.loads(json_str)
        # Update the instance data
        self.data = json_dict
    
    def return_relevant(self):
        # Check if data is already a dictionary
        if isinstance(self.data, dict):
            data = self.data
        else:
            data = json.loads(self.data)
        
        keys_to_remove = ["people_also_viewed", "similarly_named_profiles", 
                          "country_full_name", "follower_count", "public_identifier"]
        for key in keys_to_remove:
            if data.get(key):
                data.pop(key, None)
        
        # Update the instance data
        self.data = data
    
    def relevant_exp(self):
        # Check if data is already a dictionary
        if isinstance(self.data, dict):
            data = self.data
        else:
            data = json.loads(self.data)
        
        if data.get('experiences'):
            for job in data['experiences']:
                job.pop('logo_url', None)
                job.pop('location', None)
                job.pop('company_linkedin_profile_url', None)
        
        # Update the instance data
        self.data = data
    
    def process(self):
        # processed_data = self.data
        self.remove_empty_fields()
        self.return_relevant()
        self.relevant_exp()
        return self.data


def fetch_linkedin_data(url, api_key):
    api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
    
    header_dic = {'Authorization': 'Bearer ' + api_key}
    params = {
        'url': url,
        'fallback_to_cache': 'on-error',
        'use_cache': 'if-present',
        'skills': 'include'
    }
    print(url)
    response = requests.get(api_endpoint, params=params, headers=header_dic)
    print(response.status_code)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Request failed with status code {response.status_code}: {response.text}")






def write_profile(url):
    ''' writes to file and returns file name '''
    # url = 'https://www.linkedin.com/in/jonwray/'
    response = fetch_linkedin_data(url, api_key)
    ''' write raw data '''

    # Save the raw response dictionary to a JSON file
    with open(f"{response['full_name']}_raw.json", "w") as f:
        json.dump(response,f)
    
    processor = JSONProcessor(response)
    
    processed_data = processor.process()

    with open(f"{processed_data['full_name']}_relev.txt", "w") as f:
        f.write(json.dumps(processed_data))
    
    return f"{processed_data['full_name']}_relev.txt" , processed_data['full_name']
    

