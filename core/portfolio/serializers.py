from core.portfolio.factory.controller import OrderController, OrderProcessor
from rest_framework import serializers, exceptions
from .models import Order
from django.apps import apps

class OrderCreateSerializer(serializers.ModelSerializer):
    user = serializers.CharField(required=False)
    price = serializers.FloatField(required=False)
    status = serializers.CharField(read_only=True)
    qty = serializers.FloatField(read_only=True)
    setup = serializers.JSONField(required=False)
    created = serializers.DateTimeField(required=False, read_only=True)
    margin = serializers.IntegerField(required=False, default=1)
    currency = serializers.SerializerMethodField(read_only=True)
    exchange_rate = serializers.FloatField(read_only=True)
    user_currency = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = ["ticker", "price", "bot_id", "amount", "user","exchange_rate","currency",
                  "side", "status", "order_uid", "qty", "setup", "created","margin","user_currency"]

    def required_field(self, data):
        if self.initial_data["side"] == "sell":
            self.fields["bot_id"].required = False
            self.fields["amount"].required = False
            self.fields["ticker"].required = True
            self.fields["setup"].required = True
        else:
            self.fields["bot_id"].required = True
            self.fields["amount"].required = True
            self.fields["ticker"].required = True

        return super(OrderCreateSerializer, self).required_field(data)

    def create(self, validated_data):
        if not "user" in validated_data:
            request = self.context.get("request", None)
            if request:
                validated_data["user_id"] = request.user
                user = request.user
            else:
                error = {"detail": "missing user"}
                raise serializers.ValidationError(error)
        else:
            usermodel = apps.get_model("user", "User")
            try:
                user = usermodel.objects.get(id=validated_data.pop("user"))
            except usermodel.DoesNotExist:
                error = {"detail": "user not found with the given payload user"}
                raise exceptions.NotFound(error)
            validated_data["user_id"] = user
        
        controller = OrderController()
        processor = OrderProcessor[validated_data["side"]]
        
        return controller.process(processor(validated_data))

    def get_currency(self,obj) -> str:
        return obj.ticker.currency_code.currency_code

    def get_user_currency(self,obj)-> str:
        return obj.user_id.user_balance_user_id.currency_code.currency_code