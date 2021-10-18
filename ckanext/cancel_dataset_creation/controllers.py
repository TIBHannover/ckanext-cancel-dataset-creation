# encoding: utf-8

import ckan.plugins.toolkit as toolkit
from flask import request
from ckanext.cancel_dataset_creation.lib import Helper

class BaseController():

    def cancel_dataset(package_id):
        try:
            if not Helper.check_access_delete_package(package_id):
                return toolkit.abort(403, "you are not authorized")
            
            toolkit.get_action('package_delete')({},{'id': package_id})
        except:
            toolkit.abort(500, "We cannot process this request")



        return '0'