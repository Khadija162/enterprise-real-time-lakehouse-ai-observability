type Metrics = { status?:string; started_at?:string; bronze_count?:number; silver_count?:number; rejected_count?:number; rejection_rate?:number };
type Alert = { alert_id?:number; severity:string; rule:string; message:string; created_at:string };
const API = process.env.API_BASE_URL || "http://127.0.0.1:8000";
async function getData<T>(path:string, fallback:T):Promise<T>{try{const r=await fetch(API+path,{cache:"no-store"});if(!r.ok)return fallback;return await r.json() as T}catch{return fallback}}
export default async function Home(){
 const metrics=await getData<{latest:Metrics|null}>("/api/metrics",{latest:null});
 const alerts=await getData<{alerts:Alert[]}>("/api/alerts",{alerts:[]});
 const m=metrics.latest;
 return <main><p className="muted">ENTERPRISE DATA PLATFORM</p><h1>Lakehouse Control Center</h1><p className="muted">Azure-ready · Llama incident triage · Read-only dashboard</p>
 <div className="grid">{[["Pipeline status",m?.status??"No runs"],["Bronze events",m?.bronze_count??"—"],["Silver events",m?.silver_count??"—"],["Rejection rate",m?.rejection_rate==null?"—":m.rejection_rate+"%"]].map(([title,value])=><section className="card" key={title}><p className="muted">{title}</p><div className="value">{value}</div></section>)}</div>
 <section className="card" style={{marginTop:20}}><h2>Recent alerts</h2>{alerts.alerts.length===0?<p className="muted">No alerts available. Run the monitoring job to populate this view.</p>:<table><thead><tr><th>Severity</th><th>Rule</th><th>Message</th><th>Created</th></tr></thead><tbody>{alerts.alerts.slice(0,20).map((a,i)=><tr key={a.alert_id??i}><td>{a.severity}</td><td>{a.rule}</td><td>{a.message}</td><td>{a.created_at}</td></tr>)}</tbody></table>}</section>
 <p className="muted">AI analysis is exposed via backend POST /api/ai/analyze with a monitoring run ID. No auto-remediation.</p></main>;
}
