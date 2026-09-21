# encoding: utf-8

import ckan.plugins.toolkit as toolkit
from ckanext.cancel_dataset_creation.lib import Helper

class BaseController():

    @staticmethod
    def _context():
        return {'user': getattr(toolkit.g, 'user', None)}

    @staticmethod
    def cancel_dataset(package_id, is_draft):
        if not Helper.check_access_delete_package(package_id):
            toolkit.abort(403, "You are not authorized to delete this dataset")

        context = BaseController._context()
        try:
            toolkit.get_action('package_delete')(context, {'id': package_id})
        except toolkit.ObjectNotFound:
            toolkit.abort(404, "Dataset not found")
        except toolkit.NotAuthorized:
            toolkit.abort(403, "You are not authorized to delete this dataset")
        except toolkit.ValidationError as error:
            toolkit.abort(400, str(error))

        if is_draft == '1':
            return toolkit.redirect_to('user.read', id=context['user'])

        return toolkit.redirect_to('dataset.search')

    @staticmethod
    def index():
        return "0"
