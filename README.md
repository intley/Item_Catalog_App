# Item Catalog
The Item Catalog project consists of developing an application that provides a list of items within a variety of categories, as well as provide a user registration and authentication system.

This project is a part of the Full Stack Nanodegree program at Udacity.

## Getting Started

#### Prerequisites
*  [Python 2/3](https://www.python.org/)
*  [Flask](http://flask.pocoo.org/)
*  [Vagrant](https://www.vagrantup.com/)
* [VirtualBox](https://www.virtualbox.org/)

#### Configuration
1. Make sure you have a command-line terminal installed on your system such as GitBash or the Terminal application on macOS.
2. Install Vagrant and Virtualbox.
3. Download or Clone [fullstack-nanodegree-vm](https://github.com/udacity/fullstack-nanodegree-vm) repository.
4. Launch Vagrant, instructions below.
5. Clone this Git Repository inside your vagrant folder.

#### Launching Vagrant:
1. To launch vagrant, navigate to the fullstack-nanodegree-vm folder and inside this folder, VagrantFile.
2. Once you are in the VagrantFile directory, you can start the virtual machine using the command:
```
vagrant up
```
3. Proceed to launch the VM using the following command:
```
vagrant ssh
```
And now change directory to the vagrant folder:
```
cd /vagrant
```

#### Launching Application:
1. To launch the application, once you are in the vagrant directory, make sure you have cloned this Git repository.
2. Proceed to launch the application using the following command:
```
python application.py
```
3. The application will be started in the port 5000 (configured in the application), and you may view the application by going to the following webpage :
[http://localhost:5000](http://localhost:5000)

## Authorization
The Application implements Google Signin using [OAuth2.0](https://oauth.net/2/).

For best results, it is recommended that you are not signed into a Google Account on launching the application.

## JSON Endpoints
The Item Catalog implements JSON endpoints for its data. To access the JSON Endpoints, you may view them in the following URL extensions:

1. Items for a given category:
```
localhost:5000/categories/string:category_name/JSON
```
For example : localhost:5000/categories/Books/JSON

2. For a specific item:
```
localhost:5000/categories/string:category_name/string:item_name/JSON
```
For example:
localhost:5000/categories/Books/Da Vince Code/JSON

## License
This project was built by Rahul Rajendran for the sole purpose of completing his Full Stack Nanodegree in addition to increasing and instilling his knowledge of the Flask framework.
