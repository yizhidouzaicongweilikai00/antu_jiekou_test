export env=boe
pytest -sv --alluredir ./allure/json --clean-alluredir
allure generate ./allure/json -o ./allure/report --clean