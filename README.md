[![Build Status](https://travis-ci.org/jaodur/Book-A-Meal_api.svg?branch=Develop)](https://travis-ci.org/jaodur/Book-A-Meal_api)
[![Coverage Status](https://coveralls.io/repos/github/jaodur/Book-A-Meal_api/badge.svg?branch=Develop)](https://coveralls.io/github/jaodur/Book-A-Meal_api?branch=Develop)

## __Book A Meal__ 
is a web based app that enables  several caterers to setup menus,and manage orders. The app also allows
customer to order a meal, modify their orders, check their order history and also have a quick glance at the trending
menus.

The app is built with ___python/Flask___ for its backend.

## __How to setup the api backend__

## ___Prerequisites___

* `Git` [Guide to Git](https://git-scm.com/doc) [Installing Git](https://gist.github.com/derhuerst/1b15ff4652a867391f03)
* `Python 3.5 or higher`
* `Pip` [Guide to installing pip](https://github.com/BurntSushi/nfldb/wiki/Python-&-pip-Windows-installation)


## __Cloning and installing dependencies__
* After installing the **`prerequisites`** above, clone the repository Develop branch
using this command git `clone -b Develop https://github.com/jaodur/Book-A-Meal_api.git`
* Change into the newly cloned repo through `cd Book-A-Meal_api`
* Install the required dependencies through command `pip3 install -r requirements.txt`
 **`Note`** These dependencies can be installed in virtual environment, by running the same
command above after installing and activating a `Python` virtual environment.
[Guide to installing virtual environment](https://virtualenv.pypa.io/en/stable/installation/)


## __starting the application__
After cloning and installing the required dependencies, start the app using the command
below
**`python run.py`** in [terminal](https://www.taniarascia.com/how-to-use-the-command-line-for-apple-macos-and-linux/)



##  __How to use the api__
This `api` was documented flasgger swagger.
After starting the application, the documention, if the you are working on the same machine on which
the application is running `(localhost)`. Then the api documentation can be acccessed
through the link that looks like **`http://localhost:5000/apidocs/`**. Where the 5000 is the port on
which the application is running. click the like for a demo if the applicatioon is 
running on port 5000.

Documentation  |
---       | 
[LINK-local](http://localhost:5000/apidocs/) |
[LINK-Online demo](https://book-a-meal-odur.herokuapp.com/apidocs/) |



## __Author__

Odur Joseph
