// Read-only preflight. Uses no account, wallet, simulation, or write RPC.
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { readFileSync, writeFileSync } from 'node:fs';
import { createClient } from 'genlayer-js';
import { studioDevnet } from 'genlayer-js/chains';

const old = JSON.parse(readFileSync('deployments/first-evaluation-preview.json'));
const deployed = JSON.parse(readFileSync('deployments/studio-dev-2026-09-28-e8b418de.json'));
const priorSignerMetadata = JSON.parse(readFileSync('deployments/evidence/manual-evaluation-preflight-1790443162094.json'));
const address = '0x205489BCFb115DE0956974d96e30c6C79CA9361d';
const rpc = 'https://studio-dev.genlayer.com/api';
const signer = '0xb1a4d9ff24d72c5df4ff73df6b1b829e4557576a';
const args = old.args;
assert.equal(args.length, 5);
assert.equal(args[0], 'python-3130-final-1790441362822');
assert.equal(args[4], 7);
assert.equal(deployed.contractAddress.toLowerCase(), address.toLowerCase());
assert.equal(deployed.sender.toLowerCase(), signer);
assert.equal(old.authorizedSigner, signer);
assert.equal(priorSignerMetadata.signer.toLowerCase(), signer);
assert.equal(priorSignerMetadata.activeAccount, 'default');
const urls = args.slice(1, 4);
assert.deepEqual(urls, old.sources.map(x => x.url));
for (const url of urls) {
  const parsed = new URL(url);
  assert.equal(parsed.hostname, 'discuss.python.org');
  assert.equal(parsed.username, '');
  assert.equal(parsed.password, '');
}
const sources = await Promise.all(urls.map(async (url, i) => {
  const response = await fetch(url, { redirect: 'manual', signal: AbortSignal.timeout(30000) });
  const body = Buffer.from(await response.arrayBuffer());
  const media = (response.headers.get('content-type') || '').split(';')[0].trim().toLowerCase();
  const decoded = new TextDecoder('utf-8', { fatal: true }).decode(body);
  JSON.parse(decoded);
  const quotePresent = decoded.includes(old.facts[i].quote);
  return { url, status: response.status, contentType: response.headers.get('content-type'),
    location: response.headers.has('location'), bytes: body.length,
    sha256: createHash('sha256').update(body).digest('hex'), utf8: true,
    jsonValid: true, quotePresent,
    usable: response.status === 200 && !response.headers.has('location') &&
      media === 'application/json' && body.length > 0 && body.length <= 32768 && quotePresent };
}));
assert(sources.every(x => x.usable));

const client = createClient({ chain: studioDevnet, endpoint: rpc });
const options = Object.fromEntries(Object.entries(old.feeEstimate.distribution).map(
  ([key, value]) => [key, key === 'rotations' ? value.map(BigInt) : BigInt(value)]));
const [chainId, missing, feePolicy, balance, deposit] = await Promise.all([
  client.request({ method: 'eth_chainId', params: [] }),
  client.readContract({ address, functionName: 'get_case', args: [args[0]] }),
  client.request({ method: 'sim_getFeeConfig', params: [] }),
  client.request({ method: 'eth_getBalance', params: [signer, 'latest'] }),
  client.estimateTransactionFees(options),
]);
assert.equal(BigInt(chainId), 61997n);
assert.equal(missing, '');
assert.equal(feePolicy.enabled, true);
assert(BigInt(balance) >= BigInt(deposit.feeValue));
const fees = JSON.stringify({ distribution: old.feeEstimate.distribution });
const command = `node node_modules/genlayer/dist/index.js write ${address} evaluate_delay --wallet keystore --rpc ${rpc} --fees '${fees}' --args ${args.join(' ')}`;
const result = {
  checkedAt: new Date().toISOString(), submitted: false, chainId: 61997,
  rpc, contractAddress: address, signer,
  signerEvidence: 'Prior public metadata identifies default as the authorized signer; it matches the verified new deployment sender. No wallet opened.',
  functionName: 'evaluate_delay', args, sources,
  unusedCaseRead: { caseId: args[0], result: missing },
  feePolicy, feeQuote: deposit, balanceWei: BigInt(balance),
  balanceCoversDeposit: BigInt(balance) >= BigInt(deposit.feeValue),
  budgetBasis: 'Reuses prior generic write distribution. SDK deposit is a fee quote, not a target-specific simulation or success guarantee.',
  extractionFailureBehavior: 'Handled malformed extraction and INVALID_FACT fail closed to INSUFFICIENT_EVIDENCE / UNKNOWN / EXTRACTION_FAILED / 0. This does not guarantee a substantive verdict or consensus.',
  manualCommand: command,
};
const path = `deployments/new-evaluation-preview-${Date.now()}.json`;
writeFileSync(path, JSON.stringify(result, (_, v) => typeof v === 'bigint' ? v.toString() : v, 2) + '\n', { flag: 'wx' });
console.log(JSON.stringify({ path, sources, chainId: 61997, unusedCase: missing,
  signer, balanceWei: String(balance), feeValue: String(deposit.feeValue),
  feePolicyEnabled: feePolicy.enabled }));
