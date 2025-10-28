from django.shortcuts import render, redirect
from db_connection import execute_query, execute_dml, execute_single

# ==================== PÁGINA PRINCIPAL ====================

def index(request):
    """Dashboard principal con estadísticas"""
    stats = {
        'total_users': execute_single("SELECT COUNT(*) FROM USERS WHERE IS_DELETED = 'N'") or 0,
        'total_songs': execute_single("SELECT COUNT(*) FROM SONGS WHERE IS_DELETED = 'N'") or 0,
        'total_genres': execute_single("SELECT COUNT(*) FROM GENRES") or 0,
        'total_playlists': execute_single("SELECT COUNT(*) FROM PLAYLISTS WHERE IS_DELETED = 'N'") or 0,
    }

    # Canciones más recientes
    recent_songs = execute_query("""
        SELECT s.SONG_ID, s.TITLE, s.DURATION_SEC, s.CREATED_AT,
               u.USERNAME as AUTHOR_NAME, u.DISPLAY_NAME as AUTHOR_DISPLAY
        FROM SONGS s
        JOIN USERS u ON s.AUTHOR_ID = u.USER_ID
        WHERE s.IS_DELETED = 'N' AND s.IS_ACTIVE = 'Y'
        ORDER BY s.CREATED_AT DESC
        FETCH FIRST 5 ROWS ONLY
    """) or []

    return render(request, 'index.html', {
        'stats': stats,
        'recent_songs': recent_songs
    })


# ==================== USUARIOS ====================

def lista_usuarios(request):
    """Lista todos los usuarios activos"""
    query = """
        SELECT USER_ID, EMAIL, USERNAME, DISPLAY_NAME, USER_TYPE, 
               BIO, IS_ACTIVE, CREATED_AT
        FROM USERS
        WHERE IS_DELETED = 'N'
        ORDER BY CREATED_AT DESC
    """
    usuarios = execute_query(query) or []
    return render(request, 'usuarios/lista.html', {'usuarios': usuarios})


def crear_usuario(request):
    """Crear un nuevo usuario"""
    if request.method == 'POST':
        query = """
            INSERT INTO USERS (EMAIL, USERNAME, PASSWORD_HASH, DISPLAY_NAME, 
                              USER_TYPE, BIO, IS_ACTIVE, IS_DELETED)
            VALUES (:email, :username, :password_hash, :display_name, 
                    :user_type, :bio, 'Y', 'N')
        """
        params = {
            'email': request.POST.get('email'),
            'username': request.POST.get('username'),
            'password_hash': request.POST.get('password'),  # En producción: hashear
            'display_name': request.POST.get('display_name'),
            'user_type': request.POST.get('user_type'),
            'bio': request.POST.get('bio', '')
        }

        if execute_dml(query, params):
            return redirect('lista_usuarios')

    return render(request, 'usuarios/crear.html')


def detalle_usuario(request, user_id):
    """Ver detalles de un usuario"""
    query = """
        SELECT USER_ID, EMAIL, USERNAME, DISPLAY_NAME, USER_TYPE, 
               BIO, IS_ACTIVE, CREATED_AT
        FROM USERS
        WHERE USER_ID = :user_id AND IS_DELETED = 'N'
    """
    usuario = execute_query(query, {'user_id': user_id})

    if not usuario:
        return redirect('lista_usuarios')

    usuario = usuario[0]

    # Canciones del usuario
    canciones = execute_query("""
        SELECT SONG_ID, TITLE, DURATION_SEC, CREATED_AT
        FROM SONGS
        WHERE AUTHOR_ID = :user_id AND IS_DELETED = 'N'
        ORDER BY CREATED_AT DESC
    """, {'user_id': user_id}) or []

    # Seguidores y seguidos
    seguidores = execute_single("""
        SELECT COUNT(*) FROM FOLLOWS WHERE FOLLOWEE_ID = :user_id
    """, {'user_id': user_id}) or 0

    siguiendo = execute_single("""
        SELECT COUNT(*) FROM FOLLOWS WHERE FOLLOWER_ID = :user_id
    """, {'user_id': user_id}) or 0

    return render(request, 'usuarios/detalle.html', {
        'usuario': usuario,
        'canciones': canciones,
        'seguidores': seguidores,
        'siguiendo': siguiendo
    })


