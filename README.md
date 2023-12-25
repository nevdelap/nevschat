# Nev's Chat

## Update Reflex

```bash
cd reflex &&
git fetch &&
git checkout v0.3.2 &&
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
    * Cancel X
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
