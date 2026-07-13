"use client";

import { Fragment, useState } from "react";
import { languageNames, localeMetadata, locales, messages, type Locale } from "../src/i18n";

type Profile = { name:string; type:string; country:string; mission:string; beneficiaries:string; budget:string; cofunding:boolean };
const initial: Profile = {name:"Asociația Verde Exemplu",type:"Association",country:"Romania",mission:"Community climate education",beneficiaries:"Young people in rural communities",budget:"€50,000–€100,000",cofunding:true};
const grants = [
  {title:"Community Climate Action 2026",funder:"European Community Foundation",deadline:"30 Sep 2026",amount:"€25,000–€80,000",score:86,why:"Community education and rural youth align with the programme theme.",risk:"Confirm co-funding rate and applicant registration age."},
  {title:"Social Innovation Microgrants",funder:"Romania Civic Fund",deadline:"15 Oct 2026",amount:"€10,000–€40,000",score:74,why:"Romanian associations and measurable local outcomes are eligible.",risk:"Synthetic listing: official call documents require supervisor review."}
];

export default function Home() {
  const [locale,setLocale]=useState<Locale>("hu"); const t=messages[locale];
  const [step,setStep]=useState(0); const [profile,setProfile]=useState(initial); const [done,setDone]=useState(false);
  const patch=(key:keyof Profile,value:string|boolean)=>setProfile(current=>({...current,[key]:value}));
  const fields = [
    <Fragment key="organisation"><Field label={t.orgName} value={profile.name} onChange={v=>patch("name",v)}/><Field label={t.orgType} value={profile.type} onChange={v=>patch("type",v)}/><Field label={t.country} value={profile.country} onChange={v=>patch("country",v)}/></Fragment>,
    <Fragment key="mission"><Field label={t.mission} value={profile.mission} onChange={v=>patch("mission",v)} area/><Field label={t.beneficiaries} value={profile.beneficiaries} onChange={v=>patch("beneficiaries",v)}/></Fragment>,
    <Fragment key="funding"><Field label={t.budget} value={profile.budget} onChange={v=>patch("budget",v)}/><label className="check"><input type="checkbox" checked={profile.cofunding} onChange={e=>patch("cofunding",e.target.checked)}/>{t.cofunding}</label></Fragment>,
    <dl className="review"><div><dt>{t.orgName}</dt><dd>{profile.name}</dd></div><div><dt>{t.country}</dt><dd>{profile.country}</dd></div><div><dt>{t.mission}</dt><dd>{profile.mission}</dd></div><div><dt>{t.budget}</dt><dd>{profile.budget}</dd></div></dl>
  ];
  const headings=[[t.orgTitle,t.orgHelp],[t.missionTitle,t.missionHelp],[t.fundingTitle,t.fundingHelp],[t.reviewTitle,t.reviewHelp]];
  return <main>
    <header className="topbar"><a className="brand" href="#top"><span className="brandMark">GB</span><span>GrantBridge Europe</span></a><label className="language"><span>{t.language}</span><select value={locale} onChange={e=>setLocale(e.target.value as Locale)}>{locales.map(x=><option key={x} value={x}>{languageNames[x]}{localeMetadata[x].reviewStatus==="draft"?" · draft":""}</option>)}</select></label></header>
    <section className="intro" id="top"><span className="pilotBadge">{t.pilot}</span><h1>{t.title}</h1><p>{t.subtitle}</p><div className="notice" role="note">ⓘ {t.synthetic}</div></section>
    <nav className="tabs" aria-label="Workspace"><a href="#profile">{t.profile}</a><a href="#matches">{t.matches}</a></nav>
    <section className="workspace" id="profile"><div className="sectionHead"><div><span className="eyebrow">{t.step} {step+1} {t.of} 4</span><h2>{headings[step][0]}</h2><p>{headings[step][1]}</p></div><div className="progress" aria-label={`${step+1} / 4`}><span style={{width:`${(step+1)*25}%`}}/></div></div>
      {done ? <div className="success" role="status"><span>✓</span><h3>{t.complete}</h3><button onClick={()=>setDone(false)}>{t.edit}</button></div> : <form onSubmit={e=>{e.preventDefault(); if(step<3)setStep(step+1); else setDone(true)}}><div className="formGrid">{fields[step]}</div><div className="formActions"><button type="button" disabled={step===0} onClick={()=>setStep(step-1)}>{t.back}</button><button className="primary" type="submit">{step===3?t.finish:t.next}</button></div></form>}
    </section>
    <section className="matches" id="matches"><div className="sectionHead"><div><span className="eyebrow">{t.matches}</span><h2>{t.matchTitle}</h2></div></div><div className="grantGrid">{grants.map(g=><article className="grant" key={g.title}><div className="grantTop"><span className="verified">✓ {t.verified}</span><strong className="score">{g.score}% <small>{t.score}</small></strong></div><h3>{g.title}</h3><p className="funder">{g.funder}</p><dl className="facts"><div><dt>{t.deadline}</dt><dd>{g.deadline}</dd></div><div><dt>{t.amount}</dt><dd>{g.amount}</dd></div></dl><h4>{t.why}</h4><p>{g.why}</p><h4>{t.risk}</h4><p>{g.risk}</p><div className="grantActions"><button className="primary">{t.interested}</button><button>{t.later}</button><button>{t.irrelevant}</button></div></article>)}</div></section>
  </main>;
}

function Field({label,value,onChange,area=false}:{label:string;value:string;onChange:(v:string)=>void;area?:boolean}) { const id=label.replace(/\W/g,"-"); return <label className="field" htmlFor={id}><span>{label}</span>{area?<textarea id={id} value={value} onChange={e=>onChange(e.target.value)} rows={4}/>:<input id={id} value={value} onChange={e=>onChange(e.target.value)}/>}</label> }
