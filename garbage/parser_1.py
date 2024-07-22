import subprocess
import sys
import os
from datetime import datetime
import glob
from bs4 import BeautifulSoup

def install(package):
    """Install a package using pip."""
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# List of required packages
required_packages = [
    'beautifulsoup4==4.12.2',
    'lxml==5.2.2'
]

# Install packages if not already installed
for package in required_packages:
    try:
        __import__(package.split('==')[0])
    except ImportError:
        install(package)

# get HTML files that have today's date in the filename
def get_today_date():
    return datetime.now().strftime('%Y-%m-%d')

def find_html_file_with_date(directory, date_str):
    # Create a search pattern with today's date
    pattern = os.path.join(directory, f'*{date_str}*.html')
    html_files = glob.glob(pattern)
    
    # Return the first file found (or None if no files are found)
    if html_files:
        return html_files[0]  # Assuming you only need one file
    return None

def get_html_content():
    folder_path = '.'
    today_date = get_today_date()
    print(today_date)
    html_file = find_html_file_with_date(folder_path, today_date)

    if html_file:
        print(f"Found HTML file: {html_file}")
    else:
        print("No HTML file found with today's date. Format as '2024-07-22'.")


    with open(html_file, 'r', encoding='utf-8') as file:
        content = file.read()
        return content


# Function to add checkboxes to the HTML
def add_checkboxes(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find all images and their parent elements
    images = soup.find_all('img')
    
    for idx, img in enumerate(images):
        # Create a checkbox for each image
        checkbox = soup.new_tag('input', type='checkbox', id=f'graph{idx+1}', value=f'graph{idx+1}', **{'class': 'large-checkbox'})
        label = soup.new_tag('label', for_=f'graph{idx+1}')
        label.string = f'Graph {idx+1}'
        
        # Add checkbox and label before the image
        img.insert_before(checkbox)
        img.insert_before(label)
        img.insert_before(soup.new_tag('br'))
        
    return str(soup)

html_content = get_html_content()
updated_html_content = add_checkboxes(html_content)

# Save to a new HTML file
with open('updated_file.html', 'w', encoding='utf-8') as file:
    file.write(updated_html_content)