from fastapi.testclient import TestClient
from main import app
import io

client = TestClient(app)

def test_ask_success():
    # A valid CSV for regression
    csv_content = """study_hours,test_score
1,50
2,60
3,70
4,80
5,90
"""
    file_data = io.BytesIO(csv_content.encode("utf-8"))

    # Step 1: Analyze
    analyze_response = client.post(
        "/analyze",
        files={"file": ("valid.csv", file_data, "text/csv")},
        data={"target_column": "test_score"}
    )
    assert analyze_response.status_code == 200

    # Step 2: Ask a question
    ask_response = client.post(
        "/ask",
        data={"question": "What feature was most important?"}
    )

    # Should return a 200 OK with an answer
    assert ask_response.status_code == 200
    data = ask_response.json()
    assert "answer" in data


def test_analyze_missing_target_column():
    # CSV without the target column
    bad_csv = """hours_studied,final_score
1,55
2,60
3,65
"""
    file_data = io.BytesIO(bad_csv.encode("utf-8"))

    # Intentionally wrong target column
    response = client.post(
        "/analyze",
        files={"file": ("bad.csv", file_data, "text/csv")},
        data={"target_column": "not_in_dataset"}
    )

    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "Target column" in str(data["detail"][0])
