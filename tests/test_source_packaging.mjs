import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { checkSourcePackaging, parseRunnerComment, RUNNER, CONTRACT } from '../scripts/check-source-packaging.mjs';

const header = `# { "Depends": "${RUNNER}" }`;
const source = body => Buffer.from(body, 'utf8');

test('actual contract has pinned first-line header and survives SDK deployment serialization', () => {
  const bytes = readFileSync(CONTRACT);
  assert.equal(bytes.subarray(0, bytes.indexOf(10)).toString(), header);
  assert.equal(checkSourcePackaging(bytes).submittedBytesPreserved, true);
  // Local logic may evolve after deployment; the header and exact current
  // submitted-byte round trip remain the packaging invariants.
});

test('missing, misplaced, malformed, aliased and wrong runner headers fail', () => {
  for (const body of ['"""docstring"""\n', `\n${header}\n`, `\ufeff${header}\n`,
    `pass\n${header}\n`, '# { invalid }\n', '# { "Depends": "py-genlayer:latest" }\n',
    '# { "Depends": "py-genlayer:test" }\n', '# { "Depends": "py-genlayer:wrong" }\n']) {
    assert.throws(() => checkSourcePackaging(source(body)));
  }
});

test('parser honors supported comment blocks and version line; policy requires first-line Depends', () => {
  assert.deepEqual(parseRunnerComment(source(`# v0.3.0\n# {\n# "Depends": "${RUNNER}"\n# }\npass\n`)), { Depends: RUNNER });
  for (const prefix of ['//', '--']) {
    assert.deepEqual(parseRunnerComment(source(`${prefix} { "Depends": "${RUNNER}" }\ncode`)), { Depends: RUNNER });
  }
  assert.throws(() => checkSourcePackaging(source(`# v0.3.0\n${header}\npass`)));
  // Whitespace inside the comment, CRLF and no trailing newline are supported.
  assert.equal(checkSourcePackaging(source(`#\t{"Depends":"${RUNNER}"}\r\npass\r\n`)).submittedBytesPreserved, true);
  assert.equal(checkSourcePackaging(source(header)).submittedBytesPreserved, true);
});
