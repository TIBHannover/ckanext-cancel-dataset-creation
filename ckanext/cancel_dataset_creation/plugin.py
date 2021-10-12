import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from flask import Blueprint
from ckanext.cancel_dataset_creation.controllers import BaseController
from ckan.lib.plugins import DefaultTranslation


class CancelDatasetCreationPlugin(plugins.SingletonPlugin, DefaultTranslation):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.ITranslation)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('public/statics', 'ckanext-cancel-dataset-creation')
    

    def get_blueprint(self):

        blueprint = Blueprint(self.name, self.__module__) 
        
        blueprint.add_url_rule(
            u'/cancel_dataset_creation/cancel_dataset',
            u'cancel_dataset',
            BaseController.cancel_dataset,
            methods=['POST']
            )


        return blueprint