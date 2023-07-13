
import json
import helper
import re

def extract_related_summaries(profiles):
    keywords = ['founder', 'co-founder', 'AI scientist', 'data science', 'machine learning']
    related_profiles = []
    # print('profiles = ')
    # print(profiles)
    if not profiles.get('similarly_named_profiles'):
        return []
    profiles_op = profiles['similarly_named_profiles']
    for profile in profiles_op:
        summary = profile.get('summary', '')
        if summary is None:
            summary = ''
        for keyword in keywords:
            pattern = r"\b" + re.escape(keyword) + r"\b"
            if re.search(pattern, summary, flags=re.IGNORECASE):
                related_profiles.append(profile)
                break
    
    return related_profiles


# def check_relevant_profile(profile):
def check_relevant_profile(profile):
    related_summaries = []
    experiences = profile.get('experiences', [])
    keywords = ['founder', 'co-founder', 'AI scientist', 'data science', 'machine learning',
                'artificial intelligence']

    for experience in experiences:
        title = experience.get('title', '')
        description = experience.get('description', '')
        if title is None:
            title = ''

        if description is None:
            description = ''

        # Check if title or description contains any of the keywords
        if any(re.search(keyword, title, re.IGNORECASE) or re.search(keyword, description, re.IGNORECASE) for keyword in keywords):
            related_summaries.append({
                'company': experience.get('company', ''),
                'title': title,
                'description': description
            })

    return related_summaries

# construct a linkding profile 

def construct_name(name):
    urls = []

    # Remove spaces and construct URL with removed spaces
    name_without_spaces = name.replace(" ", "")
    linkedin_url_1 = "https://www.linkedin.com/in/" + name_without_spaces + "/"
    urls.append(linkedin_url_1)

    # Replace spaces with "-" and construct URL with replaced spaces
    name_with_dashes = name.replace(" ", "-")
    linkedin_url_2 = "https://www.linkedin.com/in/" + name_with_dashes + "/"
    urls.append(linkedin_url_2)

    # Replace spaces with "-" and change case to lowercase
    lowercase_name = name.replace(" ", "").lower()
    linkedin_url_3 = "https://www.linkedin.com/in/" + lowercase_name + "/"
    urls.append(linkedin_url_3)

    # Replace spaces with "-" and change case to proper case
    propercase_name = name.replace(" ", "-").title()
    linkedin_url_4 = "https://www.linkedin.com/in/" + propercase_name + "/"
    urls.append(linkedin_url_4)

    return urls


def main(name):

    linkedin_urls = construct_name(name)
    error_counter = 0
    for linkedin_url in linkedin_urls:
        try:
            file_name, person_name = helper.write_profile(linkedin_url)
            # break here as we found a valid profile
            break
            
        except Exception as e:
            print(f"Error occurred for LinkedIn URL: {linkedin_url}")
            error_counter += 1
            continue
    if error_counter ==4:
        print("'No data available for this profile'")
        return -1
    
    ''' call helper'''
    
    file_name , person_name = helper.write_profile(linkedin_url)


    with open(file_name, 'r') as f:
        data = json.load(f)
    
    if len (check_relevant_profile(data)) ==0:
        ''' current profile is not ok '''
        # check for other releveant profiles
        related_profiles = extract_related_summaries(data)
        # this is related profiles with same name but with ai ml etc , if 0 then no data found
        if len(related_profiles) ==0:
            'No data available for this profile'
            return -1
        else:
            profile = related_profiles[0]
            if not profile.get('link'):
                'No data available for this profile'
                return -1
            
            link = profile.get('link')
            
            ''' proceed to perform helper function '''
            file_name, person_name = helper.write_profile(link)

            return file_name
    else:
        ''' current profile is ok'''
        print('original is ok')
        return file_name


