# 🚀 Vistas Optimizadas de Oracle - Guía de Uso

## 📋 Resumen

Este proyecto ahora incluye **4 vistas optimizadas de Oracle** que mejoran el rendimiento al pre-calcular datos complejos con múltiples JOINs.

## 🎯 Vistas Disponibles

### 1. **vw_songs_complete** - Canciones Completas
- **URL**: `/vistas/canciones/`
- **Vista Django**: `canciones_completas`
- **Descripción**: Información completa de canciones con géneros, likes y plays pre-calculados
- **JOINs**: 4 (users autor, users compositor, géneros, likes, plays)
- **Ventaja**: Evita hacer múltiples consultas para obtener estadísticas

**Columnas principales**:
- `SONG_ID`, `TITLE`, `DURATION_SEC`, `DESCRIPTION`
- `AUTHOR_USERNAME`, `AUTHOR_DISPLAY_NAME`
- `COMPOSER_USERNAME`, `COMPOSER_DISPLAY_NAME`
- `GENRES` (concatenados con comas)
- `TOTAL_LIKES`, `TOTAL_PLAYS`

### 2. **vw_public_playlists** - Playlists Públicas
- **URL**: `/vistas/playlists/`
- **Vista Django**: `playlists_publicas`
- **Descripción**: Solo playlists públicas con información del propietario
- **JOINs**: 2 (users, playlist_songs)
- **Ventaja**: Filtra automáticamente solo playlists públicas

**Columnas principales**:
- `PLAYLIST_ID`, `PLAYLIST_NAME`, `DESCRIPTION`
- `USER_ID`, `USERNAME`, `DISPLAY_NAME`
- `TOTAL_SONGS`
- `CREATED_AT`, `UPDATED_AT`

### 3. **vw_top_songs_ranking** - Ranking de Popularidad
- **URL**: `/vistas/ranking/`
- **Vista Django**: `ranking_canciones`
- **Descripción**: Top 50 canciones ordenadas por score de popularidad
- **JOINs**: 4 (users, plays, likes, comments)
- **Ventaja**: Cálculo automático de popularidad con fórmula ponderada

**Fórmula de popularidad**:
```
(Plays × 0.5) + (Likes × 2) + (Comentarios × 1.5)
```

**Columnas principales**:
- `SONG_ID`, `TITLE`, `AUTHOR_USERNAME`
- `TOTAL_PLAYS`, `TOTAL_LIKES`, `TOTAL_COMMENTS`
- `POPULARITY_SCORE` (calculado)

### 4. **vw_user_activity_profile** - Perfiles con Estadísticas
- **URL**: `/vistas/perfiles/`
- **Vista Django**: `perfiles_usuarios`
- **Descripción**: Perfiles de usuarios con todas sus estadísticas
- **JOINs**: 6 (songs, likes, plays, playlists, follows x2)
- **Ventaja**: Dashboard completo de actividad del usuario en una sola consulta

**Columnas principales**:
- `USER_ID`, `USERNAME`, `DISPLAY_NAME`, `USER_TYPE`, `BIO`
- `SONGS_CREATED`, `SONGS_LIKED`, `TOTAL_PLAYS`
- `PLAYLISTS_CREATED`
- `FOLLOWING_COUNT`, `FOLLOWERS_COUNT`

**URL adicional**: `/vistas/perfiles/<user_id>/` para ver el detalle de un usuario específico

## 🔧 Instalación

### 1. Crear las vistas en Oracle

Ejecuta el archivo SQL en tu contenedor de Docker:

```bash
# Opción 1: Desde el contenedor
docker exec -it oracle_xe_dev sqlplus riffly_m/root123@XE @/ruta/crear_vistas_oracle.sql

# Opción 2: Copiar el archivo y ejecutar
docker cp crear_vistas_oracle.sql oracle_xe_dev:/tmp/
docker exec -it oracle_xe_dev sqlplus riffly_m/root123@XE @/tmp/crear_vistas_oracle.sql

# Opción 3: Usar SQL Developer o cualquier cliente Oracle
# Conectar como riffly_m y ejecutar el contenido de crear_vistas_oracle.sql
```

### 2. Verificar que las vistas existen

```sql
-- En SQL*Plus o SQL Developer
SELECT view_name FROM user_views WHERE view_name LIKE 'VW_%';

-- Debe mostrar:
-- VW_SONGS_COMPLETE
-- VW_PUBLIC_PLAYLISTS
-- VW_TOP_SONGS_RANKING
-- VW_USER_ACTIVITY_PROFILE
```

### 3. Probar las vistas

```sql
-- Contar registros en cada vista
SELECT 'vw_songs_complete' AS vista, COUNT(*) AS registros FROM vw_songs_complete
UNION ALL
SELECT 'vw_public_playlists' AS vista, COUNT(*) AS registros FROM vw_public_playlists
UNION ALL
SELECT 'vw_top_songs_ranking' AS vista, COUNT(*) AS registros FROM vw_top_songs_ranking
UNION ALL
SELECT 'vw_user_activity_profile' AS vista, COUNT(*) AS registros FROM vw_user_activity_profile;
```

