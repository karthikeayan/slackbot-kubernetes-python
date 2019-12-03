from kubernetes_api.configreader import read_config

def check_deployment_status(instance, name, namespace):
    ret = instance.read_namespaced_deployment_status(name, namespace)
    if ret.spec.replicas != ret.status.ready_replicas:
        return False
    else:
        return True

def check_statefulset_status(instance, name, namespace):
    ret = instance.read_namespaced_stateful_set_status(name, namespace)
    if ret.spec.replicas != ret.status.ready_replicas:
        return False
    else:
        return True

def database_status(instance):
    config = read_config()
    for db in config['databases']['deployment'].split(','):
        if not check_deployment_status(instance, db, config['global']['namespace']):
            yield "Kubernetes Deployemnt " + db + " is not running properly"
        else:
            yield "Kubernetes Deployemnt " + db + " is running properly"

    for db in read_config()['databases']['statefulset'].split(','):
        if not check_statefulset_status(instance, db, config['global']['namespace']):
            yield "Kubernetes Statefulset " + db + " is not running properly"
        else:
            yield "Kubernetes Statefulset " + db + " is running properly"
