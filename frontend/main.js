import { createClient } from 'genlayer-js';
import { studioDevnet } from 'genlayer-js/chains';
import './style.css';

const RPC = 'https://studio-dev.genlayer.com/api';
const ADDRESS = '0x661F31a2017CFC3Cd48D0D6b6978415FAf0A6c59';
const CASE_ID = /^[a-z0-9][a-z0-9_-]{2,63}$/;
const client = createClient({ chain: studioDevnet, endpoint: RPC });

const form = document.querySelector('#case-form');
const input = document.querySelector('#case-id');
const button = document.querySelector('#read-button');
const status = document.querySelector('#status');
const record = document.querySelector('#case-record');

function showStatus(message, kind = '') {
  status.textContent = message;
  status.className = `status ${kind}`.trim();
  status.hidden = false;
  record.hidden = true;
  record.replaceChildren();
}

function showRecord(fields) {
  const rows = Object.entries(fields).map(([key, value]) => {
    const row = document.createElement('div');
    row.className = 'record-row';
    const name = document.createElement('dt');
    name.textContent = key;
    const storedValue = document.createElement('dd');
    storedValue.textContent = value !== null && typeof value === 'object'
      ? JSON.stringify(value) : String(value);
    row.append(name, storedValue);
    return row;
  });
  record.replaceChildren(...rows);
  record.hidden = false;
  status.hidden = true;
}

async function readCase(caseId) {
  if (!CASE_ID.test(caseId)) {
    showStatus('Enter a valid case ID using the format shown above.', 'error');
    input.focus();
    return;
  }

  button.disabled = true;
  showStatus(`Reading ${caseId} from Studio-dev…`, 'loading');
  try {
    const chainId = await client.request({ method: 'eth_chainId', params: [] });
    if (BigInt(chainId) !== 61997n) throw new Error('RPC returned an unexpected chain ID.');
    const raw = await client.readContract({
      address: ADDRESS,
      functionName: 'get_case',
      args: [caseId],
    });
    if (typeof raw !== 'string') throw new Error('Contract returned a non-string value.');
    if (raw === '') {
      showStatus(`No stored record exists for ${caseId}.`, 'empty');
      return;
    }
    const fields = JSON.parse(raw);
    if (fields === null || Array.isArray(fields) || typeof fields !== 'object') {
      throw new Error('Contract returned a record in an unexpected format.');
    }
    showRecord(fields);
  } catch (error) {
    showStatus(`Could not read this case. ${error instanceof Error ? error.message : String(error)}`, 'error');
  } finally {
    button.disabled = false;
  }
}

form.addEventListener('submit', (event) => {
  event.preventDefault();
  const caseId = input.value.trim();
  if (CASE_ID.test(caseId)) {
    const url = new URL(window.location.href);
    url.searchParams.set('case_id', caseId);
    window.history.replaceState(null, '', url);
  }
  readCase(caseId);
});

const linkedCaseId = new URLSearchParams(window.location.search).get('case_id');
if (linkedCaseId !== null) {
  input.value = linkedCaseId;
  readCase(linkedCaseId);
}
