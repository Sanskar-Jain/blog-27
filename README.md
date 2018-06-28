# Blog-27 - A Blogging Site

A Django-powered Blogging Site which allows users' to view posts, like and share on facebook and comment on them. Admins can create/update posts, save them as drafts. Comments are implemented using Django's Generic Foreign Keys.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

You should have Python3 and virtual environment installed on your computer.
Install Python3 from https://www.python.org/ and then install virtual enviroment as shown below.

```
pip install virtualenv
```

### Installing

First Clone this project to your PC.

```
git clone git@github.com:Sanskar-Jain/blog-27.git
```
then go into that directory and install the requirements.
```
cd 
pip install -r requirements.txt
```
Then create a super user
```
cd src
python manage.py createsuperuser
```
Fill the name,email and password and then runserver
```
python manage.py runserver
```

Then you are good to go.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* CodingForEntrepreneurs
* Django documentation
