import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from flask import Blueprint


class CancelDatasetCreationPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IBlueprint)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('public/statics', 'ckanext-cancel-dataset-creation')
    

    def get_blueprint(self):

        blueprint = Blueprint(self.name, self.__module__) 


        return blueprint