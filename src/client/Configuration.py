import os
class ConfigurationService:
    '''
        This provides configuration details to other objects that require them.
    '''
    def __init__(self, server_domain, port, resource_name):
        self.server_domain = server_domain
        self.port = port
        self.resource_name = resource_name
