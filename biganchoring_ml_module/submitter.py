# -*- coding: utf-8 -*-
import json
import requests
import io
import os

class Submitter:
    def __init__(self, dataset_name=None, dataset_file =None, processor_file = None,\
                 runner_location="atena02", execution_mode="mlflow", experiment_name="default_experiment",\
                 execution_command="mlflow run project", tracking_uri = None,\
                 instance_type="gpu", account="default_account", **model_params):
        '''
        Resumo:
            Inicializa a classe Submiter com vários parâmetros e parâmetros opcionais de modelo.

        Parâmetros:
            dataset_name (str, obrigatório): O nome do dataset. Padrão é None.

            dataset_file (str, obrigatório): O nome do arquivo do dataset. Padrão é None.

            processor_file (str, obrigatório): O nome do arquivo do processador. Padrão é None.

            runner_location (str, obrigatório): A localização do runner. Padrão é "atena02".

            execution_mode (str, obrigatório): O modo de execução ("mlflow" ou "no-mlflow"). Padrão é "mlflow".

            experiment_name (str, obrigatório): O nome do experimento. Padrão é "default_experiment".

            execution_command (str, obrigatório): O comando que o usuário deseja executar. Padrão é "mlflow run project".

            tracking_uri (str, obrigatório): O URI onde vai ocorrer o tracking do MLFlow. Padrão é None.

            instance_type (str, obrigatório): O tipo de instância a ser utilizada. Padrão é "gpu".

            account (str, obrigatório): A conta a ser utilizada. Padrão é "default_account".
            
            **model_params: Parâmetros adicionais do modelo como argumentos de palavra-chave. Estes serão armazenados como model_params.
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
        self.tracking_uri = tracking_uri
        self.default_image = "teste_sif_py310_miniforge3"

        # Initialize model_params as None
        self.model_params = None
        if model_params:
            # Initialize model_params with provided kwargs
            self.model_params = model_params

    
    def _validate_inputs(self):
        '''
        Resumo:
            Valida as entradas fornecidas para a classe Submiter.

        Exceções:
            ValueError: Se qualquer entrada obrigatória estiver ausente ou for inválida.

        Retorna:
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
        Resumo:
            Cria um dicionário de configuração usando os parâmetros armazenados e as entradas validadas.

        Exceções:
            ValueError: Se a validação falhar para qualquer uma das entradas.

        Retorna:
            str: O dicionário de configuração como uma string.
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
        Resumo:
            Prepara o JSON e o armazena na memória para ser utilizado no processo de submissão da tarefa.

        Exceções:
            ValueError: Se a validação de configuration_dict falhar devido ao tipo.

        Retorna:
            _io.StringIO: json_file na memória.
        '''
        configuration_dict = self._create_configuration_dict()
        if type(configuration_dict) != dict:
                raise ValueError("Problema com a geração do json!")
        else:
            json_file = io.StringIO()
            json.dump(configuration_dict, json_file)
            json_file.seek(0)
            return json_file

    def submit_task(self):
        '''
        Resumo:
            Realiza os passos necessários para fazer a submissão de uma tarefa.

        Retorna:
            Resposta da solicitação de submissão.
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
        
        print("Task submetida.")

        return submission_response
    
class Server_connection:
    '''
    Server_connection foi desenvolvido para facilitar os processos de conexões.
    '''
    def __init__(self, node_name = "atn1b01n28", username = None, password = None, port = None):
        '''
        Resumo:
            Inicializa a classe Server_connection com os argumentos necessários.

        Parâmetros:
            node_name (str, obrigatório): O nó onde o servidor está rodando em atena02.

            username (str, obrigatório): O nome de usuário necessário para fazer login no servidor.

            password (str, obrigatório): A senha necessária para fazer login no servidor.

            port (str, obrigatório): A porta necessária para fazer login no servidor.
        '''
        self.node_name = node_name
        self.username = username
        self.password = password
        self.port = port

    def login(self):
            '''
            Resumo:
                Realiza a solicitação `POST` para efetuar o login.

            Parâmetros:
                Nenhum

            Retorna:
                Resposta da solicitação de login.
            '''
            url = "http://{}:{}/auth/login".format(self.node_name, self.port)
            headers = {'accept': 'application/json',
                            'Content-Type': 'application/x-www-form-urlencoded'}
            data = {'username': self.username, 'password': self.password}
            response = requests.post(url, headers=headers, data=data, timeout=120)
            if response.status_code !=200:
                raise ValueError("Problema no login junto ao servidor!")
            else:
                return response