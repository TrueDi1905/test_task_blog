from django.core.mail import send_mail


def send(user, author):
    send_mail(
        'Новый пост',
        f'Новый пост от - {author},',
        'tinderonline12345@gmail.com',
        [user.email],
        fail_silently=False,
    )