# ==================== CANCIONES ====================

def lista_canciones(request):
    """Lista todas las canciones activas"""
    query = """
        SELECT s.SONG_ID, s.TITLE, s.DURATION_SEC, s.DESCRIPTION,
               s.CREATED_AT, u.USERNAME as AUTHOR_NAME,
               u.DISPLAY_NAME as AUTHOR_DISPLAY
        FROM SONGS s
        JOIN USERS u ON s.AUTHOR_ID = u.USER_ID
        WHERE s.IS_DELETED = 'N' AND s.IS_ACTIVE = 'Y'
        ORDER BY s.CREATED_AT DESC
    """
    canciones = execute_query(query) or []
    return render(request, 'canciones/lista.html', {'canciones': canciones})


def crear_cancion(request):
    """Crear una nueva canción"""
    if request.method == 'POST':
        query = """
            INSERT INTO SONGS (TITLE, DURATION_SEC, AUTHOR_ID, COMPOSER_ID,
                              DESCRIPTION, IS_ACTIVE, IS_DELETED)
            VALUES (:title, :duration_sec, :author_id, :composer_id,
                    :description, 'Y', 'N')
        """
        params = {
            'title': request.POST.get('title'),
            'duration_sec': int(request.POST.get('duration_sec')),
            'author_id': int(request.POST.get('author_id')),
            'composer_id': int(request.POST.get('composer_id')) if request.POST.get('composer_id') else None,
            'description': request.POST.get('description', '')
        }

        if execute_dml(query, params):
            return redirect('lista_canciones')

    # Obtener lista de usuarios para el formulario
    usuarios = execute_query("""
        SELECT USER_ID, USERNAME, DISPLAY_NAME
        FROM USERS
        WHERE IS_DELETED = 'N' AND USER_TYPE IN ('artista', 'productor')
        ORDER BY USERNAME
    """) or []

    return render(request, 'canciones/crear.html', {'usuarios': usuarios})


def detalle_cancion(request, song_id):
    """Ver detalles de una canción"""
    query = """
        SELECT s.SONG_ID, s.TITLE, s.DURATION_SEC, s.DESCRIPTION,
               s.CREATED_AT, s.AUTHOR_ID,
               u.USERNAME as AUTHOR_NAME, u.DISPLAY_NAME as AUTHOR_DISPLAY
        FROM SONGS s
        JOIN USERS u ON s.AUTHOR_ID = u.USER_ID
        WHERE s.SONG_ID = :song_id AND s.IS_DELETED = 'N'
    """
    cancion = execute_query(query, {'song_id': song_id})

    if not cancion:
        return redirect('lista_canciones')

    cancion = cancion[0]

    # Géneros de la canción
    generos = execute_query("""
        SELECT g.GENRE_ID, g.NAME
        FROM SONG_GENRES sg
        JOIN GENRES g ON sg.GENRE_ID = g.GENRE_ID
        WHERE sg.SONG_ID = :song_id
    """, {'song_id': song_id}) or []

    # Comentarios
    comentarios = execute_query("""
        SELECT c.COMMENT_ID, c.BODY, c.CREATED_AT,
               u.USERNAME, u.DISPLAY_NAME
        FROM COMMENTS c
        JOIN USERS u ON c.USER_ID = u.USER_ID
        WHERE c.SONG_ID = :song_id AND c.IS_DELETED = 'N'
        ORDER BY c.CREATED_AT DESC
    """, {'song_id': song_id}) or []

    # Estadísticas
    total_likes = execute_single("""
        SELECT COUNT(*) FROM LIKES WHERE SONG_ID = :song_id
    """, {'song_id': song_id}) or 0

    total_plays = execute_single("""
        SELECT COUNT(*) FROM PLAYS WHERE SONG_ID = :song_id
    """, {'song_id': song_id}) or 0

    return render(request, 'canciones/detalle.html', {
        'cancion': cancion,
        'generos': generos,
        'comentarios': comentarios,
        'total_likes': total_likes,
        'total_plays': total_plays
    })


