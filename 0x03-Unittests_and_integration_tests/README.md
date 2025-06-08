# README.md

## 0x03. Unittests and Integration Tests

This project implements both **unit tests** and **integration tests** for a Python backend module. The main objective is to practice testing strategies using Python’s `unittest` framework, as well as mocking with `unittest.mock`, and to gain hands-on experience with parameterized tests and integration test setups.

### 📋 Project Structure

```bash
0x03-Unittests_and_integration_tests/
├── client.py
├── fixtures.py
├── test_client.py
├── test_utils.py
├── utils.py
└── README.md
```

### 📌 Overview

* **Unit Tests:**

  * Implemented in `test_utils.py`.
  * Tests small, isolated functions like `access_nested_map`, `get_json`, and `memoize`.
  * Uses `unittest.TestCase`, `parameterized.expand`, and `mock.patch`.

* **Integration Tests:**

  * Implemented in `test_client.py`.
  * Tests the integration of `GithubOrgClient` methods using live-like fixture data.
  * Uses `parameterized_class` to set up test data across multiple test cases.

### 🛠️ Key Features

✅ **Testing `access_nested_map`:**

* Validates correct nested dictionary access.
* Asserts expected values and exceptions using `assertEqual` and `assertRaises`.

✅ **Testing `get_json`:**

* Mocks HTTP requests using `patch` to avoid actual network calls.
* Tests that mocked `requests.get().json()` returns expected data.

✅ **Testing Memoization:**

* Validates that the `memoize` decorator caches function results.
* Uses `patch.object` to ensure methods are called only once.

✅ **Testing `GithubOrgClient`:**

* Tests `.org`, `_public_repos_url`, `public_repos`, and `has_license`.
* Applies `patch` and `PropertyMock` to simulate API calls.
* Uses fixtures from `fixtures.py` for realistic payloads.
* Uses `parameterized_class` to set up integration tests with multiple payloads.

### 📝 Usage

Activate the virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate    # Windows
pip install -r requirements.txt  # includes parameterized and pycodestyle
```

Run the tests:

```bash
python -m unittest test_utils.py
python -m unittest test_client.py
```

Check PEP8 compliance:

```bash
pycodestyle test_utils.py test_client.py
```

### 🔗 External Libraries Used

* **unittest** – Core testing framework.
* **parameterized** – For parameterizing tests and classes.
* **unittest.mock** – For mocking dependencies.

### 🗂️ Requirements

* Python 3.7+
* Code follows PEP8 (`pycodestyle`)
* All files are executable (`chmod +x filename.py`)
* All modules, classes, and functions include detailed docstrings explaining their purpose.
