# Emdee five for life
## Intro
Emdee five for life is an easy retired challenge from Hack The Box. It is part of the Dante Track. This challenge is pretty straight forward, and requires that you write a script to scrape text from a web page, parse that text, hash a string into md5 and submit that hash to get the flag.

When you visit the site provided, the web server gives you a simple web page with a string and a text submission box. The instructions tell you to submit the MD5 hash of the presented string.

## My Initial testing
First I simply did as the web page said. I found an online tool to hash the string. In this case I used [MD5 Hash Generator](https://www.md5hashgenerator.com/). When I submitted the hash, it said, "Too Slow!"

## Further Exploration
I opened burp suite and repeated the same test to capture the requests and responses. The main things I took note of were that the request was a POST request, the cookie in the header was a php session ID "PHPSESSID", and the data sent in the request was "hash={the hash value}". I also noticed that none of the responses I had captured sent me a "Set Cookie" header. I cleared the cookies for the site and repeated the initial test. That got me the initial GET request and the Set Cookie header.
After gathering this information in burp, I recreated the requests with curl.

## Curl test
I will just provide the commands I used and a brief description of the responses. See the [curl test](curl-test.md) page for the request and response details. 

I started with a simple GET request.
```bash
curl {IP Address}:{Port}
```
I got the string to hash and the session cookie in response.

After a little trial and error, I sent this POST request.
```bash
curl --data "hash=f726c4a8818b8dc67f8ce26e3b45ba77" --cookie "PHPSESSID=f726c4a8818b8dc67f8ce26e3b45ba77" {IP Address}:{Port}
```
The response from this request had the "Too Slow" string.

With this information I figured a script was going to be the easiest way to get hash submitted quickly enough.

## Python script for Emdee five for life
The script is the [md54life.py](md54life.py) file included with this write up.
### What I needed the script to do.
1. GET the web page and PHP Session ID.
2. Parse the web page for the string to hash.
3. Hash the string.
4. POST the hash along with the session ID.
5. Print the result.

### The Process
I broke down each step into a function in the script. I added a few other functions in the script as well for some added functionality. I used the argparse library to add some argument parsing into my script with the url being the main argument to pass into the script. In case the user, I, forgot to put the URL into an argument, the script prompts the user, me, for a url if I don't include it. I also added a debug function that pauses the script if I have a debug argument set to true. I put a call to the debug function at the start of each other function.

The argument variables are passed into the ``main()`` function, which has calls to the rest of the functions.
```python
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
```
The first function, ``urlGET()`` uses the requests library to send the GET request and retrieve the session ID cookie from the response. The session ID is saved as a global variable "session_id".

The next function, ``soupParse()`` uses Beautiful Soup to scrape the web page and gets the ``<h3>TEXT</h3>`` and saves the string as a global variable "string_to_hash".

Next is the ``hashString()`` function, which as its name suggests, hashes the "string_to_hash" into md5 in hex format. The hash is saved as a global variable "md5_hash".

The ``postHash()`` function sends the "md5_hash" as data and "session_id" as a cookie header to the server as a POST request.

Finally, the ``responsePrint()`` function prints the response of the POST request which contained the flag.

## Further Exploration
You may have noticed the delay statements in the ``main()`` function. After getting the flag, I wanted to know what the time limit was to post the hash. I added the delay variable and a loop. The loop ran five times incrementing the time delay with each pass. I started with 1 second intervals, then half second, quarter second, and finally eighth second intervals. 
```python
if args.time_test:
        for i in range (5):
            delay = i/8
            main(baseurl,delay,args.debug)
            time.sleep(1)
    else:
        delay = 0
        main(baseurl,delay,args.debug)
```
I found that the allotted time to submit the hash is 0.25 seconds. Definitely not long enough to complete the challenge without writing a script.