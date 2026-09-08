// pm2 process definitions for the auto-request webhook.
//
// This was the tmux session `autoreq`, window 0, restarted by attaching
// and pressing Ctrl-C.
// pm2 is what the rest of this box already runs, and unlike tmux it brings a
// process back when it dies and keeps logs where a script can read them.
//
//   pm2 start ecosystem.config.js
//   pm2 restart autoreq
//   pm2 logs autoreq
//
// No deploy workflow and no CI: pushing to main changes nothing on the server.
// Deploying is `git pull` in the checkout there, then the restart above.
//
// After changing which apps exist, run `pm2 save`, or `pm2 resurrect` brings
// back the previous set.

const CWD = __dirname;

// The venv, explicitly. pm2 runs no login shell, so it never picks up the
// activated venv these were started under, and a bare `python` would resolve to
// the system interpreter -- which has a different set of packages.
const PY = CWD + "/.venv/bin/python";

const base = {
  cwd: CWD,
  interpreter: PY,
  autorestart: true,
  exp_backoff_restart_delay: 5000,
  max_restarts: 50,
  min_uptime: "60s",
  kill_timeout: 15000,
  time: true,
  env: { PYTHONUNBUFFERED: "1" },
};

module.exports = {
  apps: [
    // Observed at 108 MB.
    { ...base, name: "autoreq", script: "autoreqmain.py", max_memory_restart: "1G" },
  ],
};