## 🌐 Navegación en el Sistema

### Desde el Dashboard Principal (`/`)
Hay una nueva sección llamada **"🚀 Vistas Optimizadas de Oracle"** con 4 tarjetas:
1. 🎵 Canciones Completas
2. 📋 Playlists Públicas
3. 🏆 Ranking Top 50
4. 👥 Perfiles Detallados

### Menú de Navegación
Se agregó un botón especial en el menú: **🏆 Ranking**

## 📊 Ventajas de Usar las Vistas

### Antes (sin vistas):
```python
# Para mostrar una canción con todos sus datos:
cancion = query("SELECT * FROM SONGS WHERE song_id = ?")
autor = query("SELECT * FROM USERS WHERE user_id = ?")
generos = query("SELECT * FROM SONG_GENRES JOIN GENRES...")
likes = query("SELECT COUNT(*) FROM LIKES WHERE song_id = ?")
plays = query("SELECT COUNT(*) FROM PLAYS WHERE song_id = ?")
# = 5 consultas a la BD
```

### Ahora (con vistas):
```python
# Una sola consulta obtiene TODO:
cancion = query("SELECT * FROM vw_songs_complete WHERE song_id = ?")
# = 1 consulta a la BD ✨
```

## 🎨 Templates Incluidos

Todos los templates están en `templates/vistas/`:
- `canciones_completas.html` - Tabla con todas las canciones y sus estadísticas
- `playlists_publicas.html` - Grid de tarjetas con playlists
- `ranking_canciones.html` - Tabla de ranking con medallas 🥇🥈🥉
- `perfiles_usuarios.html` - Grid de tarjetas con estadísticas de usuarios
- `perfil_detalle.html` - Perfil individual con todas las canciones del usuario

## 🔗 URLs Completas

```
http://localhost:8000/                           # Dashboard principal
http://localhost:8000/vistas/canciones/          # Vista: Canciones completas
http://localhost:8000/vistas/playlists/          # Vista: Playlists públicas
http://localhost:8000/vistas/ranking/            # Vista: Ranking top 50
http://localhost:8000/vistas/perfiles/           # Vista: Perfiles de usuarios
http://localhost:8000/vistas/perfiles/1/         # Perfil detallado del usuario 1
```

## 💡 Tips

1. **Mejor rendimiento**: Las vistas pre-calculan los datos, especialmente útil para rankings y estadísticas
2. **Mantenimiento**: Si cambias la estructura de las tablas, recuerda actualizar las vistas
3. **Desarrollo**: Puedes modificar las vistas sin cambiar el código Python
4. **Debugging**: Usa `SELECT * FROM vw_nombre_vista` en SQL Developer para probar

## 🐛 Solución de Problemas

### Error: "table or view does not exist"
```sql
-- Verificar que las vistas existen
SELECT view_name FROM user_views;

-- Recrear las vistas
@crear_vistas_oracle.sql
```

### Las vistas no muestran datos
```sql
-- Verificar que hay datos en las tablas base
SELECT COUNT(*) FROM USERS WHERE IS_DELETED = 'N';
SELECT COUNT(*) FROM SONGS WHERE IS_DELETED = 'N';
```

### Error de permisos
```sql
-- Asegúrate de estar conectado como riffly_m
SHOW USER;
```

## 📝 Notas

- Las vistas se actualizan automáticamente cuando cambias los datos en las tablas
- No ocupan espacio adicional (son consultas guardadas)
- Puedes crear índices en las tablas base para mejorar aún más el rendimiento
- Las vistas incluyen filtros de `IS_DELETED = 'N'` para mostrar solo datos activos

## 🎓 Aprende Más

Para entender mejor cómo funcionan las vistas de Oracle:
- [Oracle Views Documentation](https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/CREATE-VIEW.html)
- Busca "Oracle Materialized Views" si necesitas aún más rendimiento con datos que cambian poco

---

**¡Disfruta de tu sistema Riffly optimizado!** 🎵🚀
-- ========================================
-- CREAR VISTAS OPTIMIZADAS EN ORACLE
-- Para el proyecto Riffly Music Platform
-- Usuario: riffly_m
-- ========================================

-- Vista 1: Información completa de canciones con 4 JOINs
CREATE OR REPLACE VIEW vw_songs_complete AS
SELECT 
    s.song_id,
    s.title,
    s.duration_sec,
    s.description,
    s.is_active,
    s.created_at,
    u_author.username AS author_username,
    u_author.display_name AS author_display_name,
    u_composer.username AS composer_username,
    u_composer.display_name AS composer_display_name,
    LISTAGG(g.name, ', ') WITHIN GROUP (ORDER BY g.name) AS genres,
    COUNT(DISTINCT l.user_id) AS total_likes,
    COUNT(DISTINCT p.play_id) AS total_plays
