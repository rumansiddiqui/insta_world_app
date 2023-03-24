import os


def user_upload_path(instance, filename):

    username = instance.user.username
    ext = filename.split('.')[-1]
    if ext in ['jpg', 'jpeg', 'png', 'gif']:
        folder = 'images'
    elif ext in ['mp4', 'avi', 'mov', 'mkv']:
        folder = 'videos'
    else:
        raise ValueError('Unsupported file format')
    return os.path.join(username, folder, filename)
