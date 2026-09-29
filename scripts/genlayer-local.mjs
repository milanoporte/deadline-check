import os from 'node:os';
import path from 'node:path';

// The CLI resolves its config under os.homedir() at startup. Keep that
// directory within this project without changing the user's HOME variable.
os.homedir = () => path.resolve(import.meta.dirname, '..', '.tool-home');

await import('../node_modules/genlayer/dist/index.js');
