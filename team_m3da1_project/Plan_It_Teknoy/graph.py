import json
import configparser
from configparser import SectionProxy
from azure.identity import DeviceCodeCredential, ClientSecretCredential
from msgraph.core import GraphClient

class Graph:
	settings: SectionProxy
	device_code_credential: DeviceCodeCredential
	user_client: GraphClient
	client_credential: ClientSecretCredential
	app_client: GraphClient

	def __init__(self, config: SectionProxy):
		self.settings = config
		client_id = self.settings['clientId']
		tenant_id = self.settings['authTenant']
		graph_scopes = self.settings['graphUserScopes'].split(' ')

		self.device_code_credential = DeviceCodeCredential(client_id, tenant_id = tenant_id)
		self.user_client = GraphClient(credential=self.device_code_credential, scopes=graph_scopes)

	def get_user_token(self):
		graph_scopes = self.settings['graphUserScopes']
		access_token = self.device_code_credential.get_token(graph_scopes)
		return access_token.token
	
	def get_user(self):
		endpoint = '/me'
		# Only request specific properties
		select = 'displayName,mail,userPrincipalName,id'
		request_url = f'{endpoint}?$select={select}'

		user_response = self.user_client.get(request_url)
		return user_response.json()


# def display_access_token(graph: Graph):
# 	token = graph.get_user_token()
# 	print('User token:', token, '\n')

# def greet_user(graph: Graph):
# 	user = graph.get_user()
# 	print('Hello,', user['displayName'])
# 	# For Work/school accounts, email is in mail property
# 	# Personal accounts, email is in userPrincipalName
# 	print('Email:', user['mail'] or user['userPrincipalName'], '\n')



	