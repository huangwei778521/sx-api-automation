import logging
import uuid
import traceback
from gitlab.sz.sensetime.com.viper.engine_image_process_service.pb import \
    engine_image_process_service_pb2 as pb

from google.protobuf.json_format import MessageToDict

from utils.singleton import SenseXperiencePlatformConfig
from utils.k8s_cluster import K8sCluster
from kafka import KafkaConsumer


class Kafka:
    @staticmethod
    def consumer_kafka(server_info, topic='stream.features.face_24402', group_id=None, offset='latest'):
        """
        :param topic:
        :param group_id: 弃用
        :param offset: latest/earliest
        :param server_info:
        :return:
        """

        info_dir = K8sCluster().get_host_user_password(server_info)
        kafka_username = info_dir['kafka_admin_username']
        kafka_password = info_dir['kafka_admin_password']
        group_id = str(uuid.uuid4()) if group_id is None else group_id
        try:

            return KafkaConsumer(topic, group_id=group_id, bootstrap_servers=host, auto_offset_reset=offset,
                                 security_protocol='SASL_PLAINTEXT',
                                 sasl_mechanism='PLAIN',
                                 sasl_plain_username=kafka_username,
                                 sasl_plain_password=kafka_password,
                                 api_version=(0, 10)
                                 )
        except Exception as e:
            logging.info(str(e) + '\n' + str(traceback.format_exc()))
        return None

    @staticmethod
    def deserialize(msg, obj=None, _poll=False):
        """

        :param msg:
        :param obj:
        :param _poll:
        :return:
        """
        if obj is None:
            obj = pb.ObjectInfo()
        try:
            obj.Clear()
            if _poll:
                try:
                    obj.ParseFromString(list(msg.values())[0][0].value)
                except IndexError:
                    print(msg)
                    obj.ParseFromString(msg.value)
            else:
                obj.ParseFromString(msg.value)
            return MessageToDict(obj, including_default_value_fields=True, preserving_proto_field_name=True)
        except Exception as e:
            return None
            # logging.info(f"obj:{obj}")
            # raise Exception(f"反序列化Kafka msg失败e:{e}")
