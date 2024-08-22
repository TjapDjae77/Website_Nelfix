from PIL import Image
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from film.models import Film
from io import BytesIO
from rest_framework import serializers
from user.models import Profile

class FilmCreateSerializer(serializers.ModelSerializer):
    video = serializers.FileField(required=True)
    cover_image = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = Film
        fields = ['id', 'title', 'description', 'director', 'release_year', 'genre', 'price', 'duration', 'video', 'cover_image', 'created_at', 'updated_at']

    # def validate_cover_image(self, value):
    #     if value:
    #         try:
    #             # Cek apakah file adalah gambar dengan mencoba membukanya dengan Pillow
    #             img = Image.open(value)
    #             img.verify()  # Memverifikasi file apakah benar-benar gambar
    #         except (IOError, SyntaxError) as e:
    #             raise serializers.ValidationError("Uploaded file is not a valid image.")
    #     return value

    def create(self, validated_data):
        # Konversi duration dari detik menjadi string HH:MM:SS
        duration = validated_data.get('duration')
        if isinstance(duration, str):
            hours, remainder = divmod(int(duration), 3600)
            minutes, seconds = divmod(remainder, 60)
            validated_data['duration'] = f"{hours:02}:{minutes:02}:{seconds:02}"
        
        # Buat instance Film dengan data yang telah divalidasi
        film = Film.objects.create(**validated_data)
        print(validated_data)
        return film

    def to_representation(self, instance):
        # Representasikan data dalam format yang sesuai dengan kontrak API
        representation = super().to_representation(instance)
        representation['id'] = str(instance.id)  # Pastikan ID dalam format string
        representation['video_url'] = instance.video.url if instance.video else None
        representation['cover_image_url'] = instance.cover_image.url if instance.cover_image else None

        representation.pop('video', None)
        representation.pop('cover_image', None)

        return representation

class FilmListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = ['id', 'title', 'director', 'release_year', 'genre', 'price', 'duration', 'cover_image', 'created_at', 'updated_at']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['id'] = str(representation['id'])
        representation['cover_image_url'] = representation.pop('cover_image')
        representation['duration'] = self.convert_duration_to_number(representation['duration'])
        return representation

    def convert_duration_to_number(self, duration):
        if duration:
            parts = duration.split(':')
            hours = int(parts[0])
            minutes = int(parts[1])
            seconds = int(parts[2])
            return hours * 3600 + minutes * 60 + seconds
        return 0

class FilmDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = ['id', 'title', 'description', 'director', 'release_year', 'genre', 'price', 'duration', 'video', 'cover_image', 'created_at', 'updated_at']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['id'] = str(representation['id'])
        representation['video_url'] = representation.pop('video')
        representation['cover_image_url'] = representation.pop('cover_image')
        representation['duration'] = self.convert_duration_to_number(representation['duration'])
        return representation

    def convert_duration_to_number(self, duration):
        if duration:
            parts = duration.split(':')
            hours = int(parts[0])
            minutes = int(parts[1])
            seconds = int(parts[2])
            return hours * 3600 + minutes * 60 + seconds
        return 0

class FilmUpdateSerializer(serializers.ModelSerializer):
    video = serializers.FileField(required=False, allow_null=True)
    cover_image = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = Film
        fields = ['id', 'title', 'description', 'director', 'release_year', 'genre', 'price', 'duration', 'video', 'cover_image', 'created_at', 'updated_at']

    def update(self, instance, validated_data):
        # Update fields with new values
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.director = validated_data.get('director', instance.director)
        instance.release_year = validated_data.get('release_year', instance.release_year)
        instance.genre = validated_data.get('genre', instance.genre)
        instance.price = validated_data.get('price', instance.price)
        instance.duration = validated_data.get('duration', instance.duration)
        
        # Handle video and cover_image updates
        new_video = validated_data.get('video', None)
        new_cover_image = validated_data.get('cover_image', None)

        # Handle video file
        if new_video:
            if instance.video:
                # Delete old video file
                if default_storage.exists(instance.video.name):
                    default_storage.delete(instance.video.name)
            instance.video = new_video

        # Handle cover image file
        if new_cover_image:
            if instance.cover_image:
                # Delete old cover image file
                if default_storage.exists(instance.cover_image.name):
                    default_storage.delete(instance.cover_image.name)
            instance.cover_image = new_cover_image

        instance.save()
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['id'] = str(instance.id)  # Pastikan ID dalam format string
        representation['video_url'] = instance.video.url if instance.video else None
        representation['cover_image_url'] = instance.cover_image.url if instance.cover_image else None

        representation.pop('video', None)
        representation.pop('cover_image', None)

        return representation
    
class FilmDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = ['id', 'title', 'description', 'director', 'release_year', 'genre', 'video', 'created_at', 'updated_at']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['id'] = str(instance.id)
        representation['genre'] = instance.genre
        representation['video_url'] = instance.video.url if instance.video else None

        representation.pop('video', None)
        
        return representation
 
class AdminLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user and user.is_staff:
            return user
        raise serializers.ValidationError("Invalid credentials or not an admin")
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model = Profile
        fields = ['id', 'user', 'balance', 'films']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ['id', 'user', 'balance']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user_data = representation.pop('user')
        return {
            'id': str(user_data['id']),
            'username': user_data['username'],
            'email': user_data['email'],
            'balance': representation['balance']
        }