from model.project import Project


def test_add_project(app):
    old_list = app.project.get_projects_list()
    project = Project(name='123', description='456')
    app.project.create(project)
    new_list = app.project.get_projects_list()
    old_list.append(project)
    pass

