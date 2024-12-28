import requests
import json

# Custom exception for when the link button is not pressed
class LinkButtonNotPressedError(Exception):
    pass

# Function to make a POST request to the REST API
def get_appkey(ip_address):
    url = f"http://{ip_address}/api"  # The endpoint of the REST API with dynamic IP address
    headers = {
        "Content-Type": "application/json"  # Specify the content type as JSON
    }
    data = {
        "devicetype": "my_hue_app"  # Data payload to be sent in the POST request
    }

    try:
        # Make a POST request with the specified URL, headers, and data
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Raise an exception for HTTP error responses (4xx or 5xx)
        response_data = response.json()  # Parse the response as JSON

        # Check if the response contains an error indicating the link button was not pressed
        if isinstance(response_data, list) and "error" in response_data[0]:
            error = response_data[0]["error"]
            if error.get("type") == 101 and "link button not pressed" in error.get("description", ""):
                raise LinkButtonNotPressedError("The link button on the device was not pressed.")

        # Check if the response contains a success with the username (app key)
        if isinstance(response_data, list) and "success" in response_data[0]:
            return response_data[0]["success"].get("username")  # Return the username (app key)

        return None  # Return None if no username is found in the response

    except LinkButtonNotPressedError as e:
        print(f"Appkey Error: {e}")
        return None

    except requests.exceptions.RequestException as e:
        # Handle exceptions that occur during the request, such as connection errors
        print(f"An error occurred: {e}")
        return None

# Example usage of the function
if __name__ == "__main__":
    ip_address = "192.168.178.47"  # Example IP address
    result = get_appkey(ip_address)  # Call the function with the IP address
    if result:
        # Print the app key if the request was successful
        print("App key (username):", result)
