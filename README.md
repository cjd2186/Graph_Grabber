How to use:
* open the email in browser
* double click and save the email as an html file, make sure the date is in the name '2024-07-22'
  * the program checks for an html with today's date to use
* Open terminal in VSCode
  * 'crtl' + '~'
* download this github repo:
  * type: git clone https://github.com/cjd2186/Graph_Grabber.git
* Activate python virtual environment to get space for packages to install:
  * type: source venv/bin/activate
* Install necessary packages:
  * pip install requirements.txt
* Run app:
  * python app.py
  * this launches the Flask webserver on your laptop
* open web browser (e.g. firefox):
  * make sure you close any existing tab using localhost, sometimes it makes the Flask server act weird
  * go to https://localhost
  * or try https://127.0.0.1:5000 (this is the same thing as localhost)
  * this goes to the ip address that is on your laptop and goes to the application on port 5000
* select the images you want to include
* press submit on top left of webpage
  * <img width="1728" alt="image" src="https://github.com/user-attachments/assets/083b51a0-069e-42f1-abd8-1505dee3c812">

* double click on whitespace on new webpage (should be localhost/static/selected_images) and print --> save as pdf
  * can also just press cmd+p
  * <img width="1723" alt="image" src="https://github.com/user-attachments/assets/7ea01502-834d-43e9-8f17-d26d6d115d47">
* go back to VSCode terminal
  * press 'crtl' + 'c' to shut down the webserver
* type 'deactivate' to leave the virtual environment

## If any errors arise in this process, type the error message in chatgpt or contact me with any issues ##
