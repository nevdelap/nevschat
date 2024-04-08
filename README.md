# Nev's Chat

This is my private thing that I use everyday, deployed at
[www.nevdelap.com/chat](http://www.nevdelap.com/chat) (behind auth), because it
does exactly what I want and nothing else.

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
reflex init && reflex run # Test at http://localhost:3000/
```

## Release On DigitalOcean

```bash
git add . &&
git commit -m 'whatever' &&
git merge latest &&
git push origin HEAD:master &&
git tag -f latest &&
git push -f origin latest &&
ssh_droplet

# On the droplet.
cd ~/nevschat &&
scripts/deploy && sleep 30 && scripts/logs
^C
exit
```

### General Info

#### Page structure

* nevschat.py
  * vstack
    * title
    * chat (in chat.py)
    * cancel X
* chat.py
  * chat
    * vstack contains
      * wrap with the checkboxes, radio buttons, and dropdowns.
      * foreach has the previous prompts_responses each rendered by
        prompt_response_box.
      * hstack has the next prompt with buttons.
  * prompt_response_box
    * has a conditional, rendering a prompt as being edited, or not edited with
      buttons.
    * if not being edited and is being generated renders a cancel button next to
      the response.
