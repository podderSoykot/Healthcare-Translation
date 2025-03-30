from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import openai
import os
from django.http import JsonResponse
from django.conf import settings
from gtts import gTTS
from .models import Translation

# Set your OpenAI API key
openai.api_key = "paste your api key"

class TranslateView(APIView):
    def post(self, request, *args, **kwargs):
        # Get data from POST request
        input_text = request.POST.get('input_text')
        input_language = request.POST.get('input_language', 'en')
        output_language = request.POST.get('output_language', 'es')

        if not input_text:
            return Response({"error": "Input text is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Use OpenAI's ChatCompletion model for translation
            translation_prompt = f"Translate the following text from {input_language} to {output_language}: {input_text}"

            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "user", "content": translation_prompt}
                ],
                temperature=0.3
            )

            translated_text = response.choices[0].message['content'].strip()

            # Optional: Enhance translation for medical accuracy (if required)
            enhancement_prompt = f"Enhance the following translation for medical accuracy:\n{translated_text}"

            enhancement_response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "user", "content": enhancement_prompt}
                ],
                temperature=0.3
            )

            enhanced_translation = enhancement_response.choices[0].message['content'].strip()

            # Generate speech for the translated text using gTTS
            tts = gTTS(text=enhanced_translation, lang=output_language, slow=False)

            # Define path for the audio file
            audio_dir = os.path.join(settings.MEDIA_ROOT, 'translated_audio')
            os.makedirs(audio_dir, exist_ok=True)
            audio_file_path = os.path.join(audio_dir, 'translated_audio.mp3')
            tts.save(audio_file_path)

            # Get the audio file URL to return in the response
            audio_file_url = os.path.join(settings.MEDIA_URL, 'translated_audio', 'translated_audio.mp3')

            # Return the translated text and audio file URL
            return JsonResponse({
                "translated_text": enhanced_translation,
                "audio_file_url": audio_file_url,
                "success": True
            })

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Render the main translation page
def translation_page(request):
    return render(request, 'transslator/translation_page.html')

# Render the translation history page
def history_page(request):
    translations = Translation.objects.all()
    return render(request, 'transslator/history_page.html', {'translations': translations})