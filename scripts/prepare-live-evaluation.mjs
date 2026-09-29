// Read-only preparation. No account, wallet, simulation, or write API.
import {createClient} from 'genlayer-js';
import {studioDevnet} from 'genlayer-js/chains';
import {writeFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
const rpc='https://studio-dev.genlayer.com/api';
const address='0xe6f388C923b148C02Bf156357AaE19eBd7A350bb';
const sender='0xb1a4d9ff24d72c5df4ff73df6b1b829e4557576a';
const urls=[
 'https://blog.python.org/2024/09/python-3130rc2-3126-31110-31015-3920/',
 'https://discuss.python.org/t/python-3-12-7-and-3-13-0rc3-released/66306',
 'https://www.python.org/downloads/release/python-3130/'
];
const client=createClient({chain:studioDevnet,endpoint:rpc});
const caseId=`python-3130-final-${Date.now()}`;
const sources=await Promise.all(urls.map(async url=>{
 const syntaxValid=url.length>=12&&url.length<=240&&/^[\x20-\x7e]+$/.test(url)&&['www.python.org','blog.python.org','discuss.python.org'].includes(new URL(url).hostname);
 try {
  const r=await fetch(url,{redirect:'manual',signal:AbortSignal.timeout(30000)});
  const b=Buffer.from(await r.arrayBuffer());
  const media=(r.headers.get('content-type')||'').split(';')[0].trim().toLowerCase();
  let utf8=true;try{new TextDecoder('utf-8',{fatal:true}).decode(b);}catch{utf8=false;}
  return {url,syntaxValid,status:r.status,contentType:r.headers.get('content-type'),location:r.headers.get('location'),bytes:b.length,utf8,sha256:createHash('sha256').update(b).digest('hex'),satisfiesDirectRetrievalConstraints:r.status===200&&!r.headers.has('location')&&['text/html','text/plain','application/json'].includes(media)&&b.length>0&&b.length<=32768&&utf8};
 }catch(e){return {url,syntaxValid,error:e.message,satisfiesDirectRetrievalConstraints:false};}
}));
const [chain,balance,policy,missing,estimate]=await Promise.all([
 client.request({method:'eth_chainId',params:[]}),
 client.request({method:'eth_getBalance',params:[sender,'latest']}),
 client.request({method:'sim_getFeeConfig',params:[]}),
 client.readContract({address,functionName:'get_case',args:[caseId]}),
 // Use the SDK's complete generic write preset, including its default rotations.
 client.estimateTransactionFees()
]);
if(BigInt(chain)!==61997n||missing!=='')throw Error('Chain mismatch or case ID already used');
const preview={preparedAt:new Date().toISOString(),submitted:false,sdk:'genlayer-js@2.0.0-rc.1',rpc,chainId:61997,contractAddress:address,authorizedSigner:sender,caseSelection:'Recorded Python 3.13.0 final-release case (PLAN.md); beta-case URLs/facts are not recorded in this workspace.',functionName:'evaluate_delay',args:[caseId,...urls,7],unusedCaseRead:{functionName:'get_case',args:[caseId],result:missing},sources,feePolicy:policy,feeEstimate:estimate,balanceWei:BigInt(balance),balanceCoversDeposit:BigInt(balance)>=estimate.feeValue,budgetBasis:'Pinned SDK generic write fallback, not a measured evaluation profile. No targeted simulation or evaluate_delay ran. Constructor cost does not measure web/LLM/validator execution, receipt/storage requirements or elapsed time. Rotations provide bounded consensus retries, not an automatic second submission; appeal rounds zero.',expectedOutcome:{verdict:'NON_EXCUSABLE_DELAY',responsible_party:'MILESTONE_OWNER',reason_code:'OWNER_CONTROLLED',approved_days:0},uncertainty:'Conditional on usable records and independent GenVM assessments. Unavailable commitment/evidence can produce INSUFFICIENT_EVIDENCE; malformed model output, disagreement or resource exhaustion can fail without storing a case. Missing causal interval endpoints never prove a positive extension. GenVM retrieval can differ from this direct HTTP check; redirect destinations remain unenforceable.'};
writeFileSync('deployments/first-evaluation-preview.json',JSON.stringify(preview,(_,v)=>typeof v==='bigint'?v.toString():v,2)+'\n',{flag:'wx'});
console.log(JSON.stringify(preview,(_,v)=>typeof v==='bigint'?v.toString():v,2));
