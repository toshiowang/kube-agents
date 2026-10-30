# Mock: the Home tab channel picker (option E of the `/sethome` plan)

Four variants of the gateway's App Home view. Each JSON is the view `publishHome` would send to `views.publish`: the dashboard as it is drawn today (Fleet, Waiting on you, Running, Recent pull requests, Last audit, the feedback tally) plus the new **Home channel** section. Sample values stand in for a real fleet.

| File | State |
| --- | --- |
| `1-no-home.json` | A `next` install with no home channel yet. A warning line under Fleet; the picker shows its placeholder. |
| `2-with-home.json` | A learned home channel. The picker shows it; the line says who set it and when. |
| `3-after-pick.json` | Right after a pick. The status line says it is recorded and takes effect within about two minutes, and names the previous channel. |
| `4-cr-set.json` | The CR field is set. No picker; the line names `spec.integration.slack.homeChannel` and the install.env key. |

## See it in Slack's Block Kit Builder

1. Open <https://app.slack.com/block-kit-builder> (a Slack login is needed; any workspace).
2. In the top bar choose the surface **App Home** (the default is Message).
3. Replace the JSON on the left with the contents of one file. The preview on the right is how Slack draws it; the channel picker opens as a real dropdown there.
4. Repeat for the other files.

The `<!date^…>` tokens render in the viewer's time zone; `<#C…>` and `<@U…>` render as channel and member mentions only in a workspace that has them, so the Builder may show the raw ids.

## The PNGs

`1-no-home.png` to `4-cr-set.png` are a local rendering of the same JSON (the `.html` beside each, screenshotted with headless Chrome in Slack's dark theme proportions). The Builder page needs a Slack login, so no screenshot was taken there. Slack's own drawing differs in fonts and spacing, not in blocks or order.

## What the picker does

- `conversations_select`, `action_id` `home_channel_select`, filter public and private channels only (no DMs or group DMs offered), initial value = the current home.
- A pick is a `block_actions` payload. The gateway re-checks the member against the allowlist (`homeAdmitted`), checks the channel with `conversations.info` (archived, Slack Connect, the app a member), writes the record with the resourceVersion precondition, republishes the view with the status line, and posts one line in the new channel and one in the old one.
- With the CR field set, or `homeChannelPolicy: manual`, the picker is not drawn and the line says where the value is set.

Plan: `~/.claude/handoffs/4187-sethome-plan.md`, v6.
