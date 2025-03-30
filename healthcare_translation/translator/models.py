from django.db import models

class Translation(models.Model):
    input_text = models.TextField()
    translated_text = models.TextField()
    input_language = models.CharField(max_length=10)
    output_language = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Translation from {self.input_language} to {self.output_language}"
