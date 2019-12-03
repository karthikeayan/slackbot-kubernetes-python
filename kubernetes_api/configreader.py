import configparser

def read_config():
    config = configparser.ConfigParser()
    config.read('./kubernetes_api/kubernetes.conf')
    return config