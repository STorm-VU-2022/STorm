from django.core.exceptions import ValidationError


def validate_file_size_25mb(value):
    filesize = value.size

    if filesize > 26214400:
        raise ValidationError("You cannot upload file more than 25Mb")
    else:
        return value