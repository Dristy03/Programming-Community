# Getting Started

For setting up the project, the following steps are needed to be done:

- The system must have python 3.10 and pip installed and set up as environment variable
- Also user need to have PostgreSQL 14.1 installed and its service running. 
- If virtualenv is not installed in the pc, then open your cmd / git bash in the directory you want your project file to be and write the command: **pip install virtualenv**
- The following commands should be given next:
- virtualenv FOLDERNAME [folder name is up to one's wish. This will create a virtural environment for the project]
- cd FOLDERNAME [For entering into the created folder]
- git clone https://github.com/cse-250-2018/G15-Programming-Community.git [cloning this repository in the folder]
- Script/activate [activating the env]
- **cd G15-Programming-Community** [For entering the project files]
- pip install -r requirements.txt [installing all the required packages needed for the project]
- Then the user need to create a database according to the settings.py file in our project. They can change the credentials if they want.
- python manage.py makemigrations
- python manage.py migrate
- python manage.py runserver [running the server]

<br/>
<br/>

# FAQ

**Q:** I am getting "manage.py is not found" error. How to solve it?

**A:**
 Make sure that your directory is in the folder "G15-Programming-Community" where the manage.py is located.

**Q:** Some of the required libraries are not downloading?

**A:** Make sure to upgrade pip


**Q:** I am having trouble setting up PostgreSQL in my pc?

**A:** The best option is to google it or watch some videos to solve your problem. 

**Q:** I am not getting any verification mail

**A:** Make sure you have given the right email address

**Q:** How to get rid of the warning sign in the navbar?

**A:** Complete the profile info

**Q:** Can I upload videos in Resource? 

**A:** Certainly!
