from django import forms
from .models import Course, Lesson, Rating, LessonComment

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['cname', 'description', 'category', 'image', 'fee', 'duration', 'level', 'status', 'requirements', 'what_you_will_learn']
        widgets = {
            'cname': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'fee': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'duration': forms.TextInput(attrs={'class': 'form-control'}),
            'level': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'requirements': forms.Textarea(attrs={'class': 'form-control'}),
            'what_you_will_learn': forms.Textarea(attrs={'class': 'form-control'})
        }

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'description', 'content', 'type', 'duration', 'video_url', 'video_file', 'order']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter lesson title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter a brief description of the lesson',
                'rows': 3
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter detailed lesson content (optional)',
                'rows': 5
            }),
            'type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'duration': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 30 minutes or 00:30:00'
            }),
            'video_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Optional: Enter video URL (YouTube, Vimeo, etc.)'
            }),
            'video_file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'video/mp4,video/webm'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter lesson order number'
            })
        }
        labels = {
            'title': 'Lesson Title',
            'description': 'Brief Description',
            'content': 'Detailed Content (Optional)',
            'type': 'Lesson Type',
            'duration': 'Duration',
            'video_url': 'Video URL (Optional)',
            'video_file': 'Video File (Optional)',
            'order': 'Lesson Order'
        }
        help_texts = {
            'description': 'A short overview of what this lesson covers',
            'content': 'The full lesson content, instructions, or details',
            'type': 'Select the type of lesson',
            'duration': 'How long this lesson takes to complete',
            'video_url': 'Enter a URL for external video (YouTube, Vimeo, etc.)',
            'video_file': 'Upload a video file (MP4 or WebM)',
            'order': 'The order in which this lesson appears in the course'
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating', 'review']
        widgets = {
            'rating': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 5
            }),
            'review': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write your review...'
            })
        }

class LessonCommentForm(forms.ModelForm):
    class Meta:
        model = LessonComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Add a comment...'
            })
        } 