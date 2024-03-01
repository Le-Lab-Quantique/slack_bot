def test_testing_config(app_context):
    from flask import current_app as app

    assert app.config["DEBUG"]
    assert app.config["TESTING"]
