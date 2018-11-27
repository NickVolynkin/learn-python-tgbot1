# Telegram bot sandbox

Store environment variables in `.env`:

```ini
TG_TOKEN=value
PROXY_URL=value
PROXY_USER=value
PROXY_PASS=value
```

Then export them with:

```bash
export $(cat .env | xargs) 
```

Run tests with:

```bash
python3 -m nose
```
