#!/usr/bin/env python3
import argparse, hashlib, inspect, json, requests, time
from bs4 import BeautifulSoup

# Make GET Request to the endpoint to get the string.
def urlGET(baseurl,debug):
    debugMode(debug)
    global response 
    global session_id
    response = requests.get(baseurl)
    session_id = response.cookies.get("PHPSESSID")
    print("Session ID: ", session_id)

# Parse the HTML page with BeautifulSoup and extract the string to be hashed.
def soupParse(debug):
    debugMode(debug)
    soup = BeautifulSoup(response.text, 'html.parser')
    global string_to_hash
    string_to_hash = soup.find('h3').text
    print("String to hash: ", string_to_hash)

# Complete the MD5 hash of the string.
def hashString(debug):
    debugMode(debug)
    hash_object = hashlib.md5(string_to_hash.encode())
    global md5_hash
    md5_hash = hash_object.hexdigest()
    print("MD5 Hash: ", md5_hash)

# Submit hash to the endpoint.
def postHash(baseurl,debug):
    debugMode(debug)
    data = {'hash': md5_hash}
    headers = {
        "Cookie": f"PHPSESSID={session_id}"
    }
    global response
    response = requests.post(baseurl, headers=headers, data=data)

def responsePrint(debug):
    debugMode(debug)
    time.sleep(1)
    soup = BeautifulSoup(response.text, 'html.parser')
    flag = soup.find('p').text.strip()
    print("Flag: ", flag, "\n") 
    

# debug
def debugMode(debug):
    if debug:
        # Debug Break point
        frame = inspect.currentframe().f_back
        function_name = frame.f_code.co_name
        print(f"\nDebug: called from {function_name}")
        input("Press Enter to continue: ")

def main(baseurl,delay,debug):
    # Make GET Request to the endpoint to get the string.
    urlGET(baseurl,debug)
    # Parse the HTML page with BeautifulSoup and extract the string to be hashed.
    soupParse(debug)
    # Complete the MD5 hash of the string.
    hashString(debug)
    #Test Delay times
    if delay > 0:
        time.sleep(delay)
        print("Delay: ", str(delay))
    # Submit hash to the endpoint.
    postHash(baseurl,debug)
    # Wait for response and print it
    responsePrint(debug)

if __name__ == '__main__':
    # Parse arguments, including default arguments in config.json
    parser = argparse.ArgumentParser(description='Automate the process of the emdee five for life challenge.')
    parser.add_argument('--url', dest='url', default="",
                        help='URL for challenge site.')
    parser.add_argument('--time-test', action='store_true', default=False,
                        help='Test time delay. Script loops 5 times and increments time delay by 1/8 seconds.')
    parser.add_argument('--debug', action='store_true', default=False,
                        help='Enable Debugging mode.')
    args = parser.parse_args()
    # Promt user for URL if it's not included in provided arguments.
    if not args.url:
        baseurl = input("Enter URL: ")
    else:
        baseurl = args.url
    # Prompt user for URL protocol if it's not included.
    if not baseurl.startswith("http://") and not baseurl.startswith("https://"):
        protocol = input("Enter the protocol (http or https): ")
        baseurl = f"{protocol}://{baseurl}"
    if args.time_test:
        for i in range (5):
            delay = i/8
            main(baseurl,delay,args.debug)
            time.sleep(1)
    else:
        delay = 0
        main(baseurl,delay,args.debug)