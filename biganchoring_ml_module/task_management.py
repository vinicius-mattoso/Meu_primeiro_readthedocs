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
        '''
        Cancela a tarefa com o task_id fornecido.
        '''
        # Placeholder for logic to cancel a task
        print("A tarefa {} foi cancelada.".format(self.task_id))   

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
            print("Tarefa cancelada com sucesso!")
        else:
            print("Erro ao cancelar a tarefa:", response.status_code, response.text)
            raise ValueError("Falha ao cancelar a tarefa: {}".format(response.status_code))

        return response
        

    def get_task_status(self):
        '''
        Resumo:
            Recupera o status de um task da API usando o ID da task.
            A função conecta-se ao servidor utilizando credenciais de autenticação
            armazenadas em variáveis de ambiente, envia uma solicitação GET para recuperar 
            o status da task e retorna a resposta da API.

        Exceções:
            ValueError: Se a resposta da API indicar uma falha na recuperação do status da task, 
            como um código de status inesperado.

        Retorna:
            requests.models.Response: O objeto de resposta HTTP contendo as informações do status da task.
        '''
        # Placeholder for logic to get task information
        print("Obtendo informações para o ID task_id: {}.".format(self.task_id))

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
            print("Erro ao obter o status da task:", response.status_code, response.text)
            raise ValueError("Falha ao recuperar o status da task: {}".format(response.status_code))

        return response
    
    def get_task_run_id(self):
        '''
        Resumo:
            Recupera o ID de execução de uma tarefa (task) da API usando o task ID.
            A função conecta-se ao servidor utilizando credenciais de autenticação
            armazenadas em variáveis de ambiente, envia uma solicitação GET para recuperar
            o ID de execução a partir do MLFLOW e retorna a resposta da API.

        Exceções:
            ValueError: Se a resposta da API indicar uma falha na recuperação do ID de execução da tarefa,
            como um código de status inesperado.

        Retorna:
            requests.models.Response: O objeto de resposta HTTP contendo as informações do ID de execução da tarefa.
        '''
        # Placeholder for logic to get task information
        print("Obtendo informações para o ID task_id: {}.".format(self.task_id))

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
            print("Erro ao obter o ID de execução da tarefa:", response.status_code, response.text)
            raise ValueError("Falha ao recuperar o ID de execução da tarefa: {}".format(response.status_code))

        return response





