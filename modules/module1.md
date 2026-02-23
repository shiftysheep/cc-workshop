## Module 1
1. Clone this repository where you want to store the code: `git clone https://github.com/shiftysheep/cc-workshop.git`
2. Change into the project directory: `cd cc-workshop`
3. Launch Claude from the terminal `claude`. If you have issues the path for the claude binary may not be in your system path. 
4. Enter this prompt: 
```markdown
Let's setup our project scaffolding utilizing UV. We will be creating a Typer cli application with the name of todd. Include a hello command. 
```
5. Once Claude is done you can execute the command directly in the chat box with the `!` command prefix:
```shell
!uv run todd hello
```
6. Now let's setup our status line before we continue to the next module. In the chat box enter this prompt:
```markdown
/statusline Show {model short name} | {context}% context | {cwd} | {git_status} | {branch} where git status is green "clean" or yellow "modified" using ANSI colors, and omit git fields if not in a repo.
```
7. Claude should have setup your status line with the requested information giving you a nice heads up display to utilize as you are working in the terminal. 
8. If Claude hasn't, ask to commit your changes before executing `/module` to proceed. 