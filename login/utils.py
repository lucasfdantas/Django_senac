def verificar_grupo(user, nome_grupo):
    if not user.is_authenticated:
        return False
    # Superusuário tem passe livre ou herda papel administrativo
    if user.is_superuser and nome_grupo == 'administradores':
        return True
    return user.groups.filter(name=nome_grupo).exists()