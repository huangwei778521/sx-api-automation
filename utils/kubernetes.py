import os
from kubernetes import client, config

config_path = None


class Kubernetes:
    def __init__(self):
        self.load_config()
        self.k8s_core = client.CoreV1Api()

    def get_pods_list(self, namespace):
        pods_info_list = []

        pods_list = self.k8s_core.list_namespaced_pod(namespace)
        for pod in pods_list.items:
            pod_dict = {}
            pod_dict.update(name=pod.metadata.name, type=pod.metadata.owner_references[0].name,
                            status=pod.status.conditions[-1].type, namespace=pod.metadata.namespace)
            pods_info_list.append(pod_dict)
        return pods_info_list

    def delete_pod(self, pod_name, namespace):
        self.k8s_core.delete_namespaced_pod(name=pod_name, namespace=namespace)

    def get_pod_detail(self, pod_name, namespace):
        q_resp = self.k8s_core.read_namespaced_pod(name=pod_name, namespace=namespace)
        return {"name": q_resp.metadata.name, "status": q_resp.status.conditions[-1].type}

    def load_config(self):
        try:
            config.load_incluster_config()
        except config.ConfigException:
            try:
                config.load_kube_config()
            except config.ConfigException:
                raise Exception("Could not configure kubernetes python client")
