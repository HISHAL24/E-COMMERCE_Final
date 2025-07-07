import pytest
from unittest.mock import patch, MagicMock
from service.catalogue_service import catalogueService
from dto.catalogue_dto import catalogue

@pytest.fixture
def mock_conn_cursor():
    mock_cursor = MagicMock()
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    return mock_conn, mock_cursor

@pytest.fixture
def sample_catalogue():
    return catalogue(
        catalogue_name="Test Product",
        catalogue_description="Test Description",
        effective_from="2025-01-01",
        effective_to="2025-12-31",
        status="Active"
    )

@patch("service.catalogue_service.get_connection")
def test_create_catalogue(mock_get_conn, mock_conn_cursor, sample_catalogue):
    mock_conn, mock_cursor = mock_conn_cursor
    mock_get_conn.return_value = mock_conn
    mock_cursor.rowcount = 1

    service = catalogueService()
    result = service.create_catalogue(sample_catalogue)
    assert result == 1
    mock_cursor.execute.assert_called_once()

@patch("service.catalogue_service.get_connection")
def test_get_catalogue_by_id_found(mock_get_conn, mock_conn_cursor):
    mock_conn, mock_cursor = mock_conn_cursor
    mock_get_conn.return_value = mock_conn
    expected_result = {"catalogue_id": 1, "catalogue_name": "Test Product"}
    mock_cursor.fetchone.return_value = expected_result

    service = catalogueService()
    result = service.get_catalogue_by_id(1)
    assert result == expected_result

@patch("service.catalogue_service.get_connection")
def test_get_all_catalogues(mock_get_conn, mock_conn_cursor):
    mock_conn, mock_cursor = mock_conn_cursor
    mock_get_conn.return_value = mock_conn
    expected_list = [{"catalogue_id": 1}, {"catalogue_id": 2}]
    mock_cursor.fetchall.return_value = expected_list

    service = catalogueService()
    result = service.get_all_catalogues()
    assert result == expected_list

@patch("service.catalogue_service.get_connection")
def test_delete_catalogue_by_id_success(mock_get_conn, mock_conn_cursor):
    mock_conn, mock_cursor = mock_conn_cursor
    mock_get_conn.return_value = mock_conn
    mock_cursor.rowcount = 1

    service = catalogueService()
    result = service.delete_catalogue_by_id(1)
    assert result is True

@patch("service.catalogue_service.get_connection")
def test_update_catalogue_by_id(mock_get_conn, mock_conn_cursor, sample_catalogue):
    mock_conn, mock_cursor = mock_conn_cursor
    mock_get_conn.return_value = mock_conn
    mock_cursor.rowcount = 1

    service = catalogueService()
    result = service.update_catalogue_by_id(1, sample_catalogue)
    assert result == 1