# ==================== GÉNEROS ====================

def lista_generos(request):
    """Lista todos los géneros"""
    query = """
        SELECT g.GENRE_ID, g.NAME, g.SLUG, g.CREATED_AT,
               COUNT(sg.SONG_ID) as SONG_COUNT
        FROM GENRES g
        LEFT JOIN SONG_GENRES sg ON g.GENRE_ID = sg.GENRE_ID
        GROUP BY g.GENRE_ID, g.NAME, g.SLUG, g.CREATED_AT
        ORDER BY g.NAME
    """
    generos = execute_query(query) or []
    return render(request, 'generos/lista.html', {'generos': generos})


def crear_genero(request):
    """Crear un nuevo género"""
    if request.method == 'POST':
        nombre = request.POST.get('name')
        slug = request.POST.get('slug', nombre.lower().replace(' ', '-'))

        query = """
            INSERT INTO GENRES (NAME, SLUG)
            VALUES (:name, :slug)
        """
        params = {'name': nombre, 'slug': slug}

        if execute_dml(query, params):
            return redirect('lista_generos')

    return render(request, 'generos/crear.html')


# ==================== PLAYLISTS ====================

def lista_playlists(request):
    """Lista todas las playlists públicas"""
    query = """
        SELECT p.PLAYLIST_ID, p.NAME, p.DESCRIPTION, p.CREATED_AT,
               u.USERNAME as OWNER_NAME, u.DISPLAY_NAME as OWNER_DISPLAY,
               COUNT(ps.SONG_ID) as SONG_COUNT
        FROM PLAYLISTS p
        JOIN USERS u ON p.OWNER_ID = u.USER_ID
        LEFT JOIN PLAYLIST_SONGS ps ON p.PLAYLIST_ID = ps.PLAYLIST_ID
        WHERE p.IS_DELETED = 'N' AND p.IS_PUBLIC = 'Y'
        GROUP BY p.PLAYLIST_ID, p.NAME, p.DESCRIPTION, p.CREATED_AT,
                 u.USERNAME, u.DISPLAY_NAME
        ORDER BY p.CREATED_AT DESC
    """
    playlists = execute_query(query) or []
    return render(request, 'playlists/lista.html', {'playlists': playlists})


def crear_playlist(request):
    """Crear una nueva playlist"""
    if request.method == 'POST':
        query = """
            INSERT INTO PLAYLISTS (OWNER_ID, NAME, DESCRIPTION, IS_PUBLIC, IS_DELETED)
            VALUES (:owner_id, :name, :description, :is_public, 'N')
        """
        params = {
            'owner_id': int(request.POST.get('owner_id')),
            'name': request.POST.get('name'),
            'description': request.POST.get('description', ''),
            'is_public': request.POST.get('is_public', 'Y')
        }

        if execute_dml(query, params):
            return redirect('lista_playlists')

    # Obtener usuarios para el formulario
    usuarios = execute_query("""
        SELECT USER_ID, USERNAME, DISPLAY_NAME
        FROM USERS
        WHERE IS_DELETED = 'N'
        ORDER BY USERNAME
    """) or []

    return render(request, 'playlists/crear.html', {'usuarios': usuarios})


