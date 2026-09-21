# encoding: utf-8

import ckan.plugins.toolkit as toolkit


class Helper():

    '''
        check user is authorized to delete a dataset
    '''
    def check_access_delete_package(package_id):
        context = {
            'user': getattr(toolkit.g, 'user', None),
            'auth_user_obj': getattr(toolkit.g, 'userobj', None),
        }
        data_dict = {'id':package_id}
        try:
            toolkit.check_access('package_delete', context, data_dict)
            return True

        except toolkit.NotAuthorized:
            return False
