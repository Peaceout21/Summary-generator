import helper
import name_parser
import generator
import json

import argparse
from pathlib import Path

def process_profile_by_name(name):
    # Process profile by name
    print(f"Processing profile by name: {name}")
    return name_parser.main(name)
    

def process_profile(profile):
    # Process profile object
    print(f"Processing profile by name: {profile}")
    return helper.write_profile(profile)


def main():
    # Create argument parser
    parser = argparse.ArgumentParser(description="Process LinkedIn profile")

    # Add arguments
    parser.add_argument("--name", type=str, help="Profile name")
    parser.add_argument("--profile", type=str, help="Profile object as string")

    # Parse arguments
    args = parser.parse_args()

    # Check which argument is provided
    ai_execute = True
    if args.name:
        to_write_name = args.name
        file_path = process_profile_by_name(args.name)
        if file_path == -1:
            print('No data available for this profile')
            ai_execute = False
            # return 'No data available for this profile'
        
    elif args.profile:
        # ''' check if file already downloaded'''
        file_path,to_write_name = process_profile(args.profile)
        if file_path == -1:
            print('No data available for this profile')
            ai_execute = False
            # return 'No data available for this profile'
            
        # print(file_path)
    else:
        print("Please provide either --name or --profile argument.")
        exit(0)

    ''' use ai here '''
    
    if ai_execute :
        op = generator.main(file_path)
        
        # Create 'output' folder if not present
        output_folder = Path("output")
        output_folder.mkdir(exist_ok=True)
        
        output_file = output_folder / f"Output_{to_write_name}.txt"

        with open(output_file, "w") as f:
            f.write(op)     
        print('completed execution')
if __name__ == "__main__":
    main()