FROM songs s
INNER JOIN users u_author ON s.author_id = u_author.user_id
LEFT JOIN users u_composer ON s.composer_id = u_composer.user_id
LEFT JOIN song_genres sg ON s.song_id = sg.song_id
LEFT JOIN genres g ON sg.genre_id = g.genre_id
LEFT JOIN likes l ON s.song_id = l.song_id
LEFT JOIN plays p ON s.song_id = p.song_id
WHERE s.is_deleted = 'N'
GROUP BY 
    s.song_id, s.title, s.duration_sec, s.description, 
    s.is_active, s.created_at,
    u_author.username, u_author.display_name,
    u_composer.username, u_composer.display_name;

-- Vista 2: Playlists públicas con información del propietario
CREATE OR REPLACE VIEW vw_public_playlists AS
SELECT 
    pl.playlist_id,
    pl.name AS playlist_name,
    pl.description,
    pl.created_at,
    pl.updated_at,
    u.user_id,
    u.username,
    u.display_name,
    COUNT(ps.song_id) AS total_songs
FROM playlists pl
INNER JOIN users u ON pl.owner_id = u.user_id
LEFT JOIN playlist_songs ps ON pl.playlist_id = ps.playlist_id
WHERE pl.is_public = 'Y' 
  AND pl.is_deleted = 'N'
  AND u.is_deleted = 'N'
GROUP BY 
    pl.playlist_id, pl.name, pl.description, 
    pl.created_at, pl.updated_at,
    u.user_id, u.username, u.display_name;

-- Vista 3: Ranking de canciones más populares
CREATE OR REPLACE VIEW vw_top_songs_ranking AS
SELECT 
    s.song_id,
    s.title,
    u.username AS author_username,
    COUNT(DISTINCT p.play_id) AS total_plays,
    COUNT(DISTINCT l.user_id) AS total_likes,
    COUNT(DISTINCT c.comment_id) AS total_comments,
    ROUND(COUNT(DISTINCT p.play_id) * 0.5 + 
          COUNT(DISTINCT l.user_id) * 2 + 
          COUNT(DISTINCT c.comment_id) * 1.5, 2) AS popularity_score
FROM songs s
INNER JOIN users u ON s.author_id = u.user_id
LEFT JOIN plays p ON s.song_id = p.song_id
LEFT JOIN likes l ON s.song_id = l.song_id
LEFT JOIN comments c ON s.song_id = c.song_id AND c.is_deleted = 'N'
WHERE s.is_deleted = 'N' 
  AND s.is_active = 'Y'
GROUP BY s.song_id, s.title, u.username
ORDER BY popularity_score DESC;

-- Vista 4: Perfil de usuarios con estadísticas de actividad
CREATE OR REPLACE VIEW vw_user_activity_profile AS
SELECT 
    u.user_id,
    u.username,
    u.display_name,
    u.user_type,
    u.bio,
    u.created_at,
    COUNT(DISTINCT s.song_id) AS songs_created,
    COUNT(DISTINCT l.song_id) AS songs_liked,
    COUNT(DISTINCT p.play_id) AS total_plays,
    COUNT(DISTINCT pl.playlist_id) AS playlists_created,
    COUNT(DISTINCT fw.followee_id) AS following_count,
    COUNT(DISTINCT fr.follower_id) AS followers_count
FROM users u
LEFT JOIN songs s ON u.user_id = s.author_id AND s.is_deleted = 'N'
LEFT JOIN likes l ON u.user_id = l.user_id
LEFT JOIN plays p ON u.user_id = p.user_id
LEFT JOIN playlists pl ON u.user_id = pl.owner_id AND pl.is_deleted = 'N'
LEFT JOIN follows fw ON u.user_id = fw.follower_id
LEFT JOIN follows fr ON u.user_id = fr.followee_id
WHERE u.is_deleted = 'N' 
  AND u.is_active = 'Y'
GROUP BY 
    u.user_id, u.username, u.display_name, 
    u.user_type, u.bio, u.created_at;

-- Verificar que las vistas se crearon correctamente
SELECT 'vw_songs_complete' AS vista, COUNT(*) AS registros FROM vw_songs_complete
UNION ALL
SELECT 'vw_public_playlists' AS vista, COUNT(*) AS registros FROM vw_public_playlists
UNION ALL
SELECT 'vw_top_songs_ranking' AS vista, COUNT(*) AS registros FROM vw_top_songs_ranking
UNION ALL
SELECT 'vw_user_activity_profile' AS vista, COUNT(*) AS registros FROM vw_user_activity_profile;

-- Probar cada vista
SELECT * FROM vw_songs_complete FETCH FIRST 5 ROWS ONLY;
SELECT * FROM vw_public_playlists FETCH FIRST 5 ROWS ONLY;
SELECT * FROM vw_top_songs_ranking FETCH FIRST 5 ROWS ONLY;
SELECT * FROM vw_user_activity_profile FETCH FIRST 5 ROWS ONLY;

COMMIT;

