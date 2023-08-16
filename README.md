# Nev's Chat

1. `cd nevschat`
2. `docker build -t nevschat:latest .`
3. `docker system prune --force`
4. `docker run --rm -p 3000:3000 -p 8000:8000 nevschat:latest`
