# Claude Development Guide for Olivier's Blog

This document providers instructions for AI assistants (like Claude) working on the Olivier's Blog project.

## Project Overview

Olivier's Blog project is a blog to let Olivier express himself on various topics.

## Design principles

## Architecture

## Test-Driven Development

## Tasks & agents

This list of tasks can be found in `.claude/tasks/todo` and `.claude/tasks/done`. Done tasks provide history of my prompts. Todo tasks are the next envisonned steps.

**CRITITCAL** You can always look the vision ahead in written todo tasks, but we NEVER implement anything else that the very next step (first todo tasks, by alphabetic order). Other tasks are informative and may help making future-proof design decisions. If it leads to unecessary complexity, we just forget about them and act as if they were not written at all.

**IMPORTANT** If you block on something and are in autonomous mode, adapt the task with your analysis and questions, move it to `analyzed` and move to the next task.

**CRITICAL** Commit everytime you have something stable. You should end up having ONE commit per task. `Use commit --amend` if needed. NEVER have two different tasks commited together.
