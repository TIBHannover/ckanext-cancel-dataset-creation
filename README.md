# ckanext-cancel-dataset-creation

The plugin ables users to delete a draft dataset + cancel and delete a dataset during dataset creation process. 


## Requirements

Compatibility with core CKAN versions:

| CKAN version    | Compatible?   |
| --------------- | ------------- |
|  2.9 | Yes    |
| earlier | Not Tested |           |


## Installation

To install ckanext-cancel-dataset-creation :

1. Activate your CKAN virtual environment, for example:

     . /usr/lib/ckan/default/bin/activate

2. Clone the source and install it on the virtualenv (Suggested location: /usr/lib/ckan/default/src)
:

        git clone https://github.com/TIBHannover/Ckanext-Cancel-Dataset-Creation.git
        cd Ckanext-Cancel-Dataset-Creation
        pip install -e .
        pip install -r requirements.txt

3. Add `cancel_dataset_creation` to the `ckan.plugins` setting in your CKAN
   config file (by default the config file is located at
   `/etc/ckan/default/ckan.ini`).

4. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu:

        sudo service apache2 reload



