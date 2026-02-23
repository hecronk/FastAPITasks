import pytest
from unittest.mock import MagicMock
from src.tasks.tasks import process_task

@pytest.mark.parametrize("task_id", [1])
def test_process_task(monkeypatch, task_id):
    monkeypatch.setattr("src.tasks.tasks.get_random_numbers", lambda count: {"data": 42, "errors": {}})

    # мок сессии
    class DummyTask:
        def __init__(self):
            self.result = None
            self.errors = None
            self.status = "NEW"
            self.started_at = None
            self.completed_at = None

    dummy = DummyTask()
    session_mock = MagicMock()
    session_mock.execute.return_value.scalar_one_or_none.return_value = dummy
    session_mock.commit.return_value = None
    session_mock.refresh.return_value = None

    monkeypatch.setattr("src.tasks.tasks.get_sync_session", lambda: session_mock)

    result = process_task(task_id)
    assert result["status"] == "COMPLETED"
    assert dummy.result is None
