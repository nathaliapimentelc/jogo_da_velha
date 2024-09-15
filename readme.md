# testando jogo

Description project

## Config terminals to GIT

Open file:

```bash
code ~/.bashrc
```

Ctrl + C and Ctrl + V

```text
# GIT current branch
# Function to get current Git branch
parse_git_branch() {
    local branch
    branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)
    if [ -n "$branch" ]; then
        echo "($branch)"
    fi
}

parse_git_branch() {
     git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/(\1)/'
}
export PS1="\u@\h \[\e[32m\]\w \[\e[91m\]\$(parse_git_branch)\[\e[00m\]$ "
```

## Config VSCode

Install pluins to VSCode

- ms-python.autopep8
- sobytes.flet-control-wrap
- VisualStudioExptTeam.vscodeintellicode
- ms-python.python
- ms-python.vscode-pylance
- vscode-icons-team.vscode-icons
- shd101wyy.markdown-preview-enhanced
- NguyenHoangLam.beautiful-dracula
