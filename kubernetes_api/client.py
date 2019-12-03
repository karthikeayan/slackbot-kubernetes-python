from kubernetes import client, config
import configparser

config = configparser.ConfigParser()
config.read('./kubernetes_api/kubernetes.conf')

# Authenticate to Kubernetes API
aConfiguration = client.Configuration()
namespace = config['global']['namespace']
aToken = config['global']['kube_api_token']
aConfiguration.host = config['global']['kube_api_host']
aConfiguration.ssl_ca_cert= config['global']['kube_api_cacert_file']
aConfiguration.api_key = {"authorization": "Bearer " + aToken}
aConfiguration.verify_ssl=True
aApiClient = client.ApiClient(aConfiguration)

def core_client():
    return client.CoreV1Api(aApiClient)

def apps_client():
    return client.AppsV1Api(aApiClient)