def detalle_playlist(request, playlist_id):
    """Ver detalles de una playlist"""
    query = """
        SELECT p.PLAYLIST_ID, p.NAME, p.DESCRIPTION, p.IS_PUBLIC,
               p.CREATED_AT, u.USERNAME as OWNER_NAME,
               u.DISPLAY_NAME as OWNER_DISPLAY
        FROM PLAYLISTS p
        JOIN USERS u ON p.OWNER_ID = u.USER_ID
        WHERE p.PLAYLIST_ID = :playlist_id AND p.IS_DELETED = 'N'
    """
    playlist = execute_query(query, {'playlist_id': playlist_id})

    if not playlist:
        return redirect('lista_playlists')

    playlist = playlist[0]

    # Canciones de la playlist
    canciones = execute_query("""
        SELECT ps.POSITION, s.SONG_ID, s.TITLE, s.DURATION_SEC,
               u.USERNAME as AUTHOR_NAME
        FROM PLAYLIST_SONGS ps
        JOIN SONGS s ON ps.SONG_ID = s.SONG_ID
        JOIN USERS u ON s.AUTHOR_ID = u.USER_ID
        WHERE ps.PLAYLIST_ID = :playlist_id
        ORDER BY ps.POSITION
    """, {'playlist_id': playlist_id}) or []

    return render(request, 'playlists/detalle.html', {
        'playlist': playlist,
        'canciones': canciones
    })


# ==================== COMENTARIOS ====================

def lista_comentarios(request):
    """Lista todos los comentarios recientes"""
    query = """
        SELECT c.COMMENT_ID, c.BODY, c.CREATED_AT,
               u.USERNAME, u.DISPLAY_NAME,
               s.TITLE as SONG_TITLE, s.SONG_ID
        FROM COMMENTS c
        JOIN USERS u ON c.USER_ID = u.USER_ID
        JOIN SONGS s ON c.SONG_ID = s.SONG_ID
        WHERE c.IS_DELETED = 'N'
        ORDER BY c.CREATED_AT DESC
        FETCH FIRST 50 ROWS ONLY
    """
    comentarios = execute_query(query) or []
    return render(request, 'comentarios/lista.html', {'comentarios': comentarios})


# ==================== ESTADÍSTICAS ====================

def estadisticas(request):
    """Dashboard de estadísticas generales"""

    # Top 10 canciones por reproducciones
    top_songs = execute_query("""
        SELECT s.SONG_ID, s.TITLE, u.USERNAME as AUTHOR_NAME,
               COUNT(p.PLAY_ID) as PLAYS_COUNT
        FROM SONGS s
        JOIN USERS u ON s.AUTHOR_ID = u.USER_ID
        LEFT JOIN PLAYS p ON s.SONG_ID = p.SONG_ID
        WHERE s.IS_DELETED = 'N'
        GROUP BY s.SONG_ID, s.TITLE, u.USERNAME
        ORDER BY PLAYS_COUNT DESC
        FETCH FIRST 10 ROWS ONLY
    """) or []

    # Top 10 canciones por likes
    top_liked = execute_query("""
        SELECT s.SONG_ID, s.TITLE, u.USERNAME as AUTHOR_NAME,
               COUNT(l.USER_ID) as LIKES_COUNT
        FROM SONGS s
        JOIN USERS u ON s.AUTHOR_ID = u.USER_ID
        LEFT JOIN LIKES l ON s.SONG_ID = l.SONG_ID
        WHERE s.IS_DELETED = 'N'
        GROUP BY s.SONG_ID, s.TITLE, u.USERNAME
        ORDER BY LIKES_COUNT DESC
        FETCH FIRST 10 ROWS ONLY
    """) or []

    # Géneros más populares
    top_genres = execute_query("""
        SELECT g.NAME, COUNT(sg.SONG_ID) as SONG_COUNT
        FROM GENRES g
        LEFT JOIN SONG_GENRES sg ON g.GENRE_ID = sg.GENRE_ID
        GROUP BY g.NAME
        ORDER BY SONG_COUNT DESC
        FETCH FIRST 10 ROWS ONLY
    """) or []

    return render(request, 'estadisticas.html', {
        'top_songs': top_songs,
        'top_liked': top_liked,
        'top_genres': top_genres
    })
