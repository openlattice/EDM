# EDM

This repository is our gateway to a peer-reviewed EDM (entity data model) development.  The (human readable) specification of the EDM are in the `data`-folder, while the agent is in `edm-controller`.

Idea:

#### Someone wants to make a change to the edm

1. create a new branch
        git checkout -b name_of_proposed_change
2. make changes locally
3. add files where changes were made, commit and push changes, eg.
        git add data/associationtypes.yaml
        git commit -m "an explanation of the propsed change"
        git push origin name_of_proposed_change
4. submit a pull request on github:
  - go on github to the repo, and select the branch of changes
  - click new pull request and fill out all the things
