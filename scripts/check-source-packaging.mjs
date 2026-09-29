// Offline source packaging only; no client, wallet, or RPC is constructed.
import { readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { abi } from 'genlayer-js';
import { fromRlp } from 'viem';

export const RUNNER = 'py-genlayer:5jycge4q8k23462jtb0b9fyey1s9qz928sz2nbrd9mg4sxqg2qng';
export const CONTRACT = new URL('../contracts/DeadlineCheck.py', import.meta.url);

// Text branch of executor/src/runners/parse.rs at c698f5551d52852b32b4975f437322f171ce4efe:
// comment starts at byte zero; contiguous lines use that prefix; an optional
// first version comment is omitted, and remaining comment contents concatenate.
export function parseRunnerComment(source) {
  const text = new TextDecoder('utf-8', { fatal: true, ignoreBOM: true }).decode(source);
  const prefix = ['//', '#', '--'].find(p => text.startsWith(p));
  if (!prefix) throw new Error('invalid_contract runner absent');
  let comment = '';
  let first = true;
  for (const line of text.split(/\r?\n/)) {
    if (!line.startsWith(prefix)) break;
    const content = line.slice(prefix.length);
    if (!(first && content.trim().startsWith('v'))) comment += content;
    first = false;
  }
  return JSON.parse(comment);
}

export function checkSourcePackaging(source) {
  // Decode without silently stripping a BOM: the executor checks raw byte zero.
  const text = new TextDecoder('utf-8', { fatal: true, ignoreBOM: true }).decode(source);
  const action = parseRunnerComment(source);
  // Project policy is a first-line Depends action, although GenVM also supports
  // version comments, multiline JSON, and other initialization actions.
  const first = text.split(/\r?\n/, 1)[0];
  if (!first.startsWith('#') || JSON.parse(first.slice(1)).Depends !== RUNNER
      || action.Depends !== RUNNER) throw new Error('Expected first-line pinned Depends header');
  // Same string input and serialize([code, calldata, leaderOnly]) path used by
  // pinned CLI readContractCode and SDK deployContract. Nothing is submitted.
  const serialized = abi.transactions.serialize([text, abi.calldata.encode({}), false]);
  const [encodedCode] = fromRlp(serialized, 'hex');
  const submitted = Buffer.from(encodedCode.slice(2), 'hex');
  if (!submitted.equals(source)) throw new Error('Deployment serialization changed source bytes');
  return { runner: RUNNER, sourceBytes: source.length,
    sourceSha256: createHash('sha256').update(source).digest('hex'), submittedBytesPreserved: true };
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  console.log(JSON.stringify(checkSourcePackaging(readFileSync(CONTRACT)), null, 2));
}
