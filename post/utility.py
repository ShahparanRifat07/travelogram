
def upload_dir_path(instance, filename):
    return 'uploads/{0}/{1}'.format(instance.user.pk, filename)