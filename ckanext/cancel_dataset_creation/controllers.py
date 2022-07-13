# encoding: utf-8

import ckan.plugins.toolkit as toolkit
from flask import request, redirect
import ckan.lib.helpers as h
from ckanext.cancel_dataset_creation.lib import Helper

class BaseController():

    def cancel_dataset(package_id, is_draft):
        try:
            if not Helper.check_access_delete_package(package_id):
                return toolkit.abort(403, "you are not authorized")

            toolkit.get_action('package_delete')({},{'id': package_id})
        except:
            toolkit.abort(500, "We cannot process this request")

        if is_draft == '1':
            return  redirect(h.url_for('user.read', id=toolkit.g.userobj.name,  _external=True)) 

        return  redirect(h.url_for('dataset.search',  _external=True)) 
    

    def index():
        return "0"