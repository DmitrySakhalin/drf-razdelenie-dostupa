from django.contrib.auth.models import User
from rest_framework import serializers
from advertisements.models import Advertisement


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', )

    def create(self, validated_data):
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        user = self.context["request"].user
        open_ads_count = Advertisement.objects.filter(creator=user, status='OPEN').count()
        if self.instance and self.instance.status == 'OPEN':
            if data.get('status') == 'OPEN':
                pass
            else:
                return data
        if data.get('status') == 'OPEN' and open_ads_count >= 10:
            raise serializers.ValidationError('У пользователя не может быть более 10 открытых объявлений.')
        return data