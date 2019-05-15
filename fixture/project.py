from model.project import Project
import string
import random


class ProjectHelper:

    def __init__(self, app):
        self.app = app

    def create(self, project):
        wd = self.app.wd
        self.open_projects_page()
        wd.find_element_by_xpath('//input[@value="Create New Project"]').click()
        wd.find_element_by_name('name').send_keys(project.name)
        wd.find_element_by_name('description').send_keys(project.description)
        wd.find_element_by_xpath('//input[@value="Add Project"]').click()
        try:
            error_text = wd.find_element_by_xpath('//td[@class="form-title"]').text
            if error_text == 'APPLICATION ERROR #701':
                symbols = string.ascii_letters
                project.name = 'name_' + ''.join([random.choice(symbols) for i in range(random.randrange(5))])
                self.create(project)
        except:
            return True

        self.return_to_home_page()

    def return_to_home_page(self):
        wd = self.app.wd
        wd.find_element_by_link_text("My View").click()

    def open_projects_page(self):
        wd = self.app.wd
        wd.find_element_by_link_text("Manage").click()
        wd.find_element_by_link_text("Manage Projects").click()

    def delete_project_by_name(self, project):
        wd = self.app.wd
        self.open_projects_page()
        self.choose_project_by_name(project)
        wd.find_element_by_xpath('//input[@value="Delete Project"]').click()
        # apply
        wd.find_element_by_xpath('//input[@value="Delete Project"]').click()
        self.return_to_home_page()

    def choose_project_by_name(self, project):
        wd = self.app.wd
        wd.find_element_by_link_text(project.name).click()

    def get_projects_list(self):
        wd = self.app.wd
        self.open_projects_page()
        projects_list = []
        for element in wd.find_elements_by_xpath('//table[@class="width100"]//*[contains(@class, "row-")]'):
            id = element.find_element_by_xpath('.//td[1]/a').get_attribute('href').split('=', 1)[1]
            name = element.find_element_by_xpath('.//td[1]').text
            description = element.find_element_by_xpath('.//td[5]').text
            projects_list.append(Project(id=id, name=name, description=description))
        del projects_list[0]  # вырезать заголовок таблицы
        return list(projects_list)
