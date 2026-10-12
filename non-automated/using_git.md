This file contains an overview of basic commands and their usage, 
as well as a basic overview of how we can work on each deliverable
together. The specifics are not what matters, so do whatever feels
right for you.

# Git Workflow
The project contains one or more files per deliverable, each with a clear name and purpose.

During the process of creating a new deliverable, we will create a new branch to work on called "Deliverable_X". We can each branch off of this to complete their own tasks and write code. 

It is usually a good idea to create a new branch if your idea is not a simple tweak, or if you are simply testing things out. An example naming scheme could be "<deliverable number>_<yourname>". E.g. "5_quinn".

To undo changes you make you can simply use the `git restore` command and pick which files to revert back to the last commit (save). See below on how to do this

If you haven't finished your work but need a change someone else made, you can merge their changes onto your branch.

# Git Cheat Sheet
## Switch to an existing branch

```bash
git switch branch-name
```

Example:
```bash
git switch deliverable_5
```


## Create a new branch

First switch to the branch you want to copy from:

```bash
git switch main
```

Then create the new branch:

```bash
git switch -c deliverable_7
```
## Commit changes
When you commit changes you are making a save of your current work. Git will remember all of these changes so you can come back to them later or undo them. 
### Stage all changed files:

```bash
git add .
```

### Create a commit:

```bash
git commit -m "Describe the changes"
```

Example:

```bash
git commit -m "Add project setup checks"
```
## Merge one branch into another

### Switch to the branch that should receive the changes:

```bash
git switch main
```

### Merge the other branch:

```bash
git merge deliverable_6
```

This merges deliverable_6 into main.

## View all branches
```bash
git branch
```

## Revert/undo changes
```bash
git revert <filename>
```

Example
The following will undo the changes made to `merge_listings.py` and `README.md`
```bash
git revert merge_listings.py README.md
```

The current branch is marked with *.

## Typical workflow
```bash
git switch deliverable_5
git switch -c my-new-feature
``` 
_Make changes_

```bash
git status
git add .
git commit -m "Implement new
```

**Quick rule:** create a branch for new work, commit often with clear messages, and merge back into `main` when the work is complete.
