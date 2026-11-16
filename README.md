# workflows
Reusable workflows for ucsb-cs156 projects

Each workflow starts with a comment showing an example invocation.

* `37-frontend-storybook-coverage.yml`: reports which React components and pages under
  `frontend/src/main` have no matching story under `frontend/src/stories` (one-to-one directory
  mirroring convention), as a table in the job summary of each run, and publishes an HTML copy to
  the repo's GitHub Pages site (`storybook-coverage/` for main, `prs/<N>/storybook-coverage/` for
  PRs; the caller must grant `contents: write`). Workflows `02`/`04` produce and publish the same
  report when the whole gh-pages site is rebuilt. Report-only by default; pass
  `FAIL_ON_MISSING_STORIES: true` to make it a failing check once a repo reaches 100%. The work is
  done by `python/storybook_coverage.py` (tests in `python/test_storybook_coverage.py`, run by
  `121-python-unit-tests.yml`).
* `110-release-autograder.yml`: builds the Gradescope `<assignment>-Autograder-<tag>.zip` of an
  autograder repository (jpa00, jpa01, jpa02, jpa03, team01, team02, ...) and attaches it to the
  GitHub release for the pushed tag.
* `82-kanban-slack-update.yml`: **superseded (October 2026)**. Posted a table of Kanban board
  issue counts (by column and assignee) to the team's Slack channel when called from a wrapper
  in each team01/team02 repo. The summary now runs once, centrally, from the term's
  `membership-scripts` repo (workflow 82 there, `kanban_slack_update.py`), so the wrappers are
  being removed; this file is kept for one quarter and will then be deleted. See
  <https://ucsb-cs156.github.io/topics/github_actions/workflow_82.html>.
