from kubernetes_api.configreader import read_config
from kubernetes.stream import stream
import sys, time

def get_all_pods(instance):
    config = read_config()
    return instance.list_namespaced_pod(config['global']['namespace'])

def get_pods_with_pvc(instance):
    pods_with_pvc = []
    for pod in get_all_pods(instance).items:
        if pod.status.phase == 'Running':
            for vol in pod.spec.volumes:
                if vol.persistent_volume_claim:
                    for container in pod.spec.containers:
                        for mount in container.volume_mounts:
                            if vol.name == mount.name:
                                pods_with_pvc.append({'name': pod.metadata.name,
                                                    'container_name': container.name})
                                                    #   'mount': mount.mount_path})

    return get_unique_pod_containers(pods_with_pvc)

def get_unique_pod_containers(pods):
    return list({v['name']:v for v in pods}.values())

def pod_execute(instance):
    sizes = []
    config = read_config()
    namespace = config['global']['namespace']
    command = ["/bin/sh", "-c", "df -hT -P | grep -v tmpfs | grep -v devtmpfs | awk 'NF{NF--};1' | uniq | awk '{print $1,$6}' | tail -n+2"]
    pods = get_pods_with_pvc(instance)
    for pod in pods:
        print(pod)
        res = stream(instance.connect_get_namespaced_pod_exec,
                    pod['name'],
                    namespace,
                    command=command,
                    container=pod['container_name'],
                    stderr=True, stdin=False,
                    stdout=True, tty=False)
        mounts = res.split("\n")
        for mount in filter(None, mounts):
            mount_name = mount.split(" ")[0]
            mount_percentage = mount.split(" ")[1]
            if int(mount_percentage.split("%")[0]) > 80:
                sizes.append({"pod": pod['name'], "mount": mount_name})
        # time.sleep(1)
    return sizes

def check_pvc_storage(instance):
    pods = pod_execute(instance)
    pods_count = len(pods)
    nfs_pods = []
    for pod in pods:
        if 'nfs' in pod['mount']:
            nfs_pods.append(pod)
    if len(nfs_pods) == 0:
        return str(pods_count) + " pods crossed 80% limit, but all of them or container mounts, none of them are external mounts"
    else:
        return nfs_pods