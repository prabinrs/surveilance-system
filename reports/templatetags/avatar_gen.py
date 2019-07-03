from django import template
import hashlib
register = template.Library()

@register.simple_tag
def avatar_url(email):
    initial_url = "https://s.gravatar.com/avatar/"
    email_hash = hashlib.md5(email.encode("utf-8")).hexdigest()

    return initial_url+email_hash