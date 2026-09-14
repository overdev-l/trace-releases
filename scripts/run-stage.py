"""Keep private build output off public Actions logs and artifacts."""
import os, pathlib, re, subprocess, sys
stage, *command = sys.argv[1:]
if not re.fullmatch(r'[a-z-]+', stage):
    raise SystemExit('Invalid stage')
log = pathlib.Path(os.environ['RUNNER_TEMP']) / ('trace-' + stage + '.log')
# On Windows the package manager is a .cmd shim. The command is repository-owned,
# never constructed from workflow input or an untrusted pull request.
if os.name == 'nt' and command[0] == 'pnpm':
    command = ['cmd.exe', '/d', '/s', '/c', subprocess.list2cmdline(command)]
with log.open('wb') as output:
    result = subprocess.run(command, stdout=output, stderr=subprocess.STDOUT)
if result.returncode:
    codes = sorted(set(re.findall(r'\b(?:TS|CS|NETSDK|MSB|ERR_PNPM_)[A-Z0-9_]+\b', log.read_text(errors='replace'))))
    print(f'::error::{stage} failed (exit {result.returncode}); diagnostic codes: {", ".join(codes) or "none"}. Private logs are not published.')
else:
    print(stage + ': passed')
sys.exit(result.returncode)
