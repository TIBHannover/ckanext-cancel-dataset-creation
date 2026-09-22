"""
Tests for plugin.py.

Tests are written using the pytest library (https://docs.pytest.org), and you
should read the testing guidelines in the CKAN docs:
https://docs.ckan.org/en/2.9/contributing/testing.html

To write tests for your extension you should install the pytest-ckan package:

    pip install pytest-ckan

This will allow you to use CKAN specific fixtures on your tests.

For instance, if your test involves database access you can use `clean_db` to
reset the database:

    import pytest

    from ckan.tests import factories

    @pytest.mark.usefixtures("clean_db")
    def test_some_action():

        dataset = factories.Dataset()

        # ...

For functional tests that involve requests to the application, you can use the
`app` fixture:

    from ckan.plugins import toolkit

    def test_some_endpoint(app):

        url = toolkit.url_for('myblueprint.some_endpoint')

        response = app.get(url)

        assert response.status_code == 200


To temporary patch the CKAN configuration for the duration of a test you can use:

    import pytest

    @pytest.mark.ckan_config("ckanext.myext.some_key", "some_value")
    def test_some_action():
        pass
"""
import pytest
from werkzeug.exceptions import Forbidden, NotFound

from ckan.plugins import toolkit
from ckanext.cancel_dataset_creation.controllers import BaseController
from ckanext.cancel_dataset_creation.lib import Helper

@pytest.mark.ckan_config("ckan.plugins", "cancel_dataset_creation")
@pytest.mark.ckan_config("SECRET_KEY", "test_secret")
@pytest.mark.usefixtures("with_plugins")
def test_cancel_route_rejects_get(app):
    response = app.get(
        toolkit.url_for(
            "cancel_dataset_creation.cancel_dataset",
            package_id="example",
            is_draft="0",
        ),
        status=404,
    )

    assert response.status_code == 404


def test_cancel_preserves_forbidden_response(monkeypatch):
    monkeypatch.setattr(
        Helper, "check_access_delete_package", lambda _package_id: False
    )

    def abort(status, message):
        assert status == 403
        raise Forbidden(description=message)

    monkeypatch.setattr(toolkit, "abort", abort)

    with pytest.raises(Forbidden, match="not authorized"):
        BaseController.cancel_dataset("example", "0")


def test_cancel_reports_missing_dataset(monkeypatch):
    monkeypatch.setattr(
        Helper, "check_access_delete_package", lambda _package_id: True
    )

    def package_delete(_context, _data_dict):
        raise toolkit.ObjectNotFound()

    monkeypatch.setattr(toolkit, "get_action", lambda _name: package_delete)
    monkeypatch.setattr(
        BaseController, "_context", lambda: {"user": "test-user"}
    )

    def abort(status, message):
        assert status == 404
        raise NotFound(description=message)

    monkeypatch.setattr(toolkit, "abort", abort)

    with pytest.raises(NotFound, match="Dataset not found"):
        BaseController.cancel_dataset("missing", "0")


@pytest.mark.usefixtures("with_request_context")
def test_cancel_uses_authenticated_context_and_redirects(monkeypatch):
    captured = {}
    monkeypatch.setattr(
        Helper, "check_access_delete_package", lambda _package_id: True
    )
    monkeypatch.setattr(
        BaseController, "_context", lambda: {"user": "test-user"}
    )

    def package_delete(context, data_dict):
        captured["context"] = context
        captured["data_dict"] = data_dict

    monkeypatch.setattr(toolkit, "get_action", lambda _name: package_delete)
    monkeypatch.setattr(
        toolkit,
        "redirect_to",
        lambda route, **kwargs: (route, kwargs),
    )

    result = BaseController.cancel_dataset("dataset-id", "1")

    assert captured == {
        "context": {"user": "test-user"},
        "data_dict": {"id": "dataset-id"},
    }
    assert result == ("user.read", {"id": "test-user"})


@pytest.mark.usefixtures("with_request_context")
def test_delete_access_helper_handles_authorization(monkeypatch):
    captured = {}

    def check_access(action, context, data_dict):
        captured.update(
            action=action, context=context, data_dict=data_dict
        )

    monkeypatch.setattr(toolkit, "check_access", check_access)

    assert Helper.check_access_delete_package("dataset-id") is True
    assert captured["action"] == "package_delete"
    assert captured["data_dict"] == {"id": "dataset-id"}


@pytest.mark.usefixtures("with_request_context")
def test_delete_access_helper_rejects_unauthorized_user(monkeypatch):
    def check_access(*_args):
        raise toolkit.NotAuthorized()

    monkeypatch.setattr(toolkit, "check_access", check_access)

    assert Helper.check_access_delete_package("dataset-id") is False
