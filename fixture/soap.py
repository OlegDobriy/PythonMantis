from suds.client import Client
from suds import WebFault
from model.project import Project


class SoapHelper:

    def __init__(self, app, config):
        self.app = app
        self.client = Client('http://localhost/mantisbt-1.2.20/api/soap/mantisconnect.php?wsdl')
        self.config = config
        self.admin_username = config['webadmin']['username']
        self.admin_password = config['webadmin']['password']

    def can_login(self, username, password):
        try:
            self.client.service.mc_login(username, password)
            return True
        except WebFault:
            return False

    def get_projects_list(self):
        try:
            projects_list_from_soap = self.client.service.mc_projects_get_user_accessible(self.admin_username, self.admin_password)
            projects_list = []
            for project in projects_list_from_soap:
                id = project[0]
                name = project[1]
                description = project[7]
                projects_list.append(Project(id=str(id), name=str(name), description=str(description)))
            return list(projects_list)
        except WebFault:
            return False
