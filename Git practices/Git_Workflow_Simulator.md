# Git Workflow Simulator

```
Documented a Git workflow project covering branching strategy, pull requests, conflict resolution, tags, releases and changelog
automation.
```
## Solving git merge conflict

**Explanation**:
In the project I have 3 brances:
- main
- dev
- feature  
I have eddited main.py in the main branch, than I have commited it. To create the conflict I also made some correction in the same file in branch feature. Because I had 2 versions of the file in the same place, the conflict appeared. To solve this conflict, I left only one version of the code in main.py. Than, I made merging again and finished with the final commit (da07bb6).

### Branch history and merge conflict resolution

```mermaid
flowchart TD
    A["1. Initial commit<br/>main and feature point here"]
    B["2. Commit on feature<br/>Edit main.py"]
    FF["3. Fast-forward main to this commit<br/>main and feature now point here<br/>No new commit is created"]
    C["4. Commit on main<br/>Change the same line to version A"]
    D["5. Commit on feature<br/>Change the same line to version B"]
    E["6. Merge feature into main<br/>Conflicting edits — merge pauses"]
    F["7. Resolve the conflict<br/>Choose or combine the final code"]
    M["8. Create the merge commit on main<br/>Both branches' histories are preserved"]

    A --> B
    B -.-> FF
    B --> C
    B --> D
    C --> E
    D --> E
    E --> F
    F --> M

    classDef main fill:#dbeafe,stroke:#2563eb,color:#172554
    classDef feature fill:#fef3c7,stroke:#d97706,color:#451a03
    classDef conflict fill:#fee2e2,stroke:#dc2626,color:#450a0a
    classDef resolved fill:#dcfce7,stroke:#16a34a,color:#052e16

    class C main
    class B,D feature
    class E conflict
    class F,M resolved
```


## Creating issue template, adding new features and creating PR

I decided to make a feature, that you can see how often users are visiting different pages. I made a suggestion in GitHub on tab "Issues":

![Issue pic](photos/Issue.png)

Than I create a file *login_statistics.py*. Added to index -> commited -> Pushed on branch feature.

Afterwards I created PR (I willn't delete it to show you)
![PR pic](photos/PR.png)

Than I accepted this PR and as you can see there are no any conflicts for merging:
![No conflict while PR](photos/Before_approving_PR.png)


## Conventional comments and changelog

Now I have used *conventional commit*, I did it to add CHANGELOG.md, where I described what is going to be released and which features are already in the project. Then I commited this file to feaute branch and created PR (You can see it as **Added feature for statistics #2**)

How I created conventional comment:
```bash
git commit -m "docs{changelog} Added changelog before the release"
```

## Release
I have created a release, so you can download the code base and run it on your computer!