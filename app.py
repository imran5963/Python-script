from flask import Flask, request, jsonify
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)

def fill_and_submit_form(data):
    driver = webdriver.Chrome()
    url = 'https://example.com/form'
    driver.get(url)
    def fill_form(data):
        for field, value in data.items():
            try:
                
                element = driver.find_element(By.NAME, field) 
                element.send_keys(value)
            except Exception as e:
                print(f"Could not fill field {field}: {e}")
                return None

    fill_form(data)

    try:
        submit_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')  # Adjust selector
        submit_button.click()
    except Exception as e:
        print(f"Could not submit the form: {e}")
        driver.quit()
        return None

    try:
        lot_number_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.lot-number'))  # Adjust selector
        )
        lot_number = lot_number_element.text
    except Exception as e:
        print(f"Could not retrieve lot number: {e}")
        lot_number = None


    driver.quit()


    return lot_number


@app.route('/', methods=['POST'])
def submit_form():
    try:

        data = request.get_json()


        if not data:
            return jsonify({"error": "Invalid JSON data"}), 400


        lot_number = fill_and_submit_form(data)


        if lot_number:
            return jsonify({"lotNumber": lot_number}), 200
        else:
            return jsonify({"error": "Failed to retrieve lot number"}), 500
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "An error occurred"}), 500

if __name__ == '__main__':
    app.run()
