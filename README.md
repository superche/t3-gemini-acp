# Gemini for Mac as a T3 Code Local ACP provider

Add the `agy` executable bundled with Gemini for Mac to T3 Code as a **Local ACP command**. T3 starts it with `agy acp` and uses the models reported by the running agent.

## Requirements

- macOS with Gemini installed at `/Applications/Gemini.app`, or the path to its bundled `agy` executable.
- T3 Code with **Local ACP command** support. Open T3 at least once to initialize its settings.
- Python 3.9 or later.

## Configure

Run from this repository:

```sh
python3 configure.py
```

The script adds one provider to T3's settings. By default it reads `~/.t3/userdata/settings.json` or the equivalent path under `T3CODE_HOME`. Use `--settings` for another settings file and `--agy` for another installation path. Running it again with the same paths leaves the existing provider settings intact.

In T3, open **Settings → Providers** and select **Refresh provider status**. In a new thread, select **Gemini.app agy (Local ACP)** and a Gemini model. For a minimal check, ask it to reply with a short fixed phrase.

### Configure from T3 directly

Go to **Settings → Providers → Add provider → Show more → Local ACP command**. Set the executable to `/Applications/Gemini.app/Contents/Helpers/agy` and add `acp` as its only argument. Use the same Provider settings to remove the entry if needed.

## Login behavior

This configures an executable path and an argument. The running `agy` owns authentication and can use locally cached authorization when available. A successful reply confirms that the Local ACP route is authorized on that machine. It does not identify the Google account, guarantee access to a specific model or quota, or import the Gemini app's chat history.

Verified on macOS with T3 Code Nightly `0.1.12-nightly.20261123.5124` and bundled `agy` `1.5.5`. A fresh T3 thread returned the expected test phrase with Gemini 3.8 Flash without a fresh sign-in. The ACP response did not expose the account email.

## Model availability

T3 builds its model picker from the catalog returned by the local `agy acp` session. Gemini for Mac has its own model picker, and availability can vary by client, plan, and account. To see the models available to the bundled CLI on your machine, run:

```sh
/Applications/Gemini.app/Contents/Helpers/agy models
```

On the same Mac, `agy acp` 1.5.5 and 1.5.15 both exposed Gemini 3.8 Flash as their only Gemini model. Version 1.5.15 also rejected attempts to select Gemini 4 Neon, Argon, or Hydrogen in an ACP session. Adding those IDs to T3's Custom models does not grant access. [Google's model availability documentation](https://antigravity.google/docs/models) · [T3's ACP model picker documentation](https://github.com/pingdotgg/t3code/blob/main/docs/user/providers-acp.md#models-and-options)

[T3 Code Local ACP documentation](https://github.com/pingdotgg/t3code/blob/main/docs/user/providers-acp.md#add-a-local-command) · [Google Antigravity ACP documentation](https://antigravity.google/docs/ide/extensions/acp/)
