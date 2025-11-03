from fastapi.testclient import TestClient
import io, os, sys

# Add parent directory to import from main.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app

client = TestClient(app)

def get_sample_csv_bytes():
    csv_content = """hours_studied,final_score
1,55
2,60
3,65
4,70
5,75
"""
    return io.BytesIO(csv_content.encode("utf-8"))


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello from FastAPI!"}


def test_analyze_endpoint_success():
    file_data = get_sample_csv_bytes()

    response = client.post(
        "/analyze",
        files={"file": ("test.csv", file_data, "text/csv")},
        data={"target_column": "final_score"}
    )

    assert response.status_code == 200

    json_data = response.json()
    expected_keys = {"model_used", "problem_type", "feature_importance", "score"}

    for key in expected_keys:
        assert key in json_data, f"Missing key in response: {key}"

    assert isinstance(json_data["model_used"], str)
    assert isinstance(json_data["problem_type"], str)
    assert isinstance(json_data["feature_importance"], dict)
    assert isinstance(json_data["score"], (float, int))


def test_analyze_with_missing_target_column():
    file_data = get_sample_csv_bytes()

    response = client.post(
        "/analyze",
        files={"file": ("test.csv", file_data, "text/csv")},
        data={"target_column": "non_existent_column"}
    )

    assert response.status_code == 400
    assert "Target column" in response.json()["detail"][0]


def test_analyze_with_invalid_csv():
    bad_file = io.BytesIO(b"this,is,not,a,real,csv")
    response = client.post(
        "/analyze",
        files={"file": ("fake.csv", bad_file, "text/csv")},
        data={"target_column": "final_score"}
    )

    assert response.status_code == 400
    assert "Target column 'final_score' not found in dataset." in response.json()["detail"]
