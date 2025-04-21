# from rest_framework import serializers


# class NumberStatusRequestSerializer(serializers.Serializer):
#     number = serializers.CharField()
#     service = serializers.CharField()


# class NumberStatusResponseSerializer(serializers.Serializer):
#     number = serializers.CharField()
#     status = serializers.CharField()

#     def to_representation(self, instance):
#         return {
#             "number": str(instance["number"]),
#             "status": instance["status"],
#         }


# # agent task request_response
# class NumberItemSerializer(serializers.Serializer):
#     number = serializers.IntegerField()


# class AgentTaskRequestSerializer(serializers.Serializer):
#     task_id = serializers.IntegerField()
#     numbers = serializers.ListField(child=NumberItemSerializer())


# # agent task result_response
# class ResultItemSerializer(serializers.Serializer):
#     number = serializers.IntegerField(required=True)
#     status = serializers.IntegerField(required=True)


# class AgentTaskResultSerializer(serializers.Serializer):
#     agent_id = serializers.IntegerField(required=True)
#     service_code = serializers.CharField(required=True)
#     task_id = serializers.IntegerField(required=True)
#     results = serializers.ListField(child=ResultItemSerializer())
