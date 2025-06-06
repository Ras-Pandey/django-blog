from django import forms
from .models import Blog, Tag, Category

class BlogForm(forms.ModelForm):
    category_name = forms.CharField(
        required=True,
        help_text="Enter the category for this blog."
    )
    tag_names = forms.CharField(
        required=False,
        help_text="Add tags separated by commas."
    )

    class Meta:
        model = Blog
        fields = ['title', 'content', 'category_name', 'tag_names']

    def save(self, commit=True):
        # Don't call super().save() yet, because we need to set category and tags
        blog = super().save(commit=False)

        # Handle category
        category_name = self.cleaned_data.get('category_name')
        if category_name:
            category, created = Category.objects.get_or_create(name=category_name.strip())
            blog.category = category

        if commit:
            blog.save()

        # Handle tags
        tag_names = self.cleaned_data.get('tag_names')
        if tag_names:
            tag_list = [t.strip() for t in tag_names.split(',') if t.strip()]
            for tag_name in tag_list:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                blog.tags.add(tag)

        return blog