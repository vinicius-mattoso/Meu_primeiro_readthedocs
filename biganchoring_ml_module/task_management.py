import requests
from biganchoring_ml_module.submitter import Server_connection
import os


class TaskHandler:
    def __init__(self, task_id):
        self.task_id = task_id
        # Retrieve environment variables for API connection
        self.node_name = os.getenv('NODE_NAME')
        self.username = os.getenv('USER_NAME_AUTH')
        self.password = os.getenv('PASSWORD_AUTH')
        self.port = os.getenv('PORT')
        self.connection = Server_connection(self.node_name, self.username, self.password, self.port)
    
    def cancel_task(self):
        """
        Cancels the task with the given task_id.
        """
        # Placeholder for logic to cancel a task
        print("Task {} has been canceled.".format(self.task_id))   

        # Establish connection to the server
        connection_response = self.connection.login()
        auth = connection_response.json()

        # Prepare the URL and headers for the GET request
        url = "http://{}:{}/cancel_task/{}".format(self.node_name, self.port, self.task_id)
        headers = {
            'accept': 'application/json',
            'Authorization': "{} {}".format(auth['token_type'], auth['access_token'])
        }

        # Send the post request to cancel the job
        response = requests.post(url, headers=headers)

        # Handle the response
        if response.status_code == 200:
            print("Status obtido com sucesso!")
        else:
            print("Erro ao cancelar o job:", response.status_code, response.text)
            raise ValueError("Failed to cancel the job: {}".format(response.status_code))

        return response
        

    def get_job_status(self):
        '''
        Summary:
            Retrieves the status of a job from the API using the job ID. 
            The function connects to the server using authentication credentials 
            stored in environment variables, sends a GET request to retrieve the 
            job status, and returns the API response.

        Args:
            task_id (int): The unique identifier for the job whose status is to be retrieved.

        Raises:
            ValueError: If the API response indicates a failure to retrieve the job status, such as an unexpected status code.

        Returns:
            requests.models.Response: The HTTP response object containing the job status information.
        '''
        # Placeholder for logic to get task information
        print("Getting information for the task_id ID: {}.".format(self.task_id))

        # Establish connection to the server
        connection_response = self.connection.login()
        auth = connection_response.json()

        # Prepare the URL and headers for the GET request
        url = "http://{}:{}/job_status/{}".format(self.node_name, self.port, self.task_id)
        headers = {
            'accept': 'application/json',
            'Authorization': "{} {}".format(auth['token_type'], auth['access_token'])
        }

        # Send the GET request to retrieve job status
        response = requests.get(url, headers=headers)

        # Handle the response
        if response.status_code == 200:
            print("Status obtido com sucesso!")
        else:
            print("Erro ao obter o status do job:", response.status_code, response.text)
            raise ValueError("Failed to retrieve job status: {}".format(response.status_code))

        return response
    
    def get_job_run_id(self):
        '''
        Summary:
            Retrieves the status of a job from the API using the job ID. 
            The function connects to the server using authentication credentials 
            stored in environment variables, sends a GET request to retrieve the 
            run id from the MLFLOW, and returns the API response.

        Args:
            task_id (int): The unique identifier for the job whose status is to be retrieved.

        Raises:
            ValueError: If the API response indicates a failure to retrieve the job status, such as an unexpected status code.

        Returns:
            requests.models.Response: The HTTP response object containing the job status information.
        '''
        # Placeholder for logic to get task information
        print("Getting information for the task_id ID: {}.".format(self.task_id))

        # Establish connection to the server
        connection_response = self.connection.login()
        auth = connection_response.json()

        # Prepare the URL and headers for the GET request
        url = "http://{}:{}/run_id/{}".format(self.node_name, self.port, self.task_id)
        headers = {
            'accept': 'application/json',
            'Authorization': "{} {}".format(auth['token_type'], auth['access_token'])
        }

        # Send the GET request to retrieve job status
        response = requests.get(url, headers=headers)

        # Handle the response
        if response.status_code == 200:
            print("Status obtido com sucesso!")
        else:
            print("Erro ao obter o run id do job:", response.status_code, response.text)
            raise ValueError("Failed to retrieve job run id: {}".format(response.status_code))

        return response





