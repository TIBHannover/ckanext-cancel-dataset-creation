import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from flask import Blueprint
from ckanext.cancel_dataset_creation.controllers import BaseController
from ckan.lib.plugins import DefaultTranslation


class CancelDatasetCreationPlugin(plugins.SingletonPlugin, DefaultTranslation):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.ITranslation)
    plugins.implements(plugins.IResourceController)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('public/statics', 'ckanext-cancel-dataset-creation')
    

    def get_blueprint(self):

        blueprint = Blueprint(self.name, self.__module__) 
        
        blueprint.add_url_rule(
            u'/cancel_dataset_creation/cancel_dataset/<package_id>/<is_draft>',
            u'cancel_dataset',
            BaseController.cancel_dataset,
            methods=['POST']
            )
        
        blueprint.add_url_rule(
            u'/cancel_dataset_creation/index',
            u'index',
            BaseController.index,
            methods=['GET']
            )


        return blueprint

    # IResourceController
    def before_resource_create(self, context, resource):
        resource['private'] = False

    def after_resource_create(self, context, resource):
        pass

    def before_resource_update(self, context, current, resource):
        pass

    def after_resource_update(self, context, resource):
        pass

    def before_resource_delete(self, context, resource, resources):
        pass

    def after_resource_delete(self, context, resources):
        pass

    def before_resource_show(self, resource_dict):
        return resource_dict

    # Legacy CKAN callback retained for compatibility with older releases.
    def before_create(self, context, data_dict):
        self.before_resource_create(context, data_dict)
        return data_dict

    def after_create(self, context, resource):
        return self.after_resource_create(context, resource)

    def before_update(self, context, current, resource):
        return self.before_resource_update(context, current, resource)

    def after_update(self, context, resource):
        return self.after_resource_update(context, resource)

    def before_delete(self, context, resource, resources):
        return self.before_resource_delete(context, resource, resources)

    def after_delete(self, context, resources):
        return self.after_resource_delete(context, resources)

    def before_show(self, resource_dict):
        return self.before_resource_show(resource_dict)
