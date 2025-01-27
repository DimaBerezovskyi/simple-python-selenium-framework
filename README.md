
# Simple Python Selenium UI Automation Framework

A simple UI automation framework built with:
- **Python**: 3.9 - 3.12
- **pytest**: 8.3.0
- **Selenium**: 4.24.0
- **CI**: GitHub Actions

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue)](https://www.linkedin.com/in/dmytro-berezovskyi/)

## Features

- User-friendly UI automation framework.
- Built on popular Python libraries: pytest and Selenium.
- Supports **Chrome**, **Firefox**, and **Remote** browsers for UI testing.
- Utilities for setting up and managing WebDriver instances.
- Integrated with **GitHub Actions** CI workflow for Darwin (Mac) and Linux.
- Supports multiple environments: **dev**, **stage**.
- Generates **pytest reports** and **custom logs**.
- Secure Secrets Handling: Sensitive data like passwords are encrypted and stored securely.
- Test Data Management: Integrated with YAML files for test data storage and access.

## Getting Started

### Prerequisites

- Python 3.8 - 3.12
- If you're not using macOS with ARM64 architecture or a Selenium version below 4.24.0, please upload the appropriate driver corresponding to your OS to the `resources` directory.
- secure-test-automation for encrypting sensitive data

### Local Usage

1. Clone this repository:
   ```bash
   git clone <repository-url>
   ```
2. Install required dependencies:
   ```bash
   pip install poetry
   poetry shell
   poetry install
   ```
3. Create a `.env` file and add:
   ```plaintext
   DEV_URL = "your-dev-project-url"
   STAG_URL = "your-staging-project-url"
   ```
   - Rename the `chromedriver` to `local` if you want to run tests locally.

4. If you prefer not to use environment variables, add your references to the properties file:
   ```python
   class Properties:
       _ENV_VARIABLES = {
           "dev": ("DEV_URL", ""),
           "stag": ("STAG_URL", ""),
           # Add more environments and their default URLs as needed
       }
   ```
    
### Latest Drivers
- #### CLI util [util](utils/driver_management.md)
- #### [Chrome Drivers](https://googlechromelabs.github.io/chrome-for-testing/#stable)
- #### [Firefox Drivers](https://github.com/mozilla/geckodriver)
- You can download the latest version of the driver for macOS ARM64 using the `chromedriver.sh` script located in the `resources` folder.

### TODO

| Item                                                                                                        | Status                                                   |
|-------------------------------------------------------------------------------------------------------------|----------------------------------------------------------|
| 1. Drivers factory: local, remote, [Chrome, Firefox]                                                      | ![Status](https://img.shields.io/badge/DONE-brightgreen)      |
| 2. `pytest.ini` config: addopts, errors, markers                                                          | ![Status](https://img.shields.io/badge/DONE-brightgreen)      |
| 3. Environments: dev, stag, prod                                                                          | ![Status](https://img.shields.io/badge/DONE-brightgreen)      |
| 4. Secrets                                                                                                | ![Status](https://img.shields.io/badge/DONE-brightgreen)      |
| 5. Utilities: YAML reader, logger                                                                          | ![Status](https://img.shields.io/badge/DONE-brightgreen)      |
| 6. BasePage: wait strategy, base actions                                                                  | ![Status](https://img.shields.io/badge/DONE-brightgreen)      |
| 7. Properties: make properties helper                                                                       | ![Status](https://img.shields.io/badge/DONE-brightgreen)      |
| 8. CI: GitHub Actions: run tests, publish reports, take screenshots on failure (check test summary artifacts) | ![Status](https://img.shields.io/badge/DONE-brightgreen)      |

### CI: GitHub Actions

#### *Important Notes*

- When running CI locally, ensure your Git resources contain the correct Chrome driver with x86_64 architecture (unless using Selenium version 4.24.0 or higher).
- Go to **Repository Settings** -> **Secrets and Variables** -> **Actions** -> **Variables**, and add `DEV_URL`, `STAG_URL`.
- CI configuration is available for running tests on Ubuntu in `run_test_ubuntu.yaml`.
- ```
   jobs:
      selenium-tests:
        runs-on: macos-latest
        env:
          DEV_URL: ${{ vars.DEV_URL }}
          STAG_URL: ${{ vars.STAG_URL }}
   ```

### Local: Ruff Lint Configuration

The linting configuration defines rules that dictate the checks performed. Customize these rules to suit your project's coding style and requirements.

1. Create external tools to run linting.
2. Set the working directory to:
   ```plaintext
   $ProjectFileDir$
   ```
3. Specify the program:
   ```plaintext
   path to your ruff installed /bin/ruff 
   ```
4. Provide the arguments:
   ```plaintext
   $FilePathRelativeToProjectRoot$ --config .ruff.toml
   ```
### Secrets
To secure our passwords or sensitive data, we store them in an encrypted form. For this, we use the [secure-test-automation](https://pypi.org/project/secure-test-automation/) library.
implementation on framework side: utils/crypto.py
**Pay attention** The encryption key is stored in `/config/key.properties` (this file should be added to `.gitignore`) for local testing.  
For executing tests in remote environments (e.g., BrowserStack, Jenkins, etc.), we have integrated the Vault HashiCorp library.  

```python
@pytest.fixture
def get_password():
    secure = Secure()
    read = YAMLReader.read("data.yaml", to_simple_namespace=True)
    password = read.users.john.details.password
    return secure.decrypt_password(password)
```


### Demo tool https://demoqa.com/text-box
