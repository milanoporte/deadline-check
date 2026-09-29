# DeadlineCheck

DeadlineCheck is an experimental GenLayer Intelligent Contract for recording an assessment of a publicly documented software milestone delay. This repository includes a **read-only case viewer**. It does not offer a submission flow, wallet connection, or automated claim that a stored outcome is substantively correct.

The latest verified live case ended **INSUFFICIENT_EVIDENCE / EXTRACTION_FAILED / 0 approved days**. The transaction finalized and executed successfully, but the stored outcome is **fail-closed, not a substantive delay judgment**.

## Run the reviewer page locally

From this project root, use Node.js 20.19+ or 22.12+:

```sh
npm ci --ignore-scripts
npm run dev:frontend
```

Open the local URL printed by Vite. Choose **verified Python 3.13.0 case**, or enter `python-3130-final-1790441362822` and select **Read case**. The page checks chain ID 61997 and calls the pinned `genlayer-js@2.0.0-rc.1` `readContract({ address, functionName: 'get_case', args: [caseId] })` against `https://studio-dev.genlayer.com/api`. It shows each returned JSON field without deriving a new classification. An unused ID shows an empty state; an unavailable RPC shows an error. No account or wallet is needed.

For a production bundle, run `npm run build:frontend` and serve `frontend/dist/` as static files. The page has not been published.

## Contract and evidence

| Item | Verified value |
| --- | --- |
| Network | GenLayer Studio-dev, chain ID `61997` |
| Contract | `0x661F31a2017CFC3Cd48D0D6b6978415FAf0A6c59` |
| Contract source | [contracts/DeadlineCheck.py](contracts/DeadlineCheck.py), SHA-256 `e1590172ff6211243a67c8d9a83da5813adcb02988253604c3fde9efc186ddfb` |
| Deployment transaction | `0xd135ca65b420c70f1c12fb427091d1adccb93ae8d5f1cbe35b04684815b2965b` |
| Evaluation transaction | `0xab0d76161b329074a8294da16719de56ac9a3f5b5e21eb82f64c7a1c514cebb9` |
| Verified case ID | `python-3130-final-1790441362822` |

The [deployment evidence](deployments/evidence/deployment-d135ca65-1790680430517.json) confirms the finalized constructor, source hash, and live ABI. The [evaluation evidence](deployments/evidence/evaluation-ab0d7616-2026-09-29.json) records the public-history match, finalized lifecycle, successful execution, and exact raw `get_case` return. [docs/STATUS.md](docs/STATUS.md) summarizes both verifications. The frontend links to the [Studio-dev contract explorer](https://explorer-studio-dev.genlayer.com/address/0x661F31a2017CFC3Cd48D0D6b6978415FAf0A6c59).

## Read-only reviewer steps

1. Open the verified-case link in the local page. Confirm that the contract address shown there is the one above.
2. Confirm the displayed `case_id`, `verdict`, `responsible_party`, `reason_code`, `approved_days`, and `explanation` against the raw `getCase.raw` in the evaluation evidence.
3. Confirm the evaluation transaction is `FINALIZED`, execution is `FINISHED_WITH_RETURN`, and receipt status is `0x1` in that evidence. This establishes a successful write, **not** a substantive judgment.
4. Enter a new, unused case ID to observe the empty state. This invokes `get_case` only.

## Known limits

- Studio-dev is a preview network; its state and availability can change. The browser also needs access to its public RPC.
- The verified live model assessment could not be parsed or failed strict fact validation. No successful substantive live delay assessment is established.
- The viewer reads stored cases only. It cannot create, retry, appeal, or change one, and it does not independently verify the source pages or the contract's reasoning.
- This workspace has no published website, demo video, logo, or Git remote. Local evidence files become publicly accessible only if the project is separately published.
- [PLAN.md](PLAN.md), [docs/FIRST_LIVE_EVALUATION.md](docs/FIRST_LIVE_EVALUATION.md), and historic parts of [docs/TOOLCHAIN.md](docs/TOOLCHAIN.md) record earlier preparation phases; their pre-deployment commands and expected outcomes are not current reviewer instructions.

No website or Project Explorer submission has been published from this workspace.
