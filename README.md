# Scraping con GitHub Actions

Este proyecto es un ejemplo basico para aprender a ejecutar un script de Python automaticamente con GitHub Actions.

El scraper lee libros desde `https://books.toscrape.com/`, extrae titulo, precio, disponibilidad y rating, y guarda los resultados en archivos CSV y JSON.

## Archivos principales

- `scraper.py`: script de scraping.
- `requirements.txt`: librerias necesarias.
- `.github/workflows/scraper.yml`: automatizacion de GitHub Actions.

## Probar localmente

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scraper.py
```

En Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scraper.py
```

Los resultados se guardan en la carpeta `data/`.

## Ejecutarlo en GitHub Actions

1. Sube estos archivos a un repositorio de GitHub.
2. En GitHub, abre la pestana `Actions`.
3. Selecciona `Scheduled Python Scraper`.
4. Puedes ejecutarlo manualmente con `Run workflow`.
5. Tambien se ejecutara automaticamente segun el horario definido en `.github/workflows/scraper.yml`.

## Cambiar la hora

GitHub Actions usa UTC para los horarios programados.

Esta linea ejecuta el scraper todos los dias a las 13:00 UTC:

```yaml
- cron: "0 13 * * *"
```

Para Colombia, 13:00 UTC equivale normalmente a 08:00 hora local.

Formato cron:

```text
minuto hora dia-del-mes mes dia-de-la-semana
```

Ejemplos:

```yaml
# Todos los dias a las 08:00 Colombia, equivalente a 13:00 UTC
- cron: "0 13 * * *"

# Todos los lunes a las 09:30 Colombia, equivalente a 14:30 UTC
- cron: "30 14 * * 1"
```

## Ver resultados

Despues de cada ejecucion:

1. Entra a `Actions`.
2. Abre la ejecucion del workflow.
3. Baja hasta `Artifacts`.
4. Descarga `scraping-results`.

## Nota importante

Antes de scrapear una web real, revisa sus terminos de uso y su archivo `robots.txt`. Este ejemplo usa una web creada para practicar scraping.
