# Nev's Awesome ChatGPT

This is my private thing that I use everyday, deployed at
[www.nevdelap.com/chat](http://www.nevdelap.com/chat) (behind auth), because it
does exactly what I want and nothing else.

<img
  src="screenshot.png"
  width="839px"
  alt="Screenshot of Nev's Awesome ChatGPT" />

<img
  src="screenshot2.png"
  width="839px"
  alt="Another screenshot of Nev's Awesome ChatGPT" />

## Prerequisites

```bash
paru -Sy unzip
```

## From Scratch

```bash
mkdir -p ~/miniconda3 &&
cd ~/miniconda3 &&
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
  -O miniconda.sh &&
bash miniconda.sh -b -u -p ~/miniconda3 &&
rm miniconda.sh &&
mkdir ~/nevschat &&
cd ~/nevschat &&
git clone git@github.com:nevdelap/droplet.git &&
git clone git@github.com:nevdelap/nevschat.git &&
cd nevschat &&
git submodule init &&
git submodule update &&
scripts/install_dev
```

## Update Reflex

```bash
cd reflex &&
git fetch &&
git checkout v0.4.6 &&
cd .. &&
git add reflex &&
git commit -m 'Update reflex.' &&
pip install -e reflex
```

## Run The App In Dev

```bash
cd app &&
reflex run # Test at http://localhost:3000/
```

## Release On DigitalOcean

This shows `scripts/lint` being run manually though it can be run automatically
with `scripts/install_hooks`.

```bash
git add . &&
git commit -m 'whatever' &&
scripts/lint &&
git push --force origin HEAD:master --no-verify &&
git tag --force latest &&
git push --force origin latest --no-verify &&
ssh_droplet "cd ~/nevschat && scripts/deploy && sleep 30 && scripts/logs"
```

## Quick Release

This is used as `lpd` - lint, push, deploy.

```bash
#!/bin/bash
current_dir="$(basename "$(pwd)")"
if [[ "$current_dir" == "droplet" ]]; then
    echo 'Pushing droplet.'
    git push --force origin HEAD:master
    git push --tags
    ssh_droplet "
        cd ~/droplet &&
        git fetch &&
        git checkout origin/master
    "
elif [[ "$current_dir" == "nevschat" ]]; then
    echo 'Linting, pushing, and deploying nevschat.'
    scripts/lint &&
    git push --force origin HEAD:master --no-verify &&
    git tag --force latest &&
    git push --force origin latest --no-verify &&
    ssh_droplet "
        cd ~/droplet &&
        git fetch &&
        git checkout origin/master &&
        monit reload &&
        cd ~/nevschat &&
        scripts/deploy &&
        sleep 30 &&
        scripts/logs
    "
fi
```

### General Info

#### Documentation

* [Reflex Component Library](https://reflex.dev/docs/library/)
* [Radix  UI](https://www.radix-ui.com/)
  * [Icons](https://lucide.dev/icons)
  * [Colors](https://www.radix-ui.com/colors)

#### OpenAI

The OpenAI key is supplied in the OPENAI_API_KEY environment variable. It should
be [configured](https://platform.openai.com/settings/organization/limits) with a
monthly budget and email notification when it is exceeded.

#### Google TTS

The Google TTS API key is supplied in the GOOGLE_TTS_KEY environment variable.
It should be [restricted](https://console.cloud.google.com/apis/credentials) to
be usable only for the Cloud Text-to-Speech API, and only from the production
and development IP addresses.

#### DeepL

The DeepL auth key is supplied in the DEEPL_AUTH_KEY environment variable. So
far I'm on the free tier so I haven't configured any restrictions on it yet.
