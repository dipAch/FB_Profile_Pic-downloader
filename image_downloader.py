# Download Profile Pictures from https://www.facebook.com
# Version: Python 2.7.6
# This program scraps images off https://www.facebook.com
# This program is purely intended for educational puposes and testing the powers of Python Language Libraries
# Not made with the intention to infringe Facebook Policies.

# All imports here
import urllib
import urllib2

# Contains the actual Image source URL
src_attr = []

# Issue request to retrieve profile page
# Wait for the response object to return and,
# Pass it to the function 'convert_2_source()' for further processing
# Can be modified to fetch multiple Profile Pages for different USER_IDs
# Can also be implemented using Python multithreading, food for thought?
def seed_url_provider():
    convert_2_source(urllib2.urlopen('https://www.facebook.com/dipankar.achinta'))                  

# Convert response object (HTML blob) to a parsable string and,
# Pass it to the function 'extract_img()' for getting the image source URL
def convert_2_source(page_url):
    source_code_of_page = '' 
    for eachLine in page_url:
        source_code_of_page += str(eachLine)
        extract_img(source_code_of_page) 

# Extract image from the source string of the profile page	
# The real meat of the program is here
# Find the class that holds the Profile Picture
# Get the source attribute string for the image
# Can be implemented using recursion as well, 
# But introduces overhead in terms of the number of recursive calls (& size of the recursive call stack)
def extract_img(web_page_source):
    find_img = web_page_source.find("<img", 0)
    find_class = web_page_source.find("class=", find_img)
    start_quote = web_page_source.find("\"", find_class)
    end_quote = web_page_source.find("\"", start_quote + 1)
    class_content = web_page_source[(start_quote + 1) : end_quote]
    if class_content == 'profilePic img':
        find_src = web_page_source.find("src=", end_quote + 1)
        src_start_quote = web_page_source.find("\"", find_src)
        src_end_quote = web_page_source.find("\"", src_start_quote + 1)
        src_attr.append(web_page_source[(src_start_quote + 1) : src_end_quote])
    while web_page_source.find("<img", end_quote + 1) != (-1) and len(src_attr) != 1:
        next_img = web_page_source.find("<img", end_quote + 1)
        next_class = web_page_source.find("class=", next_img)
        next_start_quote = web_page_source.find("\"", next_class)
        next_end_quote = web_page_source.find("\"", next_start_quote + 1)
        class_content = web_page_source[(next_start_quote + 1) : next_end_quote]
        if class_content == 'profilePic img':
            find_next_src = web_page_source.find("src=", next_end_quote + 1)
            next_src_start_quote = web_page_source.find("\"", find_next_src)
            next_src_end_quote = web_page_source.find("\"", next_src_start_quote + 1)
            src_attr.append(web_page_source[(next_src_start_quote + 1) : next_src_end_quote])
        end_quote = next_end_quote

# Start fetching Profile Page per USER_ID
seed_url_provider()

# For Debugging Purposes
print src_attr

# Download image if we could find the image source string
# After downloading, put it in the specified folder
if src_attr:
    filename = src_attr[0].split("/")[-1]
    dest_path = "~/pythonProgramming/photos/" + filename
    for img_source in src_attr:
        urllib.urlretrieve(img_source, dest_path)
    print "Image downloaded !!!" 
else:
    print "Download unsuccessfull !!!"