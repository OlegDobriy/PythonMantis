from model.project import Project
import random


def test_add_project(app):
    old_list = app.project.get_projects_list()
    if len(old_list) == 0:
        project = Project(name='123', description='456')
        app.project.create(project)
    project = random.choice(old_list)
    app.project.delete_project_by_name(project)
    new_list = app.project.get_projects_list()
    old_list.remove(project)
    assert sorted(old_list, key=Project.sorting_name) == sorted(new_list, key=Project.sorting_name)
