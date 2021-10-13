# encoding: utf-8

import ckan.plugins.toolkit as toolkit


class Helper():

    '''
        check user is authorized to delete a dataset
    '''
    def check_access_delete_package(package_id):
        context = {'user': toolkit.g.user, 'auth_user_obj': toolkit.g.userobj}
        data_dict = {'id':package_id}
        try:
            toolkit.check_access('package_delete', context, data_dict)
            return True

        except toolkit.NotAuthorized:
            return False