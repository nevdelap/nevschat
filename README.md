# Nev's Chat

## Update Reflex

```bash
cd reflex &&
git fetch &&
git checkout origin/main && # Or a tag.
cd .. &&
git add reflex &&
git commit -m 'Update reflex.' &&
pip install -e reflex
```

## Run The App

```bash
cd app &&
reflex init && reflex run # Test at http://localhost:3000/
```

## Release

```bash
git add . &&
git commit -m 'whatever' &&
git push origin HEAD:master &&
git tag -f latest &&
git push -f origin latest &&
ssh_droplet

# On the droplet.
cd nevschat &&
scripts/deploy && sleep 30 && scripts/logs
^C
exit
```
