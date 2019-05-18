def test_signup(app):
    username = 'user12345'
    password = 'test'
    app.james.ensure_user_exists(username, password)

