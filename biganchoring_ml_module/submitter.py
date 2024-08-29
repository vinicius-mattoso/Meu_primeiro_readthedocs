# -*- coding: utf-8 -*-
import json
import requests
import io
import os

class Server_connection:
    '''
        Server_connection foi desenvolvido para facilitar os processos de conexões. 

    '''
    def __init__(self, node_name = "atn1b01n28", username = 'admin', password = 'admin123', port = '8008'):
        '''
        Summary:
            Initializes the Server_connection class with the required arguments.

        Args:
            node_name (str, required): The node that the server is running into atena02.

            username (str, required): The username required to make the login into the server.

            password (str, required): The password required to make the login into the server.
        '''
        self.node_name = node_name
        self.username = username
        self.password = password
        self.port = port

    def login(self):
            '''
            Summary:
                Make the request.post to perfome the login.

            Args:
                None

            Returns:
                Request response

            '''
            url = "http://{}:{}/auth/login".format(self.node_name, self.port)
            headers = {'accept': 'application/json',
                            'Content-Type': 'application/x-www-form-urlencoded'}
            data = {'username': self.username, 'password': self.password}
            response = requests.post(url, headers=headers, data=data, timeout=120)
            if response.status_code !=200:
                raise ValueError("Problem into the server login!")
            else:
                return response

class Submitter:
    def __init__(self, dataset_name=None, dataset_file ="test_data.zip", processor_file = "test_processor.zip",\
                 runner_location="atena02", execution_mode="mlflow", experiment_name="default_experiment",\
                 execution_command="mlflow run measurements_regression_training_right",\
                 instance_type="gpu", account="default_account", **model_params):
        '''
        Summary:
            Initializes the Submiter class with various parameters and optional model parameters.

        Args:
            dataset_name (str, required): The name of the dataset. Default is None.

            dataset_file (str, required): The name of the dataset file. Default is "test_data.zip".

            processor_file (str, required): The name of the processor file. Default is "test_processor.zip".

            runner_location (str, required): The location of the runner. Default is "atena02".

            execution_mode (str, required): The execution mode ("mlflow" or "no-mlflow"). Default is "mlflow".

            experiment_name (str, required): The name of the experiment. Default is "default_experiment".

            execution_command (str, required): The command that the user want to execute. Default is "mlflow run measurements_regression_training_right".

            instance_type (str, required): The type of instance to use. Default is "gpu".

            account (str, required): The account to use. Default is "default_account".
            
            **model_params: Additional model parameters as keyword arguments. These will be stored as model_params.
        '''
        
        self.dataset_name = dataset_name
        self.dataset_file = dataset_file
        self.processor_file = processor_file
        self.runner_location = runner_location
        self.execution_mode = execution_mode
        self.experiment_name = experiment_name
        self.execution_command = execution_command
        self.instance_type = instance_type
        self.account = account
        self.config_path = "configured_json_by_inputs.json"
        self.tracking_uri = "http://npab1420.petrobras.biz:5000/"
        self.default_image = "teste_sif_py310_miniforge3"

        # Initialize model_params as None
        self.model_params = None
        if model_params:
            # Initialize model_params with provided kwargs
            self.model_params = model_params

    
    def _validate_inputs(self):
        '''
        Summary:
            Validates the inputs provided to the Submiter class.

        Raises:
            ValueError: If any required input is missing or invalid.

        Returns:
            None
        '''
        errors = []
        
        if not self.dataset_name:
            errors.append("dataset_name is required.")
        if not isinstance(self.dataset_file, str) or not self.dataset_file:
            errors.append("dataset_file is required and must be a non-empty string.")
        if not isinstance(self.processor_file, str) or not self.processor_file:
            errors.append("processor_file is required and must be a non-empty string.")
        if not isinstance(self.runner_location, str) or not self.runner_location:
            errors.append("runner_location is required and must be a non-empty string.")
        if self.execution_mode not in ["mlflow", "no-mlflow"]:
            errors.append("execution_mode must be 'mlflow' or 'no-mlflow'.")
        if not self.experiment_name:
            errors.append("experiment_name is required.")
        if not self.execution_command:
            errors.append("execution_command is required.")
        if not self.instance_type:
            errors.append("instance_type is required.")
        if not self.account:
            errors.append("account is required.")
        
        if errors:
            raise ValueError("Input validation failed: " + "; ".join(errors))
        


    def _create_configuration_dict(self):
        '''
        Summary:
            Creates a dict configuration dictionary using the stored parameters and validated inputs.

        Raises:
            ValueError: If validation fails for any of the inputs.

        Returns:
            str: The dict configuration as a string.
        '''
        self._validate_inputs()
        
        # Initialize model_params as an empty dictionary if None
        model_params_dict = self.model_params if self.model_params is not None else {}

        # Construct the configuration dictionary
        config_dict = {
            "dataset_name": self.dataset_name,
            "dataset_file": self.dataset_file,
            "processor_file": self.processor_file,
            "model_params": model_params_dict,
            "runner_location": self.runner_location,
            "execution_mode": self.execution_mode,
            "experiment_name": self.experiment_name,
            "command": self.execution_command,
            "clusters": {
                self.runner_location: {
                    "infra_config": {
                        "instance_type": self.instance_type,
                        "image_name": self.default_image,
                        "account": self.account
                    }
                }
            },
            "backend_execution": {
                "mlflow": {
                    "execution_config": {
                        "execution_mode": self.execution_mode,
                        "tracking_uri": self.tracking_uri
                    }
                },
                "no-mlflow": {
                    "execution_config": {}
                }
            }
        }
        return config_dict

    def _prepare_json_file(self):
        '''
        Summary:
            Prepare the json and handle in memory to be used into the task submission proccess.

        Raises:
            ValueError: If validation of configuration_dict fails due to the type.

        Returns:
            _io.StringIO: json_file in memory.
        '''
        configuration_dict = self._create_configuration_dict()
        if type(configuration_dict) != dict:
                raise ValueError("Problem com a geração do json!")
        else:
            json_file = io.StringIO()
            json.dump(configuration_dict, json_file)
            json_file.seek(0)
            return json_file

    def submit_task(self):
        '''
        Summary:
            Perform the steps to make a submission of a task.

        Returns:
            Response of the submission request
        '''
        node_name = os.getenv('NODE_NAME')#"atn1b05n26"
        username = os.getenv('USER_NAME_AUTH')#'admin'
        password = os.getenv('PASSWORD_AUTH')#'admin123'
        port = os.getenv('PORT')#'8008'

        connection = Server_connection(node_name,username,password,port)
        connection_response = connection.login()
        auth = connection_response.json()      

        json_file = self._prepare_json_file()

        url = "http://{}:{}/new_task".format(node_name, port)
        headers = {'accept': 'application/json',
                'Authorization': "{} {}".format(auth['token_type'], auth['access_token'])}
        files = [("files", ("submiter_confs_mlflow.json", json_file, 'application/json'))]
        submission_response = requests.post(url, headers=headers, files=files, timeout=120)
        
        # print("submission_response.text:", submission_response.text)

        # Implement additional logic for task submission if needed
        print("Task submitted.")

        return submission_response
