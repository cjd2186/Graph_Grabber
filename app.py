from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from bs4 import BeautifulSoup
import os
from copy import deepcopy

app = Flask(__name__)

# Folder to store HTML files
HTML_FOLDER = 'static'
os.makedirs(HTML_FOLDER, exist_ok=True)

# Utility function to get HTML content with checkboxes
def add_checkboxes_to_html(html_content, checked_images=None):
    soup = BeautifulSoup(html_content, 'html.parser')
    images = soup.find_all('img')

    if checked_images is None:
        checked_images = []

    # Find or create the form tag
    form = soup.find('form')
    if form is None:
        form = soup.new_tag('form', action='/process', method='post', id='image-form')
        soup.body.insert(0, form)  # Insert form at the beginning of the body

    for idx, img in enumerate(images):
        checkbox_id = f'checkbox{idx+1}'
        checkbox = soup.new_tag('input', type='checkbox', attrs={'name': 'images', 'id': checkbox_id, 'value': img['src'], 'class': 'large-checkbox'})
        if img['src'] in checked_images:
            checkbox['checked'] = 'checked'

        label = soup.new_tag('label', **{'for': checkbox_id})
        label.string = f'Image {idx+1}'

        img.insert_before(checkbox)
        img.insert_before(label)
        img.insert_before(soup.new_tag('br'))

    # Add a hidden input to store the selected image IDs
    hidden_input = soup.new_tag('input', type='hidden', attrs={'name': 'selected_ids', 'id': 'selected_ids'})
    form.append(hidden_input)

    # Add a submit button if not already present
    submit_button = soup.new_tag('input', type='submit', value='Submit')
    form.append(submit_button)

    # Add JavaScript to handle form submission
    script = soup.new_tag('script')
    script.string = """
        document.getElementById('image-form').addEventListener('submit', function(event) {
            var selectedIds = [];
            var checkboxes = document.querySelectorAll('input[type=checkbox]:checked');
            checkboxes.forEach(function(checkbox) {
                selectedIds.push(checkbox.value);
            });
            document.getElementById('selected_ids').value = selectedIds.join(',');
        });
    """
    soup.body.append(script)

    return str(soup)

@app.route('/')
def index():
    html_file = find_html_file_with_date('.', get_today_date())
    if not html_file:
        return "No HTML file found", 404

    with open(html_file, 'r', encoding='utf-8') as file:
        content = file.read()
    
    updated_html_content = add_checkboxes_to_html(content)
    with open(os.path.join('templates', 'form.html'), 'w', encoding='utf-8') as file:
        file.write(updated_html_content)

    return render_template('form.html')

@app.route('/process', methods=['POST'])
def process():
    selected_ids = request.form.get('selected_ids', '')
    selected_ids = selected_ids.split(',')
    print("Selected IDs:", selected_ids)

    # Generate a new HTML file based on selected IDs
    original_html_file = find_html_file_with_date('.', get_today_date())
    if not original_html_file:
        return "Original HTML file not found", 404

    with open(original_html_file, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
    
    # Remove unselected images and associated text
    images = soup.find_all('img')
    for img in images:
        if img['src'] not in selected_ids:
            # Remove image and its associated text
            prev_sibling = img.find_previous_sibling()
            next_sibling = img.find_next_sibling()

            # Remove the image
            img.decompose()

            # Remove associated text if it's not adjacent to another image
            if prev_sibling and isinstance(prev_sibling, str) and prev_sibling.strip():
                prev_sibling.extract()
            if next_sibling and isinstance(next_sibling, str) and next_sibling.strip():
                next_sibling.extract()

    # Remove remaining text nodes that are not adjacent to any images
    for text_node in soup.find_all(string=True):
        if isinstance(text_node, str) and text_node.strip():
            # Check if the text node is not between images
            prev_sibling = text_node.find_previous_sibling()
            next_sibling = text_node.find_next_sibling()
            if not (prev_sibling and prev_sibling.name == 'img') and not (next_sibling and next_sibling.name == 'img'):
                text_node.extract()

    new_html_file = os.path.join(HTML_FOLDER, 'selected_images.html')
    with open(new_html_file, 'w', encoding='utf-8') as file:
        file.write(str(soup))

    return redirect(url_for('serve_file', filename='selected_images.html'))

@app.route('/static/<path:filename>')
def serve_file(filename):
    # Ensure the file is in the correct directory
    return send_from_directory(HTML_FOLDER, filename)

def get_today_date():
    from datetime import datetime
    return datetime.now().strftime('%Y-%m-%d')

def find_html_file_with_date(directory, date_str):
    import glob
    pattern = os.path.join(directory, f'*{date_str}*.html')
    html_files = glob.glob(pattern)
    if html_files:
        return html_files[0]
    return None

if __name__ == '__main__':
    app.run(debug=True)